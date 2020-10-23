import re
import requests
from lxml import html
from pprint import pprint
from datetime import datetime

url = 'https://lenta.ru'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
response = requests.get(url, headers = headers)
dom = html.fromstring(response.text)
news_list = []

titles = dom.xpath("//div[@class='span4']//div[@class='item']/a/text() | //div[@class='span4']//div[@class='first-item']//h2/a/text()")
links = dom.xpath("//div[@class='span4']//div[@class='item']/a/@href | //div[@class='span4']//div[@class='first-item']//h2/a/@href")
time = dom.xpath("//a/time/@datetime")

def transform_time(string):
    rus_month = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': '10',
        'ноября': 11,
        'декабря': 12,
    }
    month = re.findall(r'\b[а-я]+', string)[0]
    time = string.replace(month, rus_month[month])
    return str(datetime.strptime(time, ' %H:%M, %d %m %Y'))

for i, title in enumerate(titles):
    news_dict = {}
    news_dict['title'] = title.replace('\xa0', ' ')
    news_dict['link'] = f'{url}{links[i]}'
    news_dict['origin'] = url
    news_dict['date'] = transform_time(time[i])
    news_list.append(news_dict)

if __name__ == '__main__':
    pprint(news_list)
