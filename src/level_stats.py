import json
import os

path = r"activities"

def avg_stats(path):
    with open("cn_enemies", "r", encoding="utf-8") as file:
        stats = json.load(file)
    
    for root, _, files in os.walk(path, topdown=False):
        total_maxHp = 0
        total_atk = 0
        total_def = 0
        total_magicResistance = 0
        total_enemy = 0
        print("\n")
        print(root)
        try:
            for file in files:
                file_path = f"{root}\{file}"
                with open(file_path, "r", encoding="utf-8") as f:
                    level = json.load(f).get("level")
                    for enemy in level.keys():
                        item = stats.get(enemy)
                        count = level.get(enemy)
                        total_enemy += count
                        total_maxHp += item.get("maxHp") * count
                        total_atk += item.get("atk") * count
                        total_def += item.get("def") * count
                        total_magicResistance += item.get("magicResistance") * count
            print(f"maxHp: {total_maxHp/total_enemy}")
            print(f"atk: {total_atk/total_enemy}")
            print(f"def: {total_def/total_enemy}")
            print(f"res: {total_magicResistance/total_enemy}")    
        except AttributeError:
            print(file)
            
avg_stats(path)
    