"""Сбор данных с сайтов hh.ru и superjob.ru"""
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
vacancy = input('Укажите название вакансии: ') #почтальон
vacancy_list = [] #сюда будут записаны собранные данные

def get_salary(string):
    string = re.sub(r'\s', '', string)
    value = re.findall(r'\d+', string)
    if string == 'Подоговорённости':
        return None, None
    elif 'от' in string:
        return int(value[0]), None
    elif len(value) == 2:
        return int(value[0]), int(value[1])
    elif 'до' in string:
        return None, int(value[0])
    else:
        return None, None

def get_data_dict(soup, name_tag, salary_tag, get_link_code):
    global vacancy_dict
    for tag in soup:
        name = tag.find(name_tag).getText()
        salary = tag.find(salary_tag).getText()
        link = get_link_code
        vacancy_dict['vacancy'].append(name)
        vacancy_dict['min_salary'].append(get_salary(salary)[0])
        vacancy_dict['max_salary'].append(get_salary(salary)[1])
        vacancy_dict['link'].append(link)

def collect_data(url, origin, params, start_page, vacancies_class, last_page_class, name_class, salary_tag, salary_class, link_class):
    """Функция собирает данные с двух сайтов и записывает их в vacancy_list"""
    global vacancy_list
    while True:
        params['page'] = start_page
        response = requests.get(url, params=params, headers=headers)
        soup = bs(response.text, 'html.parser')
        vacancies = soup.findAll('div', vacancies_class)
        for tag in vacancies:
            temp_dict = {}
            name = tag.find('div', name_class).getText()
            salary = tag.find(salary_tag, salary_class).getText()
            link = tag.find('a', link_class)['href']
            temp_dict['vacancy'] = name
            temp_dict['min_salary'] = get_salary(salary)[0]
            temp_dict['max_salary'] = get_salary(salary)[1]
            temp_dict['origin'] = origin
            if origin == 'https://www.superjob.ru':
                temp_dict['link'] = f'{origin}{link}'
            else:
                temp_dict['link'] = link
            vacancy_list.append(temp_dict)
        if soup.find('a', last_page_class):
            start_page += 1
        else:
            break

hh_start_page = 0
hh_params = {
    'area': '1',
    'search_field': 'name',
    'st': 'searchVacancy',
    'text': vacancy,
    'page': 0
}

collect_data(url='https://hh.ru/search/vacancy',
             params=hh_params,
             start_page=0,
             last_page_class= {'data-qa' : 'pager-next'},
             vacancies_class= {'data-qa' : 'vacancy-serp__vacancy', 'class' : 'vacancy-serp-item'},
             name_class= {'class': 'vacancy-serp-item__info'},
             salary_tag = 'div', salary_class={'class': 'vacancy-serp-item__sidebar'},
             link_class={'class': 'bloko-link HH-LinkModifier'},
             origin='https://hh.ru/')

sj_start_page = 1
sj_params = {
    'keywords' : vacancy,
    'geo[t][0]' : 4,
    'page' : 1
}

collect_data(url='https://www.superjob.ru/vacancy/search/',
             params=sj_params,
             start_page=1,
             last_page_class= {'class' : 'f-test-button-dalshe'},
             vacancies_class= {'class' : 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'},
             name_class= {'class' : '_3mfro PlM3e _2JVkc _3LJqf'},
             salary_tag = 'span', salary_class={'class' : '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'},
             link_class={"class" : "icMQ_"},
             origin='https://www.superjob.ru')

if __name__ == '__main__':
    print(vacancy_list)
    df = pd.DataFrame(vacancy_list)
    print(df)