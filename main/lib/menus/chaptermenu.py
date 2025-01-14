import pygame as pg
import sys
from lib.menus.mapmenu import Mapmenu
from settings import *
from lib import MOD
from lib.end import EndPlot
#import textwrap
class Chapter:
    def __init__(self,game):
        self.screen = MOD.get_screen()
        self.background_image = pg.image.load(STARTMENU_BACKGROUND).convert()
        self.text_font = pg.font.Font(FONT3,60)
        self.create_bottons()
        self.game=game
        self.level_Lock = game.level_Lock
        self.lock_image = pg.image.load(LOCK_PATH).convert_alpha()
        self.unlock_image = pg.image.load(UNLOCK_PATH).convert_alpha()
        self.lock_image = pg.transform.scale(self.lock_image, LOCK_SCALE)
        self.unlock_image = pg.transform.scale(self.unlock_image, UNLOCK_SCALE)
        self.error_music = pg.mixer.Sound(ERROR_SOUND)
        
    def play_error_music(self):
        self.error_music.set_volume(0.5)
        self.error_music.play()

    def create_bottons(self):

        #按钮颜色
        self.color_b1 = WHITE
        self.color_b2 = WHITE
        self.color_b3 = WHITE
        self.color_b4 = WHITE
        self.color_b5 = WHITE
        self.color_b6 = WHITE
        #按钮文本
        self.optionsTexts = ["Starry Summon","Ruins","The Abyss Lake","Intrigue","Wasteland","Epilogue"]
        self.botton1 = self.text_font.render(self.optionsTexts[0],True,self.color_b1)
        self.botton2 = self.text_font.render(self.optionsTexts[1], True, self.color_b2)
        self.botton3 = self.text_font.render(self.optionsTexts[2], True, self.color_b3)
        self.botton4 = self.text_font.render(self.optionsTexts[3], True, self.color_b4)
        self.botton5 = self.text_font.render(self.optionsTexts[4], True, self.color_b5)
        self.botton6 = self.text_font.render(self.optionsTexts[5], True, self.color_b6)
        #按钮矩形区域
        self.rect_b1 = self.botton1.get_rect(center=(800,200))
        self.rect_b2 = self.botton2.get_rect(center=(800,300))
        self.rect_b3 = self.botton3.get_rect(center=(800,400))
        self.rect_b4 = self.botton4.get_rect(center=(800,500))
        self.rect_b5 = self.botton5.get_rect(center=(800, 600))
        self.rect_b6 = self.botton5.get_rect(center=(800, 700))

    def run(self):
        Back_Button_Pic=pg.image.load(BACK_BUTTON_PATH).convert()
        Back_Button_Pic=pg.transform.scale(Back_Button_Pic, (400,100))
        Back_Button=MOD.BUTTON(20,20,Back_Button_Pic)
        while True:
            # 绘制背景图像
            self.screen.blit(self.background_image, (0, 0))

            # 创建按钮
            self.screen.blit(self.botton1,self.rect_b1)
            self.screen.blit(self.botton2, self.rect_b2)
            self.screen.blit(self.botton3, self.rect_b3)
            self.screen.blit(self.botton4, self.rect_b4)
            self.screen.blit(self.botton5, self.rect_b5)
            self.screen.blit(self.botton6, self.rect_b6)
            Back_Button.draw()
            # 绘制锁
            self.draw_lock()
            # 获取鼠标对象位置
            mouse_pos = pg.mouse.get_pos()

            # 检测鼠标悬停
            if self.rect_b1.collidepoint(mouse_pos):
                self.color_b1 = LIGHT_BLUE
            else: self.color_b1 = WHITE

            if self.rect_b2.collidepoint(mouse_pos):
                self.color_b2 = LIGHT_BLUE
            else: self.color_b2 = WHITE

            if self.rect_b3.collidepoint(mouse_pos):
                self.color_b3 = LIGHT_BLUE
            else: self.color_b3 = WHITE

            if self.rect_b4.collidepoint(mouse_pos):
                self.color_b4 = LIGHT_BLUE
            else: self.color_b4 = WHITE

            if self.rect_b5.collidepoint(mouse_pos):
                self.color_b5 = LIGHT_BLUE
            else:
                self.color_b5 = WHITE
            if self.rect_b6.collidepoint(mouse_pos):
                self.color_b6 = LIGHT_BLUE
            else:
                self.color_b6 = WHITE
            # 重新渲染字体
            self.botton1 = self.text_font.render(self.optionsTexts[0],True,self.color_b1)
            self.botton2 = self.text_font.render(self.optionsTexts[1], True, self.color_b2)
            self.botton3 = self.text_font.render(self.optionsTexts[2], True, self.color_b3)
            self.botton4 = self.text_font.render(self.optionsTexts[3], True, self.color_b4)
            self.botton5 = self.text_font.render(self.optionsTexts[4], True, self.color_b5)
            self.botton6 = self.text_font.render(self.optionsTexts[5], True, self.color_b6)
            # 更新窗口
            pg.display.update()

            # 获取事件
            if(self.menu_events(Back_Button)==0):
                break

    def plots(self):
        self.plotFont = pg.font.Font(FONT1,160)
        self.plotstexts = ["Le Saint Dragon appelle","--Really Kayle"]
        self.plot_counter = 0
        self.plot = self.plotFont.render(self.plotstexts[self.plot_counter],True,WHITE).convert_alpha() # 支持透明度
        self.plot_rect = self.plot.get_rect(center=(WIDTH//2,HEIGTH//2))
        self.plot_alpha = 0
        self.plotFadeIn = True
        self.plotFadeOut = False

    def draw_lock(self):
        self.level_Lock = self.game.level_Lock
        x = 1200
        for i in range(1, 7):
            y = 175 + (i-1)*100
            if self.level_Lock[i]:
                self.screen.blit(self.unlock_image, (x, y))
            else:
                self.screen.blit(self.lock_image, (x, y))

    def run_plot(self):
        running = True

        self.plots()

        # 等待的实现
        wait = False
        waitTime = 2000 # ms
        waitStart = 0

        while running:
            # 屏幕背景
            self.screen.fill("black")

            # 淡入淡出的实现
            if self.plotFadeIn:
                self.plot_alpha += 0.75
                if self.plot_alpha >= 255:
                    self.plot_alpha = 255
                    self.plotFadeIn = False
                    wait = True
                    waitStart = pg.time.get_ticks()

            elif wait:
                curtime = pg.time.get_ticks()
                if curtime - waitStart >= waitTime:
                    wait = False
                    self.plotFadeOut = True

            elif self.plotFadeOut:
                self.plot_alpha -= 0.75
                if self.plot_alpha <=0 :
                    self.plot_alpha = 0
                    self.plotFadeOut = False
                    self.plot_counter += 1
                    if self.plot_counter < len(self.plotstexts):
                        # 重新渲染文本
                        self.plot = self.plotFont.render(self.plotstexts[self.plot_counter],True,WHITE).convert_alpha()
                        self.plot_rect = self.plot.get_rect(center=(WIDTH//2,HEIGTH//2))
                        self.plotFadeIn = True

            # 设置透明度
            self.plot.set_alpha(self.plot_alpha)
            # 绘制到屏幕
            self.screen.blit(self.plot,self.plot_rect)
            # 更新屏幕
            pg.display.flip()

            # 退出循环
            if self.plot_counter == len(self.plotstexts) and self.plotFadeOut == False :
                running = False

    def menu_events(self,Back_Button):
           for event in pg.event.get():
               # 退出游戏
               if event.type == pg.QUIT:
                   MOD.QUIT()
               #处理按钮
               if Back_Button.Active():
                    return 0
               # 检测点击按钮
               if event.type == pg.MOUSEBUTTONDOWN:
                   MOD.play_click_sound()
                   m_pos = pg.mouse.get_pos()
                   # 开始按钮
                   if self.rect_b1.collidepoint(m_pos):
                       MOD.playbackmusic(1)
                       self.run_plot()#加载剧情动画
                       self.game.level1.run()
                       MOD.playbackmusic(0)
                       return 1
                   # 存档按钮
                   if self.rect_b2.collidepoint(m_pos):
                       if not self.level_Lock[2]:
                           self.play_error_music()
                           continue
                       self.game.level2.run()
                       return 1
                   # 帮助按钮
                   if self.rect_b3.collidepoint(m_pos):
                       if not self.level_Lock[3]:
                           self.play_error_music()
                           continue
                       self.game.level3.run()
                       return 1
                   # 退出按钮
                   if self.rect_b4.collidepoint(m_pos):
                       if not self.level_Lock[4]:
                           self.play_error_music()
                           continue
                       self.game.level4.run()
                       return 1
                   if self.rect_b5.collidepoint(m_pos):
                       if not self.level_Lock[5]:
                           self.play_error_music()
                           continue
                       self.game.level5.run()
                       return 1
                   if self.rect_b6.collidepoint(m_pos):
                        if not self.level_Lock[6]:
                           self.play_error_music()
                           continue
                        self.end = EndPlot(self.game)
                        self.end.run()
                        return 1