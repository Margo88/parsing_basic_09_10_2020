'''Написать программу, которая собирает входящие
письма из своего или тестового почтового ящика и
сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from pymongo import MongoClient
import time
from datetime import datetime
import re

client = MongoClient('127.0.0.1', 27017)
db = client['inbox']
my_letters = db.my_letters

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe')

driver.get('https://mail.ru/')

login = driver.find_element_by_name('login')
login.send_keys('study.ai_172')

button = driver.find_element_by_id('mailbox:submit-button')
button.click()

passw = driver.find_element_by_name('password')
passw.send_keys('NextPassword172')

passw.send_keys(Keys.ENTER)

first_letter = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'llc'))
)
driver.get(first_letter.get_attribute('href'))

def transorm_time(string):
    # '22 октября, 11:16'
    # '22 октября 2019, 11:16'
    rus_month = {
        'января': '1',
        'февраля': '2',
        'марта': '3',
        'апреля': '4',
        'мая': '5',
        'июня': '6',
        'июля': '7',
        'августа': '8',
        'сентября': '9',
        'октября': '10',
        'ноября': '11',
        'декабря': '12',
    }
    month = re.search(r'\b[а-я]+', string)[0]
    tm = string.replace(month, rus_month[month])
    try:
        return str(datetime.strptime(tm, '%d %m %Y, %H:%M'))
    except ValueError:
        return str(datetime.strptime(tm, '%d %m, %H:%M')).replace('1900', '2020')

while True:
    letter = {}
    try:
        letter['topic'] = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))).text
        date = driver.find_element_by_class_name('letter__date').text
        letter['date'] = transorm_time(date)
        letter['from'] = driver.find_element_by_class_name('letter-contact').get_attribute('title')
        letter['body'] = driver.find_element_by_class_name('letter__body').text
        my_letters.update_one(letter, {'$set': letter}, upsert=True)
    except StaleElementReferenceException:
        continue
    #нашла кнопку "следующее" на странице письма
    try:
        next_page = driver.find_element_by_class_name("button2.button2_has-ico.button2_arrow-down.button2_pure.button2_short.button2_ico-text-top.button2_hover-support.js-shortcut")
        next_page.click()
        #нужно немного подождать, иначе начет парсить страницу второй раз до открытия следующей
        time.sleep(1)
    #в последнем письме кнопки нет
    except NoSuchElementException:
        break

# Пробовала сначла собрать список всех ссылок на письма, но не придумала, как остановиться:
# links = []
# while True:
#     inbox = driver.find_elements_by_class_name('llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')
#     for itm in inbox:
#         links.append(itm.get_attribute('href'))
#     actions = ActionChains(driver)
#     actions.move_to_element(inbox[-1])
#     actions.perform()
#
# unique_links = set(links)