import json
import os
from collections import Counter

path = r"activities"


with open("cn_enemies", "r", encoding="utf-8") as file:
    stats = json.load(file)

with open("event_names.json", "r", encoding="utf-8") as file:
    names = json.load(file)

output = ""

for root, _, files in os.walk(path, topdown=False):
    counter_maxHp = Counter()
    counter_atk = Counter()
    counter_def = Counter()
    counter_magicResistance = Counter()
    counter_enemy = Counter()    
    
    dir_name = os.path.relpath(root, path)
    chapter_name = f"{names.get(dir_name, dir_name)}"
    output += f"\n{chapter_name}\n"
    try:
        for file in files:
            file_path = f"{root}\{file}"
            with open(file_path, "r", encoding="utf-8") as f:
                item = json.load(f)
                level = item.get("level")
                danger = item.get("dangerLevel")
                if not danger:
                    continue
                for enemy in level.keys():
                    item = stats.get(enemy)
                    if not item:
                        continue
                    count = level.get(enemy)
                    counter_enemy.update({danger:count})
                    counter_maxHp.update({danger:item.get("maxHp") * count})
                    counter_atk.update({danger:item.get("atk") * count})
                    counter_def.update({danger:item.get("def") * count})
                    counter_magicResistance.update({danger:item.get("magicResistance") * count})
            for enemy_count in counter_enemy.values():
                if enemy_count == 0:
                    continue       
        for danger_level in counter_enemy.keys():
            output += f"    {danger_level}\n"
            output += f"        maxHP: {counter_maxHp.get(danger_level)/counter_enemy.get(danger_level):.1f}\n"        
            output += f"        atk: {counter_atk.get(danger_level)/counter_enemy.get(danger_level):.1f}\n"
            output += f"        def: {counter_def.get(danger_level)/counter_enemy.get(danger_level):.1f}\n"
            output += f"        res: {counter_magicResistance.get(danger_level)/counter_enemy.get(danger_level):.1f}\n"      
    except AttributeError:
        print(f"{file} - {item}")

with open("output.txt", "w", encoding="utf-8") as out:
    out.write(output)
    