import requests
from lxml import html
from pprint import pprint

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
response = requests.get(url, headers = headers)
dom = html.fromstring(response.text)
news_list = []

titles = dom.xpath("//td//span[contains(@class,'photo__title')]/text()")
links = dom.xpath("//td/div/a/@href")

for i, title in enumerate(titles):
    news_dict = {}
    news_dict['origin'] = url
    news_dict['title'] = title.replace('\xa0', ' ')
    news_dict['link'] = links[i]
    r = requests.get(links[i], headers = headers)
    d = html.fromstring(r.text)
    time = d.xpath("//div//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0].replace('T', ' ')
    news_dict['date'] = time.replace('+03:00', '')
    news_list.append(news_dict)

if __name__ == '__main__':
    pprint(news_list)