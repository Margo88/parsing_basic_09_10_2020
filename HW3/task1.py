# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге
# MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
# 3. Написать функцию, которая будет добавлять
# в вашу базу данных только новые вакансии с сайта.

from HW3.collecting_data import vacancy_list
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['job_db']
vacancies = db.vacancies

#функция, которая добавляет в базу уникальные вакансии
def add_unique_records(collection_name, insertion_list):
    """Принимает имя коллекции и список вакансий"""
    for item in insertion_list:
        collection_name.update_one(item, {'$set' : item}, upsert=True) #включенный параметр upsert добавит данные, если не нашел из в базе

# альтернативная реализация:
# for item in insertion_list:
#     предположим, что ссылка на вакансию - уникальный идентификатор. Если документ с указанной ссылкой не найден, добавляем запись:
#     if not item.find({'link' : item['link']}):
#         insertion_list.insert_one(item)

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой суммы.

def big_salary(value, collection_name):
    """Принимает значение ЗП и имя коллекции"""
    for item in collection_name.find({'min_salary' : {'$gt':value}}):
        pprint(item)

add_unique_records(collection_name=vacancies, insertion_list=vacancy_list)
big_salary(value=30000, collection_name=vacancies)
