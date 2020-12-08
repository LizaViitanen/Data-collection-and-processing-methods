#https://api.windy.com/api/webcams/v2/[path]
#ключ авторизации API из первого шага может находиться в:
#заголовок запроса "x-windy-key": "your_API_key",
#или получить параметр ?key=your_API_key
# nk8ZS1BmmsOHHMQBrAWn9wyKS5rrL1iA

import requests
from pprint import pprint
import json

response = requests.get('https://api.windy.com/api/webcams/v2/list/?/api/webcams/v2/list/country=DE&lang=ru&key=nk8ZS1BmmsOHHMQBrAWn9wyKS5rrL1iA')
if response.ok:
    j_data = response.json()
    pprint(j_data)

with open("windy.json", 'w', encoding="utf-8") as file:
    json.dump(j_data, file, ensure_ascii=False)