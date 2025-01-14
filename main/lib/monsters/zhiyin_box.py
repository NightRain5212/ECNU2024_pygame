from settings import *
import pygame.sprite

import lib.menus.StartMenu
import random
from lib.monsters.life_bar import  lifebar
from lib import MOD
from  math import sqrt
class Box(pygame.sprite.Sprite):#继承自sprite

    #这里面的movecode设置为1，2，3：1是开箱，2是行走，3是攻击
    def __init__(self,game):
        # 获取游戏状态
        self.game = game
        pg.sprite.Sprite.__init__(self)
       #初始化小怪精灵的属性"""
        self.hp = 100# 生命值
        self.max_hp = ZHIYINBOX_MAXHP # 最大生命值
        self.atk = ZHIYINBOX_ATK  # 攻击力
        self.speedx=ZHIYINBOX_SPEED


        self.box_position=(1400,57.6) #假设宝箱设在此处

        self.rect=self.rect = pg.Rect(1464,900-64-200,64,64)

        #决定初始速度，方向
        if self.game.player.rect.x< 1464:
            self.direction=-1

        else:
            self.direction=1
        #有关于帧
        self.hen_frame=0
        self.call_frame=0
        self.load()
        self.lt=pg.time.get_ticks()
        self.lastattack=self.lt
        #一些状态
        self.onground=False
        self.active=False
        self.movecode=False#初始状态是箱子动画播放
        self.status="open"
        self.anim_finished=False
        # 一些子类
        self.box = box(self) #动画播完之后，自动，可以
        game.enemymagic.add(self.box)  # 成功添加到了enemymagic精灵组
        self.water = self.game.water
        self.obstacles = self.game.obstacles  # 前向声明
        self.blood = lifebar(self)  # 血条
        #控制运动
        self.attack_range = 150
        self.detect_range = 300
        self.attack_cooldown = ZHIYINBOX_ATTACK_COOLDOWN
        self.vx=self.direction*self.speedx
        self.vy=0# 速度矢量 最开始的时候速度应该都是0，或者下坠的时候，水平速度为0
        self.accelate_y = GRAVITY  # 加速度矢量

    def load(self): # update

        self.statussheet = {
            "walk": ZHIYINBOX_WALK_PATH,
            "attack1": ZHIYINBOX_ATTACK1_PATH,
            "attack2": ZHIYINBOX_ATTACK2_PATH,
            }
        self.statusani = {"R_walk": [] ,"L_walk": [] , "L_attack": [], "R_attack": []}
        for status, sheetpath in self.statussheet.items():
            sheet = pg.image.load(sheetpath).convert_alpha()
            sheet = pg.transform.scale(sheet, (64 * 3, 64 * 3))
            if status=="walk":
                for i in range(9):
                    x=i%3*64
                    y=i//3*64
                    img = sheet.subsurface(x, y, 64, 64)
                    self.statusani["R_walk"].append(img)
                    self.statusani["L_walk"].append(pg.transform.flip(img,True,False))

            if status=="attack1" or status=="attack2":
                for i in range(9):
                    x = i % 3*64
                    y = i // 3*64
                    img = sheet.subsurface(x, y,64,64)
                    self.statusani["L_attack"].append(img)
                    self.statusani["R_attack"].append(pg.transform.flip(img,True,False))
    def Call(self):
        ct=pg.time.get_ticks()
        duration=100
        if ct-self.lt>duration:
            #print("帧数",self.call_frame)
            if self.direction==1:
                self.image=self.statusani["R_attack"][self.call_frame]

            else:
                self.image = self.statusani["L_attack"][self.call_frame]

            self.lt=ct
            self.call_frame+=1
        if self.call_frame==18: #播放结束
            self.status="walk"
            self.call_frame=0
            self.movecode=True
            self.lastattack=ct
            self.anim_finished=True #这样才能进入依照距离，重定状态

    def hendance(self):
     ct=pg.time.get_ticks()
     if ct-self.lt>200:
        if self.direction==1:
            self.image = self.statusani["L_walk"][self.hen_frame]
        else:
            self.image=self.statusani["R_walk"][self.hen_frame]
        self.hen_frame = (self.hen_frame + 1) % 9


    def attack(self):
        ct = pg.time.get_ticks()  # 进入攻击范围就可以
        if ct - self.lastattack > self.attack_cooldown:
            self.movecode = False#不再移动
            self.anim_finished = False
            self.box.active = True
            self.status = "attack"

            self.game.player.hp -= self.atk  # 攻击范围的攻击一定击中
            self.game.player.play_hurt_sound()

    def throw_garbage(self):
        self.game.garbage_bin.add(self)
        self.game.garbage_bin.add(self.blood)
        self.game.garbage_bin.add(self.box)

    def update(self): #在初始化的前32次必须，播放箱子动画
        if self.hp <= 0:
            self.throw_garbage()
            return

        dist = MOD.check_player_distance(self)

        if self.anim_finished:  # 攻击动画还没有完结时，任何状态都无法得到更新
            if dist <= self.attack_range:
                self.attack()
            else:
                self.status = "walk"

        if self.movecode:
            if dist < self.detect_range:
                MOD.update_position(self)
        #根据状态来更新动画，不适用if -elif结构，因为"open"的结束是，把状态改为walk,并且让hen变为active,否则会显示hen的image不存在
        if self.status == "open":
            self.box.update()
        if self.status =="walk":
            self.hendance()
            self.mask = pg.mask.from_surface(self.image)
        if self.status =="attack":
            self.Call()
            self.mask = pg.mask.from_surface(self.image)
        # 更新血条
        self.blood.update()
        MOD.ensure_entity_in_screen(self)




class box(pg.sprite.Sprite):
        def __init__(self, monster):
            super().__init__()

            self.monster = monster
            self.load()
            self.boxframe=0
            self.lt = pg.time.get_ticks()
            self.active =True
            self.rect = pg.Rect(1400,900-57.6-22,64, 57.6)
            self.image=self.Boxopen[self.boxframe]
        def load(self):
            self.boxes = {
                BOX_CLOSE_PATH,
                BOX_OPEN_PATH,
            }
            self.Boxopen=[]
            for sheetpath in self.boxes:
                sheet = pg.image.load(sheetpath).convert_alpha()
                sheet = pg.transform.scale(sheet, (64 * 4, 57.6 * 4))
                for i in range(16):
                        x = i % 4 * 64
                        y = i // 4 * 57.6
                        img = sheet.subsurface(x, y, 64, 57.6)
                        self.Boxopen.append(img)

        def update(self):
            ct = pg.time.get_ticks()
            duration = 100

            if ct - self.lt > duration:
                self.lt = ct
                self.image=self.Boxopen[self.boxframe]

                self.boxframe +=1
                if self.boxframe ==32:  # 攻击结束应该记录一下lastattack
                    #self.active = False  播完之后，仍然需要宝箱
                    self.boxframe = 0
                    self.monster.movecode =True
                    self.monster.status = "walk"
                    self.monster.active = True #这个马上为True,其对象必须马上安排好
                    self.monster.anim_finished=True