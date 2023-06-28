import json
import os

path = r"activities"


with open("cn_enemies", "r", encoding="utf-8") as file:
    stats = json.load(file)

with open("event_names.json", "r", encoding="utf-8") as file:
    names = json.load(file)

for root, _, files in os.walk(path, topdown=False):
    total_maxHp = 0
    total_atk = 0
    total_def = 0
    total_magicResistance = 0
    total_enemy = 0
    dir_name = os.path.relpath(root, path)
    chapter_name = f"{names.get(dir_name, dir_name)}"
    print(f"\n{chapter_name}")
    try:
        for file in files:
            file_path = f"{root}\{file}"
            with open(file_path, "r", encoding="utf-8") as f:
                level = json.load(f).get("level")
                for enemy in level.keys():
                    item = stats.get(enemy)
                    if not item:
                        continue
                    count = level.get(enemy)
                    total_enemy += count
                    total_maxHp += item.get("maxHp") * count
                    total_atk += item.get("atk") * count
                    total_def += item.get("def") * count
                    total_magicResistance += item.get("magicResistance") * count
        if total_enemy == 0:
            continue
        print(f"maxHp: {total_maxHp/total_enemy:.1f}")
        print(f"atk: {total_atk/total_enemy:.1f}")
        print(f"def: {total_def/total_enemy:.1f}")
        print(f"res: {total_magicResistance/total_enemy:.1f}")    
    except AttributeError:
        print(f"{file} - {item}")
    