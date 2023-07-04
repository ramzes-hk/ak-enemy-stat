import json 
import os 
from exceptions import JSONException
import collections.abc

file_path = os.path.join(os.path.dirname(__file__), "..", "cn_enemies.json")
with open(file_path, "r", encoding="utf-8") as f:
    enemy_db = json.load(f)

def read_level(file) -> dict:
    enemy_counter = collections.Counter()
    with open(file, "r", encoding="utf-8") as f:
        buffer = json.load(f)
    waves = buffer.get("waves")
    enemy = {}
    if not waves:
        raise JSONException(message="No key:'waves'", file=file) 
    for wave in waves:
        fragments = wave.get("fragments")
        if not fragments and not isinstance(fragments, collections.abc.Sequence):
            raise JSONException(message="No key: 'fragments'", file=file)
        for fragment in fragments:
            actions = fragment.get("actions")
            if not actions:
                raise JSONException(message="No key: 'actions'", file=file) 
            for action in actions:
                action_type = action.get("actionType", 0)
                if action_type != 0:
                    continue
                enemy_key = action.get("key")
                enemy_count = action.get("count")
                enemy_counter.update({enemy_key: enemy_count})

                enemy_params = get_enemy_stats(enemy_key, file)
                enemy_params.update({"count": enemy_counter.get(enemy_key)})
                enemy.update({enemy_key: enemy_params})
    return enemy


def get_enemy_stats(key, file) -> dict:
    enemy = {}
    enemy_default = enemy_db.get(key)
    if enemy_default:
        enemy.update({"maxHp": enemy_default.get("maxHp")})    
        enemy.update({"atk": enemy_default.get("atk")}) 
        enemy.update({"def": enemy_default.get("def")})          
        enemy.update({"magicResistance": enemy_default.get("magicResistance")})
    with open(file, "r", encoding="utf-8") as f:
        stage = json.load(f)
    enemy_refs = stage.get("enemyDbRefs")
    if not enemy_refs:
        return enemy
    for enemy_ref in enemy_refs:
        if enemy_ref.get("id") != key:
            continue
        overwritten = enemy_ref.get("overwrittenData")
        if not overwritten:
            break
        attributes = overwritten.get("attributes")
        if not attributes:
            break
        maxHp = attributes.get("maxHp")
        atk = attributes.get("atk")
        def_ = attributes.get("def")
        magicResistance = attributes.get("magicResistance")
        if maxHp.get("m_defined"):
            enemy.update({"maxHp": maxHp.get("m_value")})
        if atk.get("m_defined"):
            enemy.update({"atk": atk.get("m_value")})
        if def_.get("m_defined"):
            enemy.update({"def": def_.get("m_value")})
        if magicResistance.get("m_defined"):
            enemy.update({"magicResistance": magicResistance.get("m_value")})
    return enemy 


                    
def traverse_levels(url):
    path = os.path.join(os.path.dirname(__file__), "..", "activities", "main")
    if not os.path.exists(path):
        os.mkdir(path)
    for root, _, files in os.walk(url, topdown=False):
        for file in files:
            chapter_number_stage = file.split("_")[2]
            chapter_number = chapter_number_stage.split("-")[0]
            chapter_dir = f"{path}/main_{chapter_number}"
            if not os.path.exists(chapter_dir):
                os.mkdir(chapter_dir)
            file_read_path = f"{root}/{file}"
            file_write_path = f"{chapter_dir}/{file}"
            level = {}
            level.update(read_level(file_read_path))
            with open(file_write_path, "w", encoding="utf-8") as f:
                json.dump(level, f, ensure_ascii=False, indent=4)
           
file_path = os.path.join(os.path.dirname(__file__), "..", "main_level_dir.txt")
       
with open(file_path, "r") as f:
    traverse_levels(fr"{f.read()}")
