import pygame as pg
import sys
from lib.menus.mapmenu import Mapmenu
from settings import *
from lib import MOD
from lib.menus import chaptermenu
from lib.saves import files
from lib import help
from lib import plot

class StartMenu:
    def __init__(self,game):
        self.screen = MOD.get_screen()
        # self.background_image = pg.image.load(STARTMENU_BACKGROUND).convert()
        self.background=MOD.Background()
        self.title_font = pg.font.Font(FONT,100)
        self.text_font = pg.font.Font(FONT,60)
        self.title = self.title_font.render('Lost Stars',True,WHITE)
        self.create_bottons()
        self.mapmenu=Mapmenu()
        self.chapter=chaptermenu.Chapter(game)#将game对象传递进下一个菜单中
        self.game = game
        self.file=game.files
        self.help=help.Help()
        self.plot=plot.Plot()
    def create_bottons(self):

        #按钮颜色
        self.color_b1 = WHITE
        self.color_b2 = WHITE
        self.color_b3 = WHITE
        self.color_b4 = WHITE
        self.color_b5 = WHITE
        self.color_b6 = WHITE

        #按钮文本
        self.optionsTexts = ["Start Game","Load save","Help","Plot","Exit","MapEditor"]
        self.botton1 = self.text_font.render(self.optionsTexts[0],True,self.color_b1)
        self.botton2 = self.text_font.render(self.optionsTexts[1], True, self.color_b2)
        self.botton3 = self.text_font.render(self.optionsTexts[2], True, self.color_b3)
        self.botton4 = self.text_font.render(self.optionsTexts[3], True, self.color_b4)
        self.botton5 = self.text_font.render(self.optionsTexts[4], True, self.color_b5)
        self.botton6 = self.text_font.render(self.optionsTexts[5], True, self.color_b6)
        #按钮矩形区域
        self.rect_b1 = self.botton1.get_rect(center=(550,250))
        self.rect_b2 = self.botton2.get_rect(center=(550,350))
        self.rect_b3 = self.botton3.get_rect(center=(550,450))
        self.rect_b4 = self.botton4.get_rect(center=(550,550))
        self.rect_b5 = self.botton5.get_rect(center=(550, 650))
        self.rect_b6 = self.botton6.get_rect(center=(550, 750))

    def run(self):
        MOD.playbackmusic(0)
        while True:
            self.game.clock.tick(60)
            # 绘制背景图像
            # self.screen.blit(self.background_image, (0, 0))
            self.background.play_animation(self.screen)

            # 绘制标题
            self.screen.blit(self.title,(400,100))

            # 创建按钮
            self.screen.blit(self.botton1,self.rect_b1)
            self.screen.blit(self.botton2, self.rect_b2)
            self.screen.blit(self.botton3, self.rect_b3)
            self.screen.blit(self.botton4, self.rect_b4)
            self.screen.blit(self.botton5, self.rect_b5)
            self.screen.blit(self.botton6, self.rect_b6)
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
            if(self.menu_events()==0):
                break

    def menu_events(self):
           for event in pg.event.get():
               # 退出游戏
               if event.type == pg.QUIT:
                   MOD.QUIT()
               # 检测点击按钮
               if event.type == pg.MOUSEBUTTONDOWN:
                   MOD.play_click_sound()
                   m_pos = pg.mouse.get_pos()
                   # 开始按钮
                   if self.rect_b1.collidepoint(m_pos):
                       self.game.ispaused = False
                       self.chapter.run()
                       return 1
                   # 存档按钮
                   if self.rect_b2.collidepoint(m_pos):
                       self.game.ispaused = False
                       self.file.run()
                       return 1
                   # 帮助按钮
                   if self.rect_b3.collidepoint(m_pos):
                       self.help.run()
                       return 1
                   # 退出按钮
                   if self.rect_b4.collidepoint(m_pos):
                       self.plot.run()
                       return 1
                   if self.rect_b5.collidepoint(m_pos):
                       MOD.QUIT()
                   if self.rect_b6.collidepoint(m_pos):
                       self.mapmenu.run()
                       return 1
