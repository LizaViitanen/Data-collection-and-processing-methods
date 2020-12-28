from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru')

hits = driver.find_element_by_xpath('//div[contains(text(), "Хиты продаж")]/ancestor::div[@class="section"]')
all_goods = []
while True:
    goods = hits.find_elements_by_xpath('//a[@class="fl-product-tile c-product-tile fl-product-tile_gallery-product-set"]')
    for good in goods:
        name = good.find_elements_by_css_selector('//h4').title

