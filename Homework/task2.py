"""2. Изучить список открытых API
(https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию.
Ответ сервера записать в файл."""

#NASA
#Регистрируюсь, получаю ключ
#utwhR7J90Bl1fQykJgqYfXOR8YToHFwtpjKiygX9
#https://api.nasa.gov/EPIC/api/natural/date/2020-10-10?api_key=utwhR7J90Bl1fQykJgqYfXOR8YToHFwtpjKiygX9

import requests

date = '2020-10-10'
url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
params = {
    'api_key' : 'utwhR7J90Bl1fQykJgqYfXOR8YToHFwtpjKiygX9'
}

response = requests.get(url, params=params)
j_data = response.json()[0]

#сохраняю id снимка
image_id = j_data['image']

date_for_img = date.replace('-', '/')
#Находим снимок планеты
image_url = f'https://api.nasa.gov/EPIC/archive/natural/{date_for_img}/png/{image_id}.png?api_key=utwhR7J90Bl1fQykJgqYfXOR8YToHFwtpjKiygX9'
img = requests.get(image_url)
#Записываем в файл
out = open("earth.jpg", "wb")
out.write(img.content)
out.close()