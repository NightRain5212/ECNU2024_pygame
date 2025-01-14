from random import randint
import random
from lib import MOD
import pygame as pg
from settings import *
from  math import sqrt
from lib.monsters.life_bar import lifebar
#小怪的出现方式，从天空降落吧
class Flower(pg.sprite.Sprite):#继承自sprite
    def __init__(self,game):#实例化这个小怪必须知道在哪个关卡里面,game就是关卡
        # 获取游戏状态
        self.game = game
        pg.sprite.Sprite.__init__(self)#在C++中，继承类在初始化列表中，也需要，对基类进行初始化
       #基本属性FLOWER_MAXHP = 50


        self.hp = FLOWER_MAXHP   # 生命值
        self.max_hp = FLOWER_MAXHP   # 最大生命值
        self.atk =FLOWER_ATK  # 攻击力

        # 随机决定小怪的位置
        x = random.randint(0, 1536)
        y=randint(200,300)#从高处下落，随机会落到某个瓷砖上

        self.rect = pg.Rect(x,y, 64, 64)
        # 移动方向

        if self.game.player.rect.x < x: #在玩家右边
            self.direction = -1
        else:       #在玩家左边
            self.direction = 1

        self.speedx =FLOWER_SPEED

        #一些状态
        self.anim_finished=True
        self.movecode = True
        self.active=True
        self.status="walk"
        self.is_angry = False
        self.onground=False
        #一些子类
        self.mist=purplemist(self)
        game.enemymagic.add(self.mist) #成功添加到了enemymagic精灵族
        self.water = None
        self.obstacles =self.game.obstacles  # 前向声明
        self.blood=lifebar(self)

        #有关帧
        self.load()  # 导入图片
        self.flowerframe = 0#寄生花的帧数
        self.lt = pg.time.get_ticks()
        self.lastattack = self.lt
        self.image = self.frames[self.flowerframe ]
        

        #控制运动的参数
        self.vx=self.direction*self.speedx
        self.vy=0
        self.accelate_y=GRAVITY
        self.attack_range = FLOWER_ATTACK_RANGE
        self.detect_range = FLOWER_DETECT_RANGE
        self.attack_cooldown = FLOWER_ATTACK_COOLDOWN

    def load(self):

        sheetpath= FLOWER_PATH
        self.frames=[]

        sheet = pg.image.load(sheetpath).convert_alpha()
        sheet = pg.transform.scale(sheet, (64 * 3, 64 * 3))
        for i in range(9):
                    x = i % 3 * 64
                    y = i // 3 * 64
                    img = sheet.subsurface(x, y, 64, 64)
                    self.frames.append(img)


    def flowerdance(self):#update
        # 更新帧
        ct = pg.time.get_ticks()
        duration = 50    #每帧的间隔100ms
        if ct - self.lt > duration and self.anim_finished ==True: #如果那个紫雾效果没有播放完成，也不能如愿
            self.image = self.frames[self.flowerframe ]
            self.flowerframe=(self.flowerframe+1)%9
            self.lt = ct


    def throw_garbage(self):
        self.game.garbage_bin.add(self)
        self.game.garbage_bin.add(self.mist)


    def update(self):
        if self.hp <= 0 and self.anim_finished:
            self.throw_garbage()
            return

        dist = MOD.check_player_distance(self)
        if self.movecode:
            if dist < self.detect_range:
                MOD.update_position(self)

        dist = MOD.check_player_distance(self)

        if self.anim_finished==True:  # 攻击动画还没有完结时，任何状态都无法得到更新self.anim_finished==True
            if dist <= self.attack_range:  #玩家的跳跃会改变dist的值
                self.attack()
            else:
                self.status = "walk"

        if self.status=="walk":
                self.flowerdance()

        if self.status=="attack":
                self.mist.update()
        # 更新血条
        self.blood.update()
        self.mask = pg.mask.from_surface(self.image)
        MOD.ensure_entity_in_screen(self)

    def attack(self):

        ct=pg.time.get_ticks()#进入警戒范围,不是每次进入警戒范围都会触发攻击，
        if ct-self.lastattack>self.attack_cooldown:
                self.anim_finished=False
                self.mist.active = True
                self.status="attack"
                self.game.player.hp-=self.atk





class purplemist(pg.sprite.Sprite):
    def __init__(self,monster):
        self.is_dead=False
        super().__init__()
        self.framenum=48
        self.monster=monster
        self.load()
        self.purpleframe = 0
        self.lt=pg.time.get_ticks()
        self.active=False
        self.rect= pg.Rect(0,0, 256, 256)
        self.atk = self.monster.atk/100

    def load(self):
        self.statussheet = {
            "attack1": FLOWER_ATTACK1_PATH,
            "attack2": FLOWER_ATTACK2_PATH,
            "attack3": FLOWER_ATTACK3_PATH}
        # 状态帧表
        self.frames= []
        for status, sheetpath in self.statussheet.items():
            sheet = pg.image.load(sheetpath).convert_alpha()
            sheet = pg.transform.scale(sheet, (256 * 4, 256 * 4))
            for i in range(16):
                    x = i % 4 * 256
                    y = i // 4 * 256
                    img = sheet.subsurface(x, y, 256, 256)
                    self.frames.append(img)

    def check_attack(self):
         player = self.monster.game.player
         if self.rect.colliderect(player):
              player.hp -= self.atk

    def update(self):

        self.rect.center=self.monster.rect.center

        ct=pg.time.get_ticks()
        if ct-self.lt>60:  # 进入有条件，因此到了48帧就
            self.image = self.frames[self.purpleframe]
            self.lt = ct
            self.purpleframe+=1

        if self.purpleframe ==self.framenum:
             self.monster.anim_finished = True# 最后一帧，
             self.purpleframe = 0
             self.active = False
             self.monster.status="walk"

             self.monster.lastattack = pg.time.get_ticks()
        self.check_attack()
