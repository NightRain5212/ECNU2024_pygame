from settings import *
import pygame.sprite
from lib import MOD
import lib.menus.StartMenu
import random
from  math import sqrt
from lib.monsters.life_bar import  lifebar
class Warrant(pygame.sprite.Sprite):#继承自sprite

    def __init__(self,game):
        # 获取游戏状态
        self.game = game
        pg.sprite.Sprite.__init__(self)
       #基本属性"""
        self.hp = WARRANT_MAXHP
        self.max_hp = WARRANT_MAXHP
        self.atk =WARRANT_ATK

        self.cishu=0

       # 随机决定小怪的位置
        x = random.randint(0, 1536)
        y = random.randint(200, 300)  # 从高处下落，随机会落到某个瓷砖上
        self.rect = pg.Rect(x, y,64,181.33)
        if self.game.player.rect.x < x:  # 在玩家右边
            self.direction = -1

        else:
            self.direction = 1
        self.speedx =WARRANT_SPEED

        # 有关帧
        self.load()  # 导入图片
        self.warrentframe = 0
        self.image = self.statusani["Rwalk"][self.warrentframe]
        # 一些状态
        self.onground=False
        self.anim_finished = True
        self.movecode = True
        self.active = True
        self.status="walk"
        # 一些子类
        self.Puppet =puppet(self)
        game.enemymagic.add(self.Puppet)  # 成功添加到了enemymagic精灵族
        self.water = None
        self.obstacles = self.game.obstacles   # 前向声明
        self.blood = lifebar(self)  # 血条
        # 行为控制
        self.lt = pg.time.get_ticks()
        self.lastattack = self.lt
        self.attack_range = 150
        self.detect_range = 300
        self.attack_cooldown = WARRANT_ATTACK_COOLDOWN
        self.vx = self.direction * self.speedx
        self.vy = 0  # 小怪的水平速度不需要加速度，遇到障碍直接回头
        self.accelate_y = GRAVITY  # 水平方向上没有加速度，加速度矢量


    def load(self):#init# 导入图片

        self.statussheet = {
                "walk": WARRANT_WALK_PATH,
                "symmetry_warrent":WARRANT_SYM_PATH}
            # 状态帧表
        self.statusani = {"Rwalk": [],"Lwalk": [] ,"symmetry_warrent":[]}

        for status, sheetpath in self.statussheet.items():
            sheet = pg.image.load(sheetpath).convert_alpha()
            if status=="walk":
                sheet=pg.transform.scale(sheet,(64*5,181.33))
                for i in range(5):
                    x=i*64
                    y=i//5*181.33
                    img = sheet.subsurface(x, y, 64, 181.33)
                    self.statusani["Rwalk"].append(img)
                    self.statusani["Lwalk"].append(pg.transform.flip(img,True,False))
            if status=="symmetry_warrent":
                sheet = pg.transform.scale(sheet, (64*5,181.33))
                for i in range(5):
                    x = i * 64
                    y = i //  5 *181.33
                    img = sheet.subsurface(x, y, 64, 181.33)
                    self.statusani["symmetry_warrent"].append(img)



    def warrentdance(self):#update
        ct = pg.time.get_ticks()
        duration = 100  # 每帧的间隔100ms
        if ct - self.lt > duration:
            if self.direction == 1:

                self.image = self.statusani["Rwalk"][self.warrentframe]

            else:
                self.image = self.statusani["Lwalk"][self.warrentframe]
            self.mask = pg.mask.from_surface(self.image)  # 更新位掩码
            self.warrentframe = (self.warrentframe + 1) % 5# 一共5张帧图
            self.lt=ct

    def symmetry_dance(self):
        ct = pg.time.get_ticks()
        duration = 100  # 每帧的间隔100ms:
        if ct - self.lt > duration:

            self.image = self.statusani["symmetry_warrent"][self.warrentframe]
            self.mask = pg.mask.from_surface(self.image)  # 更新位掩码
            self.warrentframe = (self.warrentframe + 1) % 5  # 一共5张帧图
            self.lt = ct

    def attack(self):

        ct = pg.time.get_ticks() #进入攻击范围就可以
        if ct-self.lastattack  > self.attack_cooldown :
                  #开启攻击模式，需要一些开关
                  self.movecode = False
                  #self.game.player.hp -= self.atk/100
                  self.anim_finished = False
                  self.Puppet.active = True
                  self.status="attack"

                  #攻击范围的攻击一定击中
                  self.game.player.hp -= self.atk #带来一次攻击即可，不用检测攻击效果与player碰撞，因为puppet会定位住player
                  self.game.player.play_hurt_sound()


    def throw_garbage(self):
        self.game.garbage_bin.add(self)
        self.game.garbage_bin.add(self.blood)
        self.game.garbage_bin.add(self.Puppet)

    def update(self):#level1里面先update,再draw，所以，所有状态必须最先确定
        if self.hp <= 0 :#攻击动画已经完结
            self.throw_garbage()
            return

        if self.movecode:
            MOD.update_position(self)
        dist = MOD.check_player_distance(self)
        if self.anim_finished: #攻击动画还没有完结时，任何状态都无法得到更新
            if dist <= self.attack_range:
                self.attack()
            else:
                self.status = "walk"

   #根据状态来更新动画

        print(self.cishu,"次",self.status)
        self.cishu+=1
        if self.status=="walk":
            print("image应该要有")
            self.warrentdance()

        else: #攻击状态status=="attack":
            self.symmetry_dance()
            self.Puppet.update()


        # 更新血条
        self.blood.update()
        MOD.ensure_entity_in_screen(self)

class puppet(pygame.sprite.Sprite):

    def __init__(self, monster):
        super().__init__()
        self.framenums = 6
        self.monster = monster
        self.load()
        self.puppetframe = 0
        self.lt = pg.time.get_ticks()
        self.active = False
        self.rect = pg.Rect(0, 0, 64, 57.6)

    def load(self):
        statussheet = [
            PUPPET_1_PATH,
            PUPPET_2_PATH,
            ]
        # 状态帧表
        self.statusani = { "L_attack": [], "R_attack": []}

        for sheetpath in statussheet:
            sheet = pg.image.load(sheetpath).convert_alpha()
            sheet = pg.transform.scale(sheet, (64 * 4, 57.6 * 4))
            for i in range(16):
                x = i % 4 * 64
                y = i // 4 * 57.6
                img = sheet.subsurface(x, y, 64, 57.6)
                self.statusani["L_attack"].append(img)
                self.statusani["R_attack"].append(pg.transform.flip(img, True, False))
    def update(self):
        ct = pg.time.get_ticks()
        duration=100
        if ct-self.lt>duration:
            self.lt = ct
            if self.monster.rect.centerx>self.monster.game.player.rect.centerx:
                self.image=self.statusani["R_attack"][self.puppetframe]
                self.rect.right=self.monster.game.player.rect.x
                self.rect.y=self.monster.game.player.rect.y

            else:

                self.image = self.statusani["L_attack"][self.puppetframe]
                self.rect.x =self.monster.game.player.rect.right
                self.rect.y = self.monster.game.player.rect.y
            self.puppetframe+=1
            if self.puppetframe==32:
                self.puppetframe = 0
                self.active=False
                self.monster.movecode=True
                self.monster.anim_finished=True
                self.monster.lastattack=pg.time.get_ticks()
