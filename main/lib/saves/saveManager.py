import json
import os
import pickle
from datetime import datetime
from lib.monsters.wolf import DarkWolf
from lib.monsters.snake import Snake
from lib.monsters.Paraflower import Flower
from lib.monsters.zhiyin_box import Box
from lib.monsters.Warrant import Warrant
from lib.monsters.dragon import Dragon
from lib.monsters.firegiant import Firegiant

save_folder = "save"

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

def save_game(slot_num, game):
    """保存游戏状态到指定槽位"""
    save_data = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'level_locks': {'level1':True,
                        'level2':False,
                        'level3':False,
                        'level4':False,
                        'level5':False,
                        'level6':False
                        },
        'player_lv': game.player_lv,
        'levels': {},
        'magic_lock': game.magic_lock,
        'cure_lock': game.cure_lock
    }
    for i in range(1,7):
        if game.level_Lock[i]:
            save_data['level_locks'][f'level{i}'] = True
        else:
            save_data['level_locks'][f'level{i}'] = False
    # 保存每个关卡的状态
    for level_num in range(1, 6):
        level = getattr(game, f'level{level_num}')
        level_data = {
            'player': {
                'hp': level.player.hp,
                'mp': level.player.mp,
                'position': (level.player.rect.x, level.player.rect.y)
            },
            'enemies': []
        }

        # 保存敌人状态
        for enemy in level.enemies:
            if enemy.active:
                enemy_data = {
                    'type': enemy.__class__.__name__,
                    'hp': enemy.hp,
                    'position': (enemy.rect.x, enemy.rect.y),
                    'active': enemy.active
                }
                level_data['enemies'].append(enemy_data)

        save_data['levels'][f'level{level_num}'] = level_data

    # 保存到文件
    save_path = os.path.join(save_folder, f'save{slot_num}.json')
    with open(save_path, 'w') as f:
        json.dump(save_data, f, indent=2)

def load_game(slot_num, game):
    """从指定槽位加载游戏状态"""
    save_path = os.path.join(save_folder, f'save{slot_num}.json')
    
    if not os.path.exists(save_path):
        return False

    with open(save_path, 'r') as f:
        save_data = json.load(f)

    # 恢复关卡解锁状态
    level_Lock = save_data['level_locks']
    for i in range(1,7):
        if level_Lock[f'level{i}']:
            game.level_Lock[i] = True
        else:
            game.level_Lock[i] = False
    
    # 恢复技能锁
    game.magic_lock = save_data['magic_lock']
    game.cure_lock = save_data['cure_lock']
    
    # 恢复玩家等级
    game.player_lv = save_data.get('player_lv', 1)

    # 恢复每个关卡状态
    for level_num in range(1, 6):
        level = getattr(game, f'level{level_num}')
        level_data = save_data['levels'][f'level{level_num}']

        # 恢复玩家状态
        player_data = level_data['player']
        level.player.lv = game.player_lv
        level.player.update_stats()
        level.player.hp = min(player_data['hp'], level.player.max_hp)
        level.player.mp = min(player_data['mp'], level.player.max_mp)
        level.player.rect.x, level.player.rect.y = player_data['position']

        # 清除现有敌人
        level.enemies.empty()
        level.enemymagic.empty()

        # 重新创建敌人
        for enemy_data in level_data['enemies']:
            enemy_type = enemy_data['type']
            enemy = None
            
            # 根据类型创建对应的敌人
            if enemy_type == 'DarkWolf':
                enemy = DarkWolf(level)
            elif enemy_type == 'Snake':
                enemy = Snake(level)
            elif enemy_type == 'Flower':
                enemy = Flower(level)
            elif enemy_type == 'Box':
                enemy = Box(level)
            elif enemy_type == 'Warrant':
                enemy = Warrant(level)
            elif enemy_type == 'Dragon':
                enemy = Dragon(level)
                level.boss = enemy
            elif enemy_type == 'Firegiant':
                enemy = Firegiant(level)
                level.boss = enemy

            if enemy:
                enemy.hp = enemy_data['hp']
                enemy.rect.x, enemy.rect.y = enemy_data['position']
                enemy.active = enemy_data['active']
                level.enemies.add(enemy)

    return True

def clear_game(slot_num, game):
    save_path = os.path.join(save_folder, f'save{slot_num}.json')
    if os.path.exists(save_path):  # 确保文件存在
        os.remove(save_path)  # 删除文件
        return True
    else:
        return False

def get_save_info(slot_num):
    """获取存档信息"""
    save_path = os.path.join(save_folder, f'save{slot_num}.json')
    
    if not os.path.exists(save_path):
        return None
        
    with open(save_path, 'r') as f:
        save_data = json.load(f)
        
    return save_data['date']

