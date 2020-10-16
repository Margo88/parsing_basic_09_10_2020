"""для сайта superjob"""
#https://www.superjob.ru/vacancy/search/?keywords=%D0%A8%D0%B2%D0%B5%D1%8F&geo%5Bt%5D%5B0%5D=4
import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.superjob.ru/vacancy/search/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
vacancy = 'повар'

page = 1

params = {
    'keywords' : vacancy,
    'geo[t][0]' : 4,
    'page' : page
}

response = requests.get(url, params=params, headers=headers)
soup = bs(response.text, 'html.parser')
vacancies = soup.findAll('div', {'class' : 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
for vacancy in vacancies:
    name = vacancy.find('div', {'class' : '_3mfro PlM3e _2JVkc _3LJqf'}).getText()
    salary = vacancy.find('span', {'class' : '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()
    find_link = vacancy.find('a', {'class' : 'icMQ_'})['href']
    link = f'https://www.superjob.ru{find_link}'
    print(name, salary, link)

