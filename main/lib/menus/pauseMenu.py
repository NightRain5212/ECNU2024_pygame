import pygame as pg
from settings import *
import sys
from lib import MOD


class pauseMenu:

    def __init__(self, game):
        self.screen = pg.display.get_surface()
        self.text_font = pg.font.Font(FONT, 60)
        self.text = self.text_font.render('Game Paused', True, WHITE)
        self.create_bottons()
        self.game = game
        self.background_image = pg.image.load(STARTMENU_BACKGROUND).convert()
        self.files=game.files

    def create_bottons(self):

        # 按钮颜色
        self.color_b1 = WHITE
        self.color_b2 = WHITE
        self.color_b3 = WHITE
        self.color_b4 = WHITE
        # 按钮文本
        self.optionsTexts = ["Continue", "Exit", "save","Home(no save)"]
        self.botton1 = self.text_font.render(self.optionsTexts[0], True, self.color_b1)
        self.botton2 = self.text_font.render(self.optionsTexts[1], True, self.color_b2)
        self.botton3 = self.text_font.render(self.optionsTexts[2], True, self.color_b3)
        self.botton4 = self.text_font.render(self.optionsTexts[3], True, self.color_b4)
        # 按钮位置
        self.centerpos = (self.screen.get_width() // 2 - self.text.get_width() // 2,
                          self.screen.get_height() // 2 - self.text.get_height() // 2)

        # 按钮矩形区域
        self.rect_b1 = self.botton1.get_rect(center=(self.centerpos[0] + 100, self.centerpos[1]))
        self.rect_b2 = self.botton2.get_rect(center=(self.centerpos[0] + 100, self.centerpos[1] + 100))
        self.rect_b3 = self.botton3.get_rect(center=(self.centerpos[0] + 100, self.centerpos[1] + 200))
        self.rect_b4 = self.botton4.get_rect(center=(self.centerpos[0] + 100, self.centerpos[1] + 300))

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.text, (self.centerpos[0], self.centerpos[1] - 200))

    def run(self):
        self.isrunning = True
        while self.isrunning:
            # 绘制背景图像
            self.screen.fill("black")

            # 绘制标题
            self.draw()

            # 创建按钮
            self.screen.blit(self.botton1, self.rect_b1)
            self.screen.blit(self.botton2, self.rect_b2)
            self.screen.blit(self.botton3, self.rect_b3)
            self.screen.blit(self.botton4, self.rect_b4)

            # 获取鼠标对象位置
            mouse_pos = pg.mouse.get_pos()

            # 检测鼠标悬停
            if self.rect_b1.collidepoint(mouse_pos):
                self.color_b1 = LIGHT_BLUE
            else:
                self.color_b1 = WHITE

            if self.rect_b2.collidepoint(mouse_pos):
                self.color_b2 = LIGHT_BLUE
            else:
                self.color_b2 = WHITE

            if self.rect_b3.collidepoint(mouse_pos):
                self.color_b3 = LIGHT_BLUE
            else:
                self.color_b3 = WHITE

            if self.rect_b4.collidepoint(mouse_pos):
                self.color_b4 = LIGHT_BLUE
            else:
                self.color_b4 = RED
            # 重新渲染字体
            self.botton1 = self.text_font.render(self.optionsTexts[0], True, self.color_b1)
            self.botton2 = self.text_font.render(self.optionsTexts[1], True, self.color_b2)
            self.botton3 = self.text_font.render(self.optionsTexts[2], True, self.color_b3)
            self.botton4 = self.text_font.render(self.optionsTexts[3], True, self.color_b4)
            # 更新窗口
            pg.display.update()

            # 检测按钮点击
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MOD.QUIT()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.rect_b1.collidepoint(mouse_pos):
                        self.isrunning = False
                    if self.rect_b2.collidepoint(mouse_pos):
                        MOD.QUIT()
                    if self.rect_b3.collidepoint(mouse_pos):
                        self.files.run()
                    if self.rect_b4.collidepoint(mouse_pos):
                        self.game.ispaused = False
                        self.isrunning = False
                        self.game.startMenu.run()
            # 更新窗口
            pg.display.update()
