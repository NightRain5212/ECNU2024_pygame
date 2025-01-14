import pygame as pg
import random
import math
from lib import MOD
from settings import *
from lib.monsters.life_bar import lifebar

class DarkWolf(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.name="DarkWolf"
        self.game = game
        self.statussheet = {
            "attack": WOLF_ATK_PATH,
            "walk": WOLF_WALK_PATH
        }
        self.lstatusani = {"walk": [], "attack": []}
        self.rstatusani = {"walk": [], "attack": []}
        self.framenums = {"walk": 8, "attack": 8}
        self.load_frames()
        self.cf = 0  # 当前帧
        self.lt = pg.time.get_ticks()  # 上次更新时间
        self.status = "walk"
        
        # 初始化位置和方向
        self.image = self.lstatusani[self.status][self.cf]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(100, 700), random.randint(100, 500))
        self.direction = 1





        # 状态属性
        self.hp = WOLF_MAXHP
        self.max_hp = WOLF_MAXHP
        self.atk =WOLF_ATK
        self.speedx = WOLF_SPEED
        self.vy = 0
        self.vx = self.speedx
        self.isalive = True
        self.onground = False
        
        # 攻击相关
        self.attack_radius = WOLF_ATTACK_RANGE # 攻击范围
        self.detect_range  =WOLF_NOTICE_RANGE  # 发现玩家范围
        self.min_distance = WOLF_MIN_DISTANCE
        self.can_attack = True
        self.attack_cooldown = WOLF_ATTACK_COOLDOWN  # 攻击冷却时间(毫秒)
        self.last_attack = 0
        self.mask = pg.mask.from_surface(self.image)
        self.anim_finished = True
        self.active = True

        # 初始化血条
        self.blood = lifebar(self)

        #火球精灵被放在外面的精灵组enemymagic和里面的fire_manager
        self.fire_manager=pg.sprite.Group()


    def load_frames(self):
        # for status,path in self.statussheet.items():
        #     sheet = pg.image.load(path).convert_alpha()
        #     if status == "attack":
        #         sheet = pg.transform.scale(sheet,(64*4,64*2))
        #     else:
        #         sheet = pg.transform.scale(sheet,(64*4,64*4))
        #     width = sheet.get_width()
        #     height = sheet.get_height()
        #     num = self.framenums[status]
        #     wpf = width // 4
        #     hpf = height // 4
        #     for i in range(num):
        #         x = i % 4 * wpf
        #         y = i // 4 * hpf
        #         img = sheet.subsurface(pg.Rect(x,y,wpf,hpf))
        #         img.set_colorkey((0,0,0))
        #         self.lstatusani[status].append(img)
        #         self.rstatusani[status].append(pg.transform.flip(img,True,False))
        for i in range(16):
            sheet = pg.image.load(WOLF_WALK_PATH).convert_alpha()
            sheet = pg.transform.scale(sheet,(64*4,64*4))
            width = sheet.get_width()
            height = sheet.get_height()
            wpf = width // 4
            hpf = height // 4
            for i in range(16):
                x = i % 4 * wpf
                y = i // 4 * hpf
                img = sheet.subsurface(pg.Rect(x,y,wpf,hpf))
                img.set_colorkey((0,0,0))
                if i < 8:
                    self.lstatusani["walk"].append(img)
                    self.rstatusani["walk"].append(pg.transform.flip(img,True,False))
                else:
                    self.lstatusani["attack"].append(img)
                    self.rstatusani["attack"].append(pg.transform.flip(img,True,False))
            
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
        if self.direction==-1:
            self.image = self.lstatusani[self.status][self.cf]
        else:
            self.image = self.rstatusani[self.status][self.cf]
        self.mask = pg.mask.from_surface(self.image)
        self.game.screen.blit(self.image,self.rect)
    

    def attack_player(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack >= self.attack_cooldown:
            fireball = Fire(self)  #休战期一过，马上就初始化一个火球
            self.fire_manager.add(fireball)
            self.game.enemymagic.add(fireball)
            fireball.direction = self.direction
            fireball.active = True #可以被绘画
            self.last_attack = current_time
            self.status = "attack"
            self.anim_finished = False

    def throw_garbage(self):
        self.game.garbage_bin.add(self)
        self.game.garbage_bin.add(self.blood)

    
    def update(self):
        if self.hp<=0:
                self.throw_garbage()
                return
        dist = MOD.check_player_distance(self)
        if dist < self.detect_range:
            MOD.update_position(self)
        if dist <= self.detect_range:
            self.attack_player()
            self.status = "attack"
            self.anim_finished = False

        # 状态机逻辑
        if self.anim_finished:
            self.status = "walk"
        self.update_animation()
        # 更新血条
        #火球依赖某一个精灵族更新
        self.blood.update()
        self.fire_manager.update()

class Fire(pg.sprite.Sprite):
    def __init__(self, monster):
        super().__init__()
        self.framenums = 6
        self.monster = monster
        self.load()
        self.fireframe = 0  # 火焰动画当前帧数
        self.lt = pg.time.get_ticks()
        self.active = False
        self.rect = pg.Rect(0, 0, 50, 50)
        self.image = self.statusani["L_attack"][self.fireframe]
        self.mask = pg.mask.from_surface(self.image)
        self.direction = self.monster.direction
        self.lifetime = WOLF_FIRE_LIFETIME
        self.rect.center = self.monster.rect.center
        self.born_time = pg.time.get_ticks()
        self.atk = WOLF_FIRE_ATK
        self.speed = WOLF_FIRE_SPEED
        self.vy = 0
        self.vx = self.speed
        self.game = self.monster.game


    def load(self):
        sheetpath = WOLF_FIRE_PATH
        sheet = pg.image.load(sheetpath).convert_alpha()
        sheet = pg.transform.scale(sheet, (50 * 3, 50 * 2))
        self.statusani = {"L_attack":[],"R_attack":[]}
        for i in range(6):
            x = i % 3 * 50
            y = i // 3 * 50
            img = sheet.subsurface(x, y, 50, 50)
            self.statusani["L_attack"].append(img)
            self.statusani["R_attack"].append(pg.transform.flip(img, True, False))

    def update_animation(self):
        ct = pg.time.get_ticks()
        duration = 40
        if ct - self.lt > duration:
            fireframe = self.fireframe % 6
            if self.direction==-1:
                self.image = self.statusani["R_attack"][fireframe]
            else:
                self.image = self.statusani["L_attack"][fireframe]
            self.fireframe += 1
            self.mask = pg.mask.from_surface(self.image)
            if self.fireframe == 24:  # 攻击结束
                self.active = False #不再可见
                self.fireframe = 0
                self.monster.movecode = True
                self.monster.lastattack = pg.time.get_ticks()
                self.monster.anim_finished = True

            self.lt = ct
        #self.game.screen.blit(self.image,self.rect),这会被遮盖

    def kill(self):
        self.isalive = False
        self.active = False
        self.monster.fire_manager.remove(self)

        super().kill()

    def update_position(self):
        if self.direction==-1:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
    def check_player_collision(self):
        if pg.sprite.collide_mask(self,self.game.player):
            self.game.player.hp -= self.atk
            self.game.player.play_hurt_sound()
            self.kill()

    def update(self):

        if self.active: 
            if pg.time.get_ticks() - self.born_time > self.lifetime:
                self.kill()

                return#超过存活时间直接销
            self.update_animation()
            self.update_position()
            self.check_player_collision()

