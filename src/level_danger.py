import json 
import requests
import os

url = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/stage_table.json"

response = requests.get(url)
levels = response.json().get("stages")

for root, _, files in os.walk("activities", topdown=False):
    path = f"activities/{os.path.relpath(root, url)}"
    for file in files:
        level_name = "_".join(os.path.splitext(file)[0].split("_")[1:])
        level = levels.get(level_name)
        if level:
            danger = level.get("dangerLevel")
            if danger:
                dir = f"{root}/{file}"
                with open(dir, "r", encoding="utf-8") as f:
                    try:
                        item = json.load(f)
                        item.update({"dangerLevel": danger})
                    except json.decoder.JSONDecodeError:
                        print(dir)
                with open(dir, "w", encoding="utf-8") as f:
                    json.dump(item, f, ensure_ascii=False, indent=4)
                    