import pygame as pg
from settings import *
import sys
import csv
from lib import tiles
import os
import math
#存放通用函数
def get_screen():
    return pg.display.get_surface()#获取窗口对象，pygame中始终只有一个窗口
#给定位置绘制文本
def draw_text( text, font, text_color, text_size,x, y):
    # font是字体类型(文件地址）,text是文本字符串，xy是文本左上角坐标
    FONTfont = pg.font.Font(font, text_size)
    SCREEN=get_screen()
    IMG = FONTfont.render(text, True, text_color)  # 将文本text渲染成图像
    SCREEN.blit(IMG, (x, y))
#按钮类
class BUTTON:
    def __init__(self,x,y,image):
        self.SCREEN=get_screen()
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)#左上角坐标
        self.clicked=False#判断图标状态
    #画按钮
    def draw(self):
        self.SCREEN.blit(self.image,(self.rect.x,self.rect.y))#xy是图片左上角坐标
    #检测按钮是否被有效点击
    def Active(self,pos=None):
        action=False
        if pos==None:
            pos=pg.mouse.get_pos()
        if self.rect.collidepoint(pos):#检查pos是否在矩形区域之内
            if pg.mouse.get_pressed()[0]==1 and self.clicked==False:#get_pressed()返回[0,0,0]即鼠标左中右是否按下
                action=True
                self.clicked=True
        if pg.mouse.get_pressed()[0]==0:
            self.clicked = False
        return action
    def Active1(self):
        action=False
        pos=pg.mouse.get_pos()
        if self.rect.collidepoint(pos) and pg.mouse.get_pressed()[0]==1 :#检查pos是否在矩形区域之内
            action=True#get_pressed()返回[0,0,0]即鼠标左中右是否按下
        self.clicked = False
        return action

#退出游戏
def QUIT():
    pg.mixer.music.stop()
    pg.quit()
    sys.exit()
