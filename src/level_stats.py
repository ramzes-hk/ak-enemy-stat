import json
import os
from collections import Counter

    
with open(os.path.join(os.path.dirname(__file__), "..", "event_names.json"), "r", encoding="utf-8") as file:
    chapter_names = json.load(file)


path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "activities"))
print(path)

output = {}

for root, _, files in os.walk(path, topdown=False):
    counter_maxHp = Counter()
    counter_atk = Counter()
    counter_def = Counter()
    counter_magicResistance = Counter()
    counter_enemy = Counter()
    dir_name = os.path.relpath(root, path)
    chapter_name = f"{chapter_names.get(dir_name, dir_name)}"
    print(chapter_name)
    for file in files:
        file_dir = os.path.join(root, file)
        with open(file_dir, "r", encoding="utf-8") as f:
            stage = json.load(f)
        danger_level = stage.get("dangerLevel")

        for key in stage.keys():
            if key == "dangerLevel":
                continue

            enemy = stage.get(key)
            count = enemy.get("count", 0)
            maxHp = enemy.get("maxHp", 0) * count
            atk = enemy.get("atk", 0) * count
            def_ = enemy.get("def", 0) * count
            magicResistance = enemy.get("magicResistance", 0) * count
            
            counter_enemy.update({danger_level: count})
            counter_maxHp.update({danger_level: maxHp})
            counter_atk.update({danger_level: atk})
            counter_def.update({danger_level: def_})
            counter_magicResistance.update({danger_level: magicResistance})
    
    stats = {
        "maxHP": counter_maxHp,
        "atk": counter_atk,
        "def": counter_def,
        "res": counter_magicResistance
    }
    chapter = {} 
    for key in counter_enemy.keys():
        chapter.update({})
        count = counter_enemy.get(key, 0)
        danger = {} 
        for stat, counter in stats.items():
            danger.update({stat: "{:.1f}".format(counter.get(key, 0)/count)})
            chapter.update({key: danger})
    print(chapter)       
    output.update({chapter_name: chapter})


    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
