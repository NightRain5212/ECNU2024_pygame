import os
import pygame as pg

from settings import *
# 假设素材路径
ASSETS_DIR = TILES_PATH

TILES = {
    0: {"name": "glass", "type": "decoration", "size": (30, 30),  "image": r"src/img/Map/level/glass.png"},
    1: {"name": "wall9", "type": "decoration", "size": (30, 30),  "image": r"src/img/Map/level/wall9.png"},
    2: {"name": "redglass2", "type": "decoration", "size": (30, 30),  "image": r"src/img/Map/level/redglass2.png"},
    3: {"name": "redglass3", "type": "decoration", "size": (30, 30),  "image": r"src/img/Map/level/redglass3.png"},
    4: {"name": "wall10", "type": "decoration", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall10.png')},
    5: {"name": "twowheels", "type": "decoration", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'twowheels.png')},
    6: {"name": "badMoon", "type": "decoration", "size": (150, 150),  "image": os.path.join(ASSETS_DIR, 'badMoon.png')},
    7: {"name": "bigtree (1)", "type": "decoration", "size": (60, 120),  "image": os.path.join(ASSETS_DIR, 'bigtree (1).png')},
    8: {"name": "bigtree (2)", "type": "decoration", "size": (60, 120),  "image": os.path.join(ASSETS_DIR, 'bigtree (2).png')},
    9: {"name": "bigtree (3)", "type": "decoration", "size": (60, 120),  "image": os.path.join(ASSETS_DIR, 'bigtree (3).png')},
    10: {"name": "Bones (1)", "type": "decoration", "size": (30, 90),  "image": os.path.join(ASSETS_DIR, 'Bones_shadow (1).png')},
    11: {"name": "Bones (2)", "type": "decoration", "size": (30, 90),  "image": os.path.join(ASSETS_DIR, 'Bones_shadow (2).png')},
    12: {"name": "Bones (3)", "type": "decoration", "size": (120, 50),  "image": os.path.join(ASSETS_DIR, 'Bones_shadow (3).png')},
    13: {"name": "Bones (4)", "type": "decoration", "size": (60, 90),  "image": os.path.join(ASSETS_DIR, 'Bones_shadow (4).png')},
    14: {"name": "bucket", "type": "decoration", "size": (60, 90),  "image": os.path.join(ASSETS_DIR, 'bucket.png')},
    15: {"name": "Deadtr", "type": "decoration", "size": (30, 60),  "image": os.path.join(ASSETS_DIR, 'Dead_tree.png')},
    16: {"name": "Pointer1", "type": "decoration", "size": (30, 90),  "image": os.path.join(ASSETS_DIR, 'Pointer1.png')},
    17: {"name": "wall7", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall7.png')},
    18: {"name": "wall8", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall8.png')},
    19: {"name": "tower", "type": "decoration", "size": (30, 120),  "image": os.path.join(ASSETS_DIR, 'tower.png')},
    20: {"name": "tree (1)", "type": "decoration", "size": (30, 90),  "image": os.path.join(ASSETS_DIR, 'tree (1).png')},
    21: {"name": "tree (2)", "type": "decoration", "size": (30, 90),  "image": os.path.join(ASSETS_DIR, 'tree (2).png')},
    22: {"name": "tree (3)", "type": "decoration", "size": (30, 90),  "image": os.path.join(ASSETS_DIR, 'tree (3).png')},
    23: {"name": "wall11", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall11.png')},
    24: {"name": "tile5", "type": "impassable", "size": (30, 30) , "image": os.path.join(ASSETS_DIR, 'tile5.png')},
    25: {"name": "wall15", "type": "impassable", "size": (30, 30) , "image": os.path.join(ASSETS_DIR, 'wall15.png')},
    26: {"name": "wall12", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall12.png')},
    27: {"name": "Thorn", "type": "impassable", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'Thorn.png')},
    28: {"name": "Tile1", "type": "impassable", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'Tile1.png')},
    29: {"name": "tile2", "type": "impassable", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'tile2.png')},
    30: {"name": "tile3", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'tile3.png')},
    31: {"name": "Scull", "type": "impassable", "size": (60, 90),  "image": os.path.join(ASSETS_DIR, 'Scull.png')},
    32: {"name": "tille4", "type": "impassable", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'tille4.png')},
    33: {"name": "wall13", "type": "impassable", "size": (30, 30) , "image": os.path.join(ASSETS_DIR, 'wall13.png')},
    34: {"name": "wall14", "type": "impassable", "size": (30, 30) , "image": os.path.join(ASSETS_DIR, 'wall14.png')},
    35: {"name": "stone", "type": "impassable", "size": (30, 60) , "image": os.path.join(ASSETS_DIR, 'stone.png')},
    36: {"name": "ladders", "type": "object", "size": (30, 30) , "image": os.path.join(ASSETS_DIR, 'ladders.png')},
    37: {"name": "ladders1", "type": "object", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'ladders1.png')},
    38: {"name": "fence", "type": "decoration", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'fence.png')},
    39: {"name": "water1", "type": "water", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'water1.png')},
    40: {"name": "water2", "type": "water", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'water2.png')},
    41: {"name": "wall1", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall1.png')},
    42: {"name": "wall2", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall2.png')},
    43: {"name": "wall3", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall3.png')},
    44: {"name": "wall4", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall4.png')},
    45: {"name": "wall5", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall5.png')},
    46: {"name": "wall6", "type": "impassable", "size": (30, 30),  "image": os.path.join(ASSETS_DIR, 'wall6.png')},
    47: {"name": "tree4", "type": "decoration", "size": (60, 90), "image": os.path.join(ASSETS_DIR, 'tree4.png')},
    48: {"name": "tree5", "type": "decoration", "size": (90, 120), "image": os.path.join(ASSETS_DIR, 'tree5.png')},
    49: {"name": "tree6", "type": "decoration", "size": (60, 120), "image": os.path.join(ASSETS_DIR, 'tree6.png')},
    50: {"name": "door", "type": "decoration", "size": (60, 90), "image": os.path.join(ASSETS_DIR, 'door.png')},
    51: {"name": "cage", "type": "decoration", "size": (60, 90), "image": os.path.join(ASSETS_DIR, 'cage.png')},
    52: {"name": "box1", "type": "object", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'box1.png')},
    53: {"name": "box2", "type": "impassable", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'box2.png')},

    54: {"name": "wolf", "type": "enemy", "size": (60, 60), "image": os.path.join(ASSETS_DIR, 'wolf.png')},
    55: {"name": "warrent", "type": "enemy", "size": (60, 60), "image": os.path.join(ASSETS_DIR, 'warrent.png')},
    56: {"name": "Fantasy", "type": "enemy", "size": (60, 90), "image": os.path.join(ASSETS_DIR, 'FantasyPurple.png')},
    57: {"name": "snake", "type": "enemy", "size": (90, 60), "image": os.path.join(ASSETS_DIR, 'Python.png')},
    58: {"name": "zhiyin", "type": "enemy", "size": (60, 60), "image": os.path.join(ASSETS_DIR, 'heaven.png')},
    59:{"name": "player", "type": "player", "size": (90, 90), "image": r"src/img/Character/imgs/Idle/Idle.png"},
    60:{"name": "dragon", "type": "enemy", "size": (90, 90), "image": os.path.join(ASSETS_DIR, 'dragon.png')},

    61:{"name": "wood", "type": "decoration", "size": (30, 30), "image": os.path.join(ASSETS_DIR, 'wood.png')},
    62:{"name": "fragment", "type": "object", "size": (60, 60), "image": os.path.join(ASSETS_DIR, 'fragment.png')},
    63: {"name": "Precious_box", "type": "prop", "size": (60, 60),"image": os.path.join(ASSETS_DIR, 'precious_box.png')},
    64: {"name": "lucky_rain", "type": "prop", "size": (120, 120), "image": os.path.join(ASSETS_DIR, 'lucky_rain.png')}}


class Tile(pg.sprite.Sprite):
    def __init__(self,x,y,image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.mask = pg.mask.from_surface(self.image)