#加载地图种子
def load_seed(Level):
    seed = [[-1] * COL for row in range(ROW)]
    filename = f"mapseed/level{Level}_seed.csv"

    # 如果文件存在，读取文件
    if os.path.exists(filename):
        with open(filename, "r", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for y, row in enumerate(reader):
                for x, tile in enumerate(row):
                    seed[y][x] = int(tile)
    else:
        # 如果文件不存在，创建一个新的种子并保存
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # 在这里生成一个默认的种子，比如填充为0或者随机数等
            for row in seed:
                writer.writerow(row)

    return seed
#加载世界通用瓷砖图片组
def load_world_usualpic_tileslist():
    world_img_tiles = []
    for i in range(TILE_TYPES):
        pic = pg.image.load(tiles.TILES[i]["image"]).convert_alpha()
        pic = pg.transform.scale(pic, (tiles.TILES[i]["size"][0],tiles.TILES[i]["size"][1]))
        world_img_tiles.append(pic)
    return world_img_tiles
#获取关卡地图背景(只有每一帧）
def load_level_map(level):
    background_list=[]
    if level==1:
        background_image1 = pg.image.load(LEVEL1_BACKGROUND1).convert()
        background_image2 = pg.image.load(LEVEL1_BACKGROUND2).convert_alpha()
        background_image1 = pg.transform.scale(background_image1, (WIDTH, HEIGTH))
        background_image2 = pg.transform.scale(background_image2, (WIDTH, HEIGTH//2))
        background_list.append(background_image1)
        background_list.append(background_image2)
    elif level==2:
        background_image1 = pg.image.load(LEVEL2_BACKGROUND1).convert_alpha()
        background_image2 = pg.image.load(LEVEL2_BACKGROUND2).convert_alpha()
        background_image1 = pg.transform.scale(background_image1, (WIDTH*3, HEIGTH))
        background_image2 = pg.transform.scale(background_image2, (WIDTH, HEIGTH))
        background_list.append(background_image1)
        background_list.append(background_image2)
    elif level==3:
        background_image1 = pg.image.load(LEVEL3_BACKGROUND1).convert_alpha()
        background_image2 = pg.image.load(LEVEL3_BACKGROUND2).convert_alpha()
        background_image3 = pg.image.load(LEVEL3_BACKGROUND3).convert_alpha()
        background_image1 = pg.transform.scale(background_image1, (WIDTH, HEIGTH))
        background_image2 = pg.transform.scale(background_image2, (WIDTH*3, HEIGTH))
        background_image3 = pg.transform.scale(background_image3, (WIDTH, HEIGTH))
        background_list.append(background_image1)
        background_list.append(background_image2)
        background_list.append(background_image3)
    elif level==4:
        background_image1 = pg.image.load(LEVEL4_BACKGROUND1).convert_alpha()
        background_image2 = pg.image.load(LEVEL4_BACKGROUND2).convert_alpha()
        background_image3 = pg.image.load(LEVEL4_BACKGROUND3).convert_alpha()
        background_image1 = pg.transform.scale(background_image1, (WIDTH*2, HEIGTH))
        background_image2 = pg.transform.scale(background_image2, (WIDTH*2, HEIGTH))
        background_image3 = pg.transform.scale(background_image3, (WIDTH*2.9, HEIGTH))
        background_list.append(background_image1)
        background_list.append(background_image2)
        background_list.append(background_image3)
    elif level==5:
        background_image = pg.image.load(LEVEL5_BACKGROUND).convert_alpha()
        background_image = pg.transform.scale(background_image, (5500, HEIGTH))
        background_list.append(background_image)
    return background_list
#传入屏幕和背景图列表，画图
def draw_background(level,background_list,screen,scroll):
    if level == 1:
        for x in range(10):
            screen.blit(background_list[0], (x * WIDTH+scroll, 0))
            screen.blit(background_list[1], (x * WIDTH+scroll, HEIGTH // 2))
    elif level==2:
        screen.blit(background_list[0], (scroll, 0))
        for x in range(5):
            screen.blit(background_list[1], (x * WIDTH+scroll+3*WIDTH, 0))
    elif level==3:
        for x in range(4):
            screen.blit(background_list[0], (x * WIDTH+scroll, 0))
        screen.blit(background_list[1], (scroll+4*WIDTH, 0))
    elif level==4:
        screen.blit(background_list[0], (scroll, 0))
        screen.blit(background_list[1], (2*WIDTH+scroll, 0))
        screen.blit(background_list[2], (WIDTH*4+scroll, 0))
    elif level == 5:
        screen.blit(background_list[0], (scroll ,0))
        screen.blit(background_list[0], (scroll+5500, 0))
#处理音乐
def playbackmusic(type):
    pg.mixer_music.load(backmusics[type])
    pg.mixer_music.play(loops=-1)#无限播放,
    pg.mixer.music.set_volume(1.0)#设置音量为50%

def check_tile_collision(entity, tiles, dx, dy):
    for tile in tiles:
        if tile.rect.colliderect(entity.rect.x + dx, entity.rect.y, entity.rect.width, entity.rect.height):
            dx = 0
        elif tile.rect.colliderect(entity.rect.x, entity.rect.y + dy, entity.rect.width, entity.rect.height):
            if dy < 0:
                dy = tile.rect.bottom - entity.rect.top
            elif dy >= 0:
                dy = tile.rect.top - entity.rect.bottom
                entity.isonground = True
    return dx, dy

def apply_gravity(entity, gravity):
    if not entity.isonground:
        entity.vy += gravity
    # 最大速度限制
    if entity.vy > 10:
        entity.vy = 10

def set_position(entity, x, y):
    entity.rect.x = x
    entity.rect.y = y

# 检测碰撞（考虑方向）
def Check_Tile_Collision(entity, tiles, dx, dy):
    for tile in tiles:
        if tile.rect.colliderect(entity.rect.x + dx, entity.rect.y-1, entity.rect.width, entity.rect.height):
           if entity.onground ==True:
                entity.vy=-15#水平上撞到东西
                entity.onground=False#直接跳起来
           else:dx=0 #直到坠落
        elif tile.rect.colliderect(entity.rect.x, entity.rect.y + dy, entity.rect.width, entity.rect.height):
            if dy < 0:
                dy = tile.rect.bottom - entity.rect.top
            elif dy >= 0:#向下
                dy = tile.rect.top - entity.rect.bottom
                entity.onground = True #碰到地上，直接true
    return dx, dy #若是没碰到，就是原有加速度论处

# 检测碰撞（不考虑方向）
def Check_Tile_Collision_no_direction(entity, tiles):
    for tile in tiles:
        if tile.rect.colliderect(entity.rect):
            return True
    return False


def Apply_gravity(entity, gravity): #如果，碰到地上，才会变成onground=True
    if not entity.onground:
        entity.vy += gravity #更新速度

# 播放点击音效
def play_click_sound():
    click_sound = pg.mixer.Sound(CLICK_SOUND)
    click_sound.play()

def play_levelup_sound():
    levelup_sound = pg.mixer.Sound(LEVELUP_SOUND)
    levelup_sound.play()

# 背景动画
class Background:
    def __init__(self):
        self.images = []
        self.framenums = 147
        self.cf = 0
        self.timer = pg.time.get_ticks()
        for i in range(1, 148):
            filepath = "src/img/StartMenu/{}.png".format(i)
            img = pg.image.load(filepath).convert_alpha()
            img = pg.transform.scale(img, (WIDTH, HEIGTH))
            self.images.append(img)

        self.image = self.images[self.cf]

    def play_animation(self, screen):
        duration = 2000
        current_time = pg.time.get_ticks()
        if current_time - self.timer >= duration:
            self.cf = (self.cf + 1) % self.framenums
            self.image = self.images[self.cf]
            screen.blit(self.image, (0, 0))


def check_player_distance(entity):
    player = entity.game.player
    dx = player.rect.centerx - entity.rect.centerx
    dy = player.rect.centery - entity.rect.centery
    dist = math.sqrt(dx * dx + dy * dy)
    # entity.facing_left = dx < 0
    return dist

def is_detect(entity):
    dist = check_player_distance(entity)
    return dist < entity.detect_range

def target(entity):
        # 在水平方向上追踪,update_position中遇到障碍自动爬坡
        if entity.game.player.rect.x < entity.rect.x:
            entity.direction = -1
        else:
            entity.direction = 1
        entity.vx = entity.direction * entity.speedx
def update_position(entity):
    if is_detect(entity): #是否检测到
        target(entity)
        entity.vx = entity.direction * entity.speedx

    elif entity.anim_finished: #没有检测到，但是已经攻击结束
        entity.status="walk"



    Apply_gravity(entity, GRAVITY)
    # 先根据重力来解决下落和上升
    dx = entity.vx
    dy = entity.vy
    dx, dy = Check_Tile_Collision(entity, entity.game.obstacles, dx, dy)  # 阻塞要跳起来的逻辑已经在
    entity.rect.x += dx
    entity.rect.y += dy

def check_object_collision(entity,objects):
    for obj in objects:
        if entity.rect.colliderect(obj.rect):
            return True
    return False

def check_fraction_collision(entity,fractions):
    for fraction in fractions:
        if entity.rect.colliderect(fraction.rect):
            return fraction
    return False

def ensure_entity_in_screen(entity):
    if entity.rect.y <= 0:
        entity.rect.y = 0
    if entity.rect.left <=0:
        entity.rect.left = 0 
