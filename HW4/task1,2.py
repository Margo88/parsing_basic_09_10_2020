''' №1. Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru,
yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
№2. Сложить собранные данные в БД'''

from HW4 import mail, lenta, yandex
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news']
latest_news = db.latest_news

items = []
items.append(lenta.news_list[0])
items.append(yandex.news_list[0])
items.append(mail.news_list[0])

print(items)

def add_records(collection_name, insertion_list):
    for item in insertion_list:
        collection_name.update_one(item, {'$set' : item}, upsert=True)

add_records(latest_news, items)