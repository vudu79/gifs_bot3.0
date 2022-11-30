import json

with open("static/stickers_tlgrm.json", "r", encoding="utf-8") as file:
    stickers_list = json.load(file)
stickers_dict = {}

for pack in stickers_list:
    stickers_dict[pack["name"]] = pack


with open('calendar.json', 'r', encoding='utf-8') as f:
    js = f.read()

calendar_dict = json.loads(js)

with open('calendar_storage.json', 'r', encoding='utf-8') as f:
    js = f.read()

calendar_storage = json.loads(js)
