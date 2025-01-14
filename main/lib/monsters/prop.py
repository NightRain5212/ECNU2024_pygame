from settings import *
import pygame.sprite
import pygame as pg

class hints(pg.sprite.Sprite):#self.,box):
    def __init__(self,entity,words):
        super().__init__()
        font=pg.font.Font(None,74)
        text_color=(230,19,108)
        text=words
        self.faded_speed=5#淡入淡出速度
        #创建文字surface
        self.tempt=pg.font.Font(FONT,25)
        self.image=self.tempt.render(text,True,text_color)
        self.entity=entity
        self.rect=pg.Rect(self.entity.rect.x,self.entity.rect.y-40,80,20)
        #初始化透明度
        self.alpha=1
        self.lt=0
        self.faded_direction=1
        #帧率
        self.duration=60
        #状态
        self.active=False
    def update(self):
         #更新透明度
     ct=pg.time.get_ticks()
     if ct-self.lt>self.duration:

        self.alpha+=self.faded_direction*self.faded_speed

        if self.alpha>=255:
            self.alpha=255
            self.faded_direction=-1
        if self.alpha<=0:
            self.active=False
            return
        self.image.set_alpha(self.alpha)

class precious_box(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        #引用
        self.player=game.player
        #帧
        self.load()
        self.boxframe = 0
        self.lt = pg.time.get_ticks()
        #位置大小
        self.rect = pg.Rect(900,500, 64, 57.6)
        #子类和遮罩
        self.image = self.Boxopen[0]
        self.Hint=hints(self,"生命值增加50！")
        game.enemymagic.add(self.Hint)
        #状态
        self.First=True
        self.active=True
        self.set_off=False
    def load(self):
        self.boxes = {BOX_CLOSE_PATH,BOX_OPEN_PATH}
        self.Boxopen = []
        for sheetpath in self.boxes:
            sheet = pg.image.load(sheetpath).convert_alpha()
            sheet = pg.transform.scale(sheet, (64 * 4, 57.6 * 4))
            for i in range(16):
                x = i % 4 * 64
                y = i // 4 * 57.6
                img = sheet.subsurface(x, y, 64, 57.6)
                self.Boxopen.append(img)

    def update(self):
        if self.First:
            hits= self.rect.colliderect(self.player)
            if hits:self.set_off=True

        if self.set_off:
            self.play()
        if self.Hint.active:
            self.Hint.update()

    def play(self):
        ct = pg.time.get_ticks()
        duration = 100
        if ct - self.lt > duration:
            self.lt = ct
            self.image = self.Boxopen[self.boxframe]
            self.boxframe += 1
            if self.boxframe == 32:  # 攻击结束应该记录一下lastattack
                self.Hint.active=True
                self.boost_capcity()
                self.set_off=False
                self.First=False


    def boost_capcity(self):
        self.player.hp+=50


class Luckycloud(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        #引用
        self.player = game.player
        self.garbage_bin=game.garbage_bin
        #帧
        self.load()
        self.moneyframe = 0
        self.lt = pg.time.get_ticks()
        #位置大小
        self.rect = pg.Rect(900, 500, 64, 64)
        self.image = self.moneyrain[0]
        #子类
        self.Hint = hints(self, "大幸运！生命值增加100！")
        game.enemymagic.add(self.Hint)
        #状态
        self.set_off = False
        self.First = True
        self.active = True
        # 创建遮罩
        self.image=self.moneyrain [0]
        self.mask = pg.mask.from_surface(self.image)

    def load(self):
        sheetpath = LUCKY_RAIN_PATH
        self.moneyrain = []

        sheet = pg.image.load(sheetpath).convert_alpha()
        sheet = pg.transform.scale(sheet, (120* 4, 120 * 2))
        for i in range(8):
                x = i % 4 *120
                y = i // 4 * 120
                img = sheet.subsurface(x, y, 120,120)
                self.moneyrain.append(img)

    def update(self):
        if self.First:
            hits = self.rect.colliderect(self.player)
            if hits: self.set_off = True

        if self.set_off:
            self.play()
        if self.Hint.active:
            self.Hint.update()

    def play(self):
        ct = pg.time.get_ticks()
        duration = 200
        if ct - self.lt > duration:
            self.lt = ct
            self.image = self.moneyrain[self.moneyframe]
            self.moneyframe += 1
            print('红包帧更新到',self.moneyframe,"active",self.active)
            if self.moneyframe == 8:
                #self.garbage_bin.add(self)# 攻击结束应该记录一下lastattack
                self.Hint.active = True
                self.boost_capcity()
                self.set_off = False
                self.First = False
                self.active=False

    def boost_capcity(self):
            self.player.hp += 100
            #跳跃不好说
