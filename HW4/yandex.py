from datetime import datetime
import requests
from lxml import html
from pprint import pprint
import re

url = 'https://yandex.ru/news/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
response = requests.get(url, headers = headers)
dom = html.fromstring(response.text)
news_list = []

titles = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//h2/text()")
links = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//h2/../@href")
time = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//h2/../@data-log-id")

def transform_time(string):
    unix_time = re.findall(r'\d{10}', string)
    unix_time = int(unix_time[0])
    return str(datetime.fromtimestamp(unix_time))

for i, title in enumerate(titles):
    news_dict = {}
    news_dict['title'] = title.replace('\xa0', ' ')
    news_dict['link'] = links[i]
    news_dict['origin'] = url
    news_dict['date'] = transform_time(time[i])
    news_list.append(news_dict)

if __name__ == '__main__':
    pprint(news_list)