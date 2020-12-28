from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mail']
mail_db = db.mail_db

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')

ent = driver.find_element_by_name('login')
ent.send_keys('study.ai_172')
ent.send_keys(Keys.ENTER)
time.sleep(3)

ent = driver.find_element_by_name('password')
ent.send_keys('NextPassword172')
ent.send_keys(Keys.ENTER)

time.sleep(5)
# ищем количество писем в ящике
message = driver.find_element_by_xpath("//a[@class='nav__item js-shortcut nav__item_active nav__item_shortcut nav__item_expanded_true nav__item_child-level_0']")
a = message.get_attribute('title')
count_mes = ''
for i in a:
    if i.isdigit():
        count_mes = count_mes + i
print(count_mes)

all_href = []
last_href = ''
while True:
    hrefs = driver.find_elements_by_class_name("llc")
    for href in hrefs:
        all_href.append(href.get_attribute('href'))
    if last_href == hrefs[-1].get_attribute('href'):
        break
    last_href = hrefs[-1].get_attribute('href')
    actions = ActionChains(driver)
    actions.move_to_element(hrefs[-1])
    actions.perform()
    time.sleep(5)
new_href = []
for href in all_href:
    if href not in new_href:
        new_href.append(href)
# смотрим, чтобы количество записей совпадало с количеством писем в ящике
print(len(new_href))

mails = {}
for href in new_href:
    driver.get(href)
    time.sleep(5)

    sender_mail = driver.find_element_by_class_name('letter-contact')
    sender = sender_mail.get_attribute('title')
    date_mail = driver.find_element_by_class_name('letter__date')
    date = date_mail.text
    topic_mail = driver.find_element_by_css_selector('h2')
    topic = topic_mail.text
    body_mail = driver.find_element_by_class_name('letter-body')
    body = body_mail.text
    print(body)

    mails['sender'] = sender
    mails['date'] = date
    mails['topic'] = topic
    mails['body'] = body
    mail_db.insert_one(mails)
pprint(mails)
