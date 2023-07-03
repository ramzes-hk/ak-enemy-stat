import json
import os
from collections import Counter
import requests

with open("level_dir.txt", "r", encoding="utf-8") as file:
    path = file.read()
    
with open("event_names.json", "r", encoding="utf-8") as file:
    chapter_names = json.load(file)
    
with open("cn_enemies", "r", encoding="utf-8") as file:
    enemy_db = json.load(file)

url = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/stage_table.json"

response = requests.get(url)
stages = response.json().get("stages")

output = ""

for root, _, files in os.walk(path, topdown=False):
    counter_maxHp = Counter()
    counter_atk = Counter()
    counter_def = Counter()
    counter_magicResistance = Counter()
    counter_enemy = Counter()
    
    dir_name = os.path.relpath(root, path)
    chapter_name = f"{chapter_names.get(dir_name, dir_name)}"
    
    output += f"\n{chapter_name}\n"
    
    for file in files:
        level_name = "_".join(os.path.splitext(file)[0].split("_")[1:])
        level = stages.get(level_name)
        danger = level.get("dangerLevel")
        file_path = f"{root}/{file}"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        waves = data.get("waves")
        enemy_db_refs = data.get("enemyDbRefs")
        for wave in waves:
            fragments = wave.get("fragments")
            for fragment in fragments:
                actions = fragment.get("actions")
                for action in actions:
                    if action.get("actionType") != 0:
                        continue
                    key = action.get("key")
                    count = action.get("count", 0)
                    counter_enemy.update({danger: count})
                    for enemy in enemy_db_refs:
                        if enemy.get("id") != key:
                            continue
                        overwritten = enemy.get("overwrittenData")
                        default_enemy = enemy_db.get(key)
                        maxHp = {
                            danger: default_enemy.get("maxHp", 0) * count}
                        atk = {
                            danger: default_enemy.get("atk", 0) * count}
                        def_ = {
                            danger: default_enemy.get("def", 0) * count}
                        magicResistance = {
                            danger: default_enemy.get("magicResistance", 0) * count}
                        if not overwritten:
                            counter_maxHp.update(maxHp)
                            counter_atk.update(atk)
                            counter_def.update(def_)
                            counter_magicResistance.update(magicResistance)
                            continue
                        attr = overwritten.get("attributes")
                        if attr.get("maxHp").get("m_defined"):
                            maxHp = {
                                danger: attr.get("maxHp").get("m_value", 0) * count}
                            counter_maxHp.update(maxHp)
                        if attr.get("atk").get("m_defined"):
                            atk = {
                                danger: attr.get("atk").get("m_value", 0) * count}
                            counter_atk.update(atk)
                        if attr.get("def").get("m_defined"):
                            def_ = {
                                danger: attr.get("def").get("m_value", 0) * count}
                            counter_def.update(def_)
                        if attr.get("magicResistance").get("m_defined"):
                            magicResistance = {
                                danger: attr.get("magicResistance").get("m_value", 0) * count}
                            counter_magicResistance.update(magicResistance)
                        break
                    break
    for danger in counter_enemy.keys():
        output += f"    {danger}\n"
        output += f"        maxHP: {counter_maxHp.get(danger, 0)/counter_enemy.get(danger, 1):.1f}\n"        
        output += f"        atk: {counter_atk.get(danger, 0)/counter_enemy.get(danger, 1):.1f}\n"
        output += f"        def: {counter_def.get(danger, 0)/counter_enemy.get(danger, 1):.1f}\n"
        output += f"        res: {counter_magicResistance.get(danger, 0)/counter_enemy.get(danger, 1):.1f}\n"

with open("output1.txt", "w", encoding="utf-8") as f:
    f.write(output)

         
                    
                        
    
