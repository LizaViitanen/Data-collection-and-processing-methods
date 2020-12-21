from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
db = client['vacansies_db']
hh = db.hh

def insert_vacancies(positions, hh):
    if len(positions) > 0:
        hh.insert_many(positions)


def search_salary(summa):
    result = []
    salary = int(summa)
    for vac in hh.find({'$or': [{'min':{'$gt': salary}}, {'max':{'$gt': salary}}]}):
        result.append(vac)
    return result

vacancy = input("Введите название вакансии: ")

main_link = 'https://spb.hh.ru'
params = {'st': 'searchVacancy',
          'text': vacancy,
          'page': 0}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400'}

link = f'{main_link}/search/vacancy'

responce = requests.get(link, params=params, headers=headers)
soup = bs(responce.text, 'html.parser')

if responce.ok:
    general_data = []
    while True:
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item HH-VacancySidebarTrigger-Vacancy'})
        positions = []
        for position in vacancy_list:
            vacancy_data = {}
            vacancy_name = position.find('a')
            vacancy_salary_gen = position.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
            vacancy_link = vacancy_name['href']

            # убираем кракозябры из вывода зарплаты
            vacancy_salary_cut = position.find('div', {'class': 'vacancy-serp-item__sidebar'}).text.split(' ')
            # оставляем только цифры или диапозон
            vacancy_salary_generaly = ''
            for i in vacancy_salary_gen:
                if i.isdigit() or i == '-':
                    vacancy_salary_generaly = vacancy_salary_generaly + i
            # 1 зп неуказана
            if vacancy_salary_generaly == '':
                vacancy_salary_generaly = {'max': None, 'min': None, 'currency': None}
            # 2 зп указана в диапозоне или от\до
            else:
                if "от" in vacancy_salary_gen:
                    min_salary = vacancy_salary_generaly
                    vacancy_salary_generaly = {'max': None, 'min': int(min_salary), 'currency': vacancy_salary_cut[2]}
                elif "до" in vacancy_salary_gen:
                    max_salary = vacancy_salary_generaly
                    vacancy_salary_generaly = {'max': int(max_salary), 'min': None, 'currency': vacancy_salary_cut[2]}
                else:
                    vacancy_salary = vacancy_salary_generaly.split('-')
                    min_salary = vacancy_salary[0]
                    max_salary = vacancy_salary[1]
                    vacancy_salary_generaly = {'min': int(min_salary), 'max': int(max_salary),
                                               'currency': vacancy_salary_cut[1]}

            vacancy_data['link'] = vacancy_link
            vacancy_data['salary'] = vacancy_salary_generaly
            vacancy_data['name'] = vacancy_name.text

            positions.append(vacancy_data)
        ins = insert_vacancies(positions,hh)
        general_data.append(positions)
        next_page = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if next_page == None:
            break
        redir_page = main_link + next_page['href']
        responce = requests.get(redir_page, headers=headers)
        soup = bs(responce.text, 'html.parser')

    pprint(general_data)
    #hh.find({})

    a = 100000
    res = search_salary(a)
    print(res)