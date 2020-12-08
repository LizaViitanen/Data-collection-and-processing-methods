import requests
import json
from pprint import pprint
r = requests.get('https://api.github.com/users/annasemenova91/repos', auth=('LizaViitanen', '2c81e1ff89665a17a568a4e88625b43a912ab6ab'))
print((r.json()[0]['name']))
data = r.json()[0]
pprint(data)

with open("my_repos1.json", 'w', encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)