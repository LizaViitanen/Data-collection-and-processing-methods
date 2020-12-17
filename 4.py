import requests
from lxml import html
from pprint import pprint



def get_link(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.ok:
        dom = html.fromstring(response.text)
        return dom
    else:
        return False

#Яндекс новости/ блок Санкт-Петербург

ya = 'https://yandex.ru/news/'
dom = get_link(ya)
items = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-rubric-stories news-app__top'][last()-11]")
all_news = []
for item in items:
    name = item.xpath(".//h2[@class='mg-card__title']/text()")
    link = item.xpath(".//span[@class='mg-card-source__source']//@href")
    source = item.xpath(".//span[@class='mg-card-source__source']//text()")
    date = item.xpath(".//span[@class='mg-card-source__time']/text()")
    for n in range(len(name)):
        news = {}
        news['name'] = name[n]
        news['link'] = link[n]
        news['source'] = source[n]
        news['date'] = date[n]
        all_news.append(news)
print(f'\n\n----------Новости {ya} -------------\n\n')
pprint(all_news)


#lenta.ru

lenta = 'https://lenta.ru'
dom = get_link(lenta)
items = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']")
all_news = []
for item in items:
    news = {}
    link = item.xpath(".//div[@class='item']//@href")
    name = item.xpath(".//div[@class='item']/a/text()")
    source = 'Lenta.ru'
    date = item.xpath(".//div[@class='item']//@datetime")
    for n in range(len(name)):
        news = {}
        news['name'] = name[n].replace("\xa0", " ")
        news['link'] = lenta+link[n]
        news['source'] = source
        news['date'] = date[n]
        all_news.append(news)
for item in items:
    news = {}
    link = item.xpath(".//div[@class='first-item']//h2//@href")
    name = item.xpath(".//div[@class='first-item']//h2//a/text()")
    source = 'Lenta.ru'
    date = item.xpath(".//div[@class='first-item']//h2//@datetime")

    news['name'] = name[0].replace("\xa0", " ")
    news['link'] = lenta+link[0]
    news['source'] = source
    news['date'] = date
    all_news.append(news)
print(f'\n\n----------Новости {lenta} -------------\n\n')
pprint(all_news)


#Новости Санкт-Петербурга и Ленинградской области на странице новостей mail.ru

mail = 'https://news.mail.ru/'
dom = get_link(mail)
items = dom.xpath("//div[@class='block block_bg_primary block_separated_top link-hdr']")
all_news = []
for item in items:
    link = item.xpath(".//a[@class='newsitem__title link-holder']//@href")
    for i in link:
        news = {}
        i = str(i)
        dom_new = get_link(i)
        info_link = dom_new.xpath("//div[contains(@class,'js-article')]")
        for info in info_link:
            name = info.xpath(".//span[@class='hdr__text']//text()")
            source = info.xpath(".//span[@class='link__text']/text()")
            date = info.xpath(".//span[@class='note']//@datetime")
            link = i

            news['name'] = name
            news['link'] = link
            news['source'] = source
            news['date'] = date[0].replace("T", " ")
            all_news.append(news)

for item in items:
    link = item.xpath(".//ul/li//@href")
    for i in link:
        news = {}
        i = str(i)
        dom_new = get_link(i)
        info_link = dom_new.xpath("//div[contains(@class,'js-article')]")
        for info in info_link:
            name = info.xpath(".//span[@class='hdr__text']//text()")
            source = info.xpath(".//span[@class='link__text']/text()")
            date = info.xpath(".//span[@class='note']//@datetime")
            link = i

            news['name'] = name
            news['link'] = link
            news['source'] = source
            news['date'] = date[0].replace("T", " ")
            all_news.append(news)
print(f'\n\n----------Новости {mail} -------------\n\n')
pprint(all_news)