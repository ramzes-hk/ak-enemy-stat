import json 
import os 
from collections import Counter


def read_level(url):
    try:
        enemies = Counter()
        with open(url, "r", encoding="utf-8") as file:
            data = json.load(file).get("waves")
        for wave in data:
            for action in wave.get("fragments"):
                for item in action.get("actions"):
                    if item.get("actionType") == 0:
                        enemies.update(
                            {f"{item.get('key')}": item.get("count")}
                            )
    except UnicodeDecodeError:
        print(url)
    return enemies
                    
                    
def traverse_levels(url):
    for root, _, files in os.walk(url):
        path = f"activities/main"
        if not os.path.exists(path):
            os.mkdir(path)
        for file in files:
            chapter_number_stage = file.split("_")[2]
            chapter_number = chapter_number_stage.split("-")[0]
            chapter_dir = f"{path}/main_{chapter_number}"
            if not os.path.exists(chapter_dir):
                os.mkdir(chapter_dir)
            file_read_path = f"{root}/{file}"
            file_write_path = f"{chapter_dir}/{file}"
            level = {"level": read_level(file_read_path)}
            with open(file_write_path, "w", encoding="utf-8") as f:
                json.dump(level, f, ensure_ascii=False, indent=4)
            
        
with open("main_level_dir.txt", "r") as f:
    traverse_levels(fr"{f.read()}")