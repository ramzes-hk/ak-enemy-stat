import json 
import requests
import os

url = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/stage_table.json"

response = requests.get(url)
levels = response.json().get("stages")
activities_path = os.path.join(os.path.dirname(__file__), "..", "activities")

for root, _, files in os.walk(activities_path, topdown=False):
    for file in files:
        print(file)
        level_name = "_".join(os.path.splitext(file)[0].split("_")[1:])
        level = levels.get(level_name)
        if level:
            danger = level.get("dangerLevel")
            if danger:
                dir = f"{root}/{file}"
                item = {}
                with open(dir, "r", encoding="utf-8") as f:
                    item = json.load(f)
                    item.update({"dangerLevel": danger})
                with open(dir, "w", encoding="utf-8") as f:
                    json.dump(item, f, ensure_ascii=False, indent=4)
                    
