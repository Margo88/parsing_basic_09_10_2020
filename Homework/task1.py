"""1. Посмотреть документацию к API GitHub,
разобраться как вывести список репозиториев для конкретного
пользователя, сохранить JSON-вывод в файле *.json."""
import requests
import json
url = 'https://api.github.com'
user='Margo88'

response = requests.get(f'{url}/users/{user}/repos')
#выводим список репозиториев
for _ in response.json():
    print(_['name'])

#записываем json-вывод в файл
with open('repos.json', 'w') as f:
    json.dump(response.json(), f)

