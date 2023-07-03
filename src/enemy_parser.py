import json
import requests
import os

def get_enemies(url): 
    response = requests.get(url)
    enemies = response.json().get("enemies")

    formatted_enemies = {}
    for enemy in enemies:
        formatted_enemies.update({
            enemy.get('Key'): {
                "Key": enemy
                    .get("Key"),
                "name": enemy
                    .get("Value")[0]
                    .get("enemyData")
                    .get("name")
                    .get("m_value"),
                "maxHp": enemy
                    .get("Value")[0]
                    .get("enemyData")
                    .get("attributes")
                    .get("maxHp")
                    .get("m_value"),
                "atk": enemy
                    .get("Value")[0]
                    .get("enemyData")
                    .get("attributes")
                    .get("atk")
                    .get("m_value"),
                "def": enemy
                    .get("Value")[0]
                    .get("enemyData")
                    .get("attributes")
                    .get("def")
                    .get("m_value"),
                "magicResistance": enemy
                    .get("Value")[0]
                    .get("enemyData")
                    .get("attributes")
                    .get("magicResistance")
                    .get("m_value") 
            }
        })
    return formatted_enemies

cn = get_enemies("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/levels/enemydata/enemy_database.json")
en = get_enemies("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/levels/enemydata/enemy_database.json")


for key in en.keys():
    cn[key]["name"] = en[key]["name"]

file_path = os.path.join(os.path.dirname(__file__), "..", "cn_enemies.json")
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(cn, file, indent=4, ensure_ascii=False)



    

