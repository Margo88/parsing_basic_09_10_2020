"""Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы) с сайтов Superjob и HH.
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
### По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas."""

#https://hh.ru/search/vacancy?clusters=true&area=1&search_field=name&enable_snippets=true&salary=&st=searchVacancy&text=Дегустатор

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

vacancy = input('Укажите название вакансии: ')
url = f'https://hh.ru/search/vacancy'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

page = 0

def get_salary(string):
    """Функция выдергивает цифры из зарплаты и возвращает кортеж с мин. и макс. значением зп"""
    string = re.sub(r'\s', '', string)
    value = re.findall(r'\d+', string)
    if 'от' in string:
        return int(value[0]), None
    elif '-' in string:
        return int(value[0]), int(value[1])
    else:
        return None, None

vacancy_dict = {
    'vacancy': [],
    'min_salsry': [],
    'max_salary': [],
    'link': []
}

def get_data_dict(soup):
    """Функция, которая собирает данные в словарь"""
    global vacancy_dict
    for tag in soup:
        name = tag.find('div', {'class': 'vacancy-serp-item__info'}).getText()
        salary = tag.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        link = tag.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        vacancy_dict['vacancy'].append(name)
        vacancy_dict['min_salsry'].append(get_salary(salary)[0])
        vacancy_dict['max_salary'].append(get_salary(salary)[1])
        vacancy_dict['link'].append(link)

def save_data_to_txt(soup, file_name):
    '''Функция, котрая записывает данные в текстовый файл'''
    with open(file_name + '.txt', 'a', encoding='utf-8') as f:
        for tag in soup:
            name = tag.find('div', {'class': 'vacancy-serp-item__info'}).getText()
            salary = tag.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
            link = tag.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
            f.write(f'{name}\t{get_salary(salary)[0]}\t{get_salary(salary)[1]}\t{link}\n')

while True:
    params = {
        'area': '1',
        'search_field': 'name',
        'st': 'searchVacancy',
        'text': vacancy,
        'page': page
    }
    response = requests.get(url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.findAll('div', {'data-qa' : 'vacancy-serp__vacancy', 'class' : 'vacancy-serp-item'})
    if vacancies == []: #если на странице пусто, возвращается пустой список. Выходим из цикла
        break
    #save_data_to_txt(vacancies) - если хочется сохранить в txt
    get_data_dict(vacancies)
    page += 1

df = pd.DataFrame(vacancy_dict)
df.to_excel('vacancies.xlsx')