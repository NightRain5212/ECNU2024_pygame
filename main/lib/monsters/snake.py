import pygame as pg
from settings import *
import math
from lib import MOD
from lib.monsters.life_bar import lifebar

class Snake(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.name="Snake"
        # 加载蛇的动画帧
        self.status = "walk"
        self.statussheet = {
            "walk": SNAKE_WALK_PATH,
            "attack": SNAKE_ATTACK_PATH
        }
        self.lstatusani = {"walk": [], "attack": []}
        self.rstatusani = {"walk": [], "attack": []}
        self.framenums = {"walk": 10, "attack": 10}
        self.load_frames()
        
        # 动画控制
        self.cf = 0  # 当前帧
        self.lt = pg.time.get_ticks()  # 上次更新时间
        self.anim_finished = True

        # 基础属性
        self.image = self.lstatusani[self.status][self.cf]
        self.rect = self.image.get_rect()
        self.rect.x = 800  # 初始位置
        self.rect.y = 400
        self.width = self.rect.width
        self.height = self.rect.height
        self.onground = False
        # 战斗属性
        self.hp = SNAKE_MAXHP
        self.max_hp = SNAKE_MAXHP
        self.atk = SNAKE_ATK
        self.active = True
        self.direction= 1
        
        # 初始化血条
        self.blood = lifebar(self)
        
        # 行为控制
        self.attack_range =SNAKE_ATTACK_RANGE
        self.detect_range = SNAKE_DETECT_RANGE
        self.attack_cooldown =SNAKE_ATTACK_COOLDOWN # 攻击冷却时间(ms)
        self.last_attack = 0
        self.speedx = SNAKE_SPEED
        self.vx = 0
        self.vy = 0
        # 创建遮罩
        self.mask = pg.mask.from_surface(self.image)

    def load_frames(self):
        for status, sheetpath in self.statussheet.items():
            sheet = pg.image.load(sheetpath).convert_alpha()
            sheet = pg.transform.scale(sheet, (210 * 2,64 * 5))
            width = sheet.get_width()
            height = sheet.get_height()
            num = self.framenums[status]
            wpf = width // 2
            hpf = height // 5
            for i in range(num):
                x = i % 2 * wpf
                y = i // 2 * hpf
                img = sheet.subsurface(x, y, wpf, hpf)
                self.lstatusani[status].append(img)
                self.rstatusani[status].append(pg.transform.flip(img, True, False))


    def update_animation(self):
        duration = 100
        ct = pg.time.get_ticks()
        
        if ct - self.lt > duration:
            self.cf = (self.cf + 1) % len(self.lstatusani[self.status])
            if self.cf >= len(self.lstatusani[self.status]):
                self.cf = 0
            if self.cf == 0:
                self.anim_finished = True
            else:
                self.anim_finished = False
            self.lt = ct
        
        self.image = self.lstatusani[self.status][self.cf]
        if self.direction==1: #朝右
            self.image = self.rstatusani[self.status][self.cf]
        
        self.game.screen.blit(self.image, self.rect)

        self.mask = pg.mask.from_surface(self.image) #更新位掩码




    def attack_player(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack >= self.attack_cooldown:
            self.status = "attack"
            self.anim_finished = False
            self.last_attack = current_time
            
            # 检测攻击是否命中
            if MOD.check_player_distance(self) <= self.attack_range:
                self.game.player.hp -= self.atk
                self.game.player.play_hurt_sound()

    def throw_garbage(self):
        self.game.garbage_bin.add(self)
        self.game.garbage_bin.add(self.blood)
    def setposition(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if  self.hp <= 0:
                self.throw_garbage()
                return
        dist = MOD.check_player_distance(self)
        # if dist < self.detect_range:
        MOD.update_position(self)

        # 状态机逻辑
        if self.anim_finished: #在同时攻击时无法给出攻击
            if dist <= self.attack_range:
                self.attack_player()
            else:
                self.status = "walk"
        self.blood.update()
        self.update_animation()
        MOD.ensure_entity_in_screen(self)
        
