import pygame as pg
import sys
from settings import *
from lib.mapeditor import MapEditor
from lib import MOD
class Mapmenu:
    def __init__(self):
        self.screen = MOD.get_screen()
        self.background_image = pg.image.load(STARTMENU_BACKGROUND).convert()
        self.text_font = pg.font.Font(FONT,60)

        self.create_bottons()
        self.MapEditor=MapEditor()

    def create_bottons(self):
        #按钮颜色
        self.color_b1 = WHITE
        self.color_b2 = WHITE
        self.color_b3 = WHITE
        self.color_b4 = WHITE
        self.color_b5 = WHITE
        self.color_b6 = WHITE
        #按钮文本
        self.optionsTexts = ["Level1","Level2","Level3","Level4","Level5","Goback"]
        self.botton1 = self.text_font.render(self.optionsTexts[0],True,self.color_b1)
        self.botton2 = self.text_font.render(self.optionsTexts[1], True, self.color_b2)
        self.botton3 = self.text_font.render(self.optionsTexts[2], True, self.color_b3)
        self.botton4 = self.text_font.render(self.optionsTexts[3], True, self.color_b4)
        self.botton5 = self.text_font.render(self.optionsTexts[4], True, self.color_b5)
        self.botton6 = self.text_font.render(self.optionsTexts[5], True, self.color_b6)
        #按钮矩形区域
        self.rect_b1 = self.botton1.get_rect(center=(550,200))
        self.rect_b2 = self.botton2.get_rect(center=(550,300))
        self.rect_b3 = self.botton3.get_rect(center=(550,400))
        self.rect_b4 = self.botton4.get_rect(center=(550,500))
        self.rect_b5 = self.botton5.get_rect(center=(550, 600))
        self.rect_b6 = self.botton6.get_rect(center=(550, 700))

    def run(self):
        running = True
        while running:

            # 绘制背景图像
            self.screen.blit(self.background_image, (0, 0))
            # 创建按钮
            self.screen.blit(self.botton1, self.rect_b1)
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
                self.color_b4 = WHITE
            if self.rect_b5.collidepoint(mouse_pos):
                self.color_b5 = LIGHT_BLUE
            else:
                self.color_b5 = WHITE
            if self.rect_b6.collidepoint(mouse_pos):
                self.color_b6 = LIGHT_BLUE
            else:
                self.color_b6 = WHITE
            # 重新渲染字体
            self.botton1 = self.text_font.render(self.optionsTexts[0], True, self.color_b1)
            self.botton2 = self.text_font.render(self.optionsTexts[1], True, self.color_b2)
            self.botton3 = self.text_font.render(self.optionsTexts[2], True, self.color_b3)
            self.botton4 = self.text_font.render(self.optionsTexts[3], True, self.color_b4)
            self.botton5 = self.text_font.render(self.optionsTexts[4], True, self.color_b5)
            self.botton6 = self.text_font.render(self.optionsTexts[5], True, self.color_b6)
            # 更新窗口
            pg.display.update()
            if self.mapmenu_events()==False:#使用返回值实现内部函数终止外部循环
                running=False

    def mapmenu_events(self):
        for event in pg.event.get():
            # 退出游戏
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # 检测点击按钮
            if event.type == pg.MOUSEBUTTONDOWN:
                m_pos = pg.mouse.get_pos()
                if self.rect_b1.collidepoint(m_pos):
                    self.MapEditor.level=1
                    self.MapEditor.background_update()
                    MOD.playbackmusic(1)
                    self.MapEditor.run()
                    MOD.playbackmusic(0)
                    return True
                if self.rect_b2.collidepoint(m_pos):
                    self.MapEditor.level= 2
                    self.MapEditor.background_update()
                    MOD.playbackmusic(2)
                    self.MapEditor.run()
                    MOD.playbackmusic(0)
                    return True
                if self.rect_b3.collidepoint(m_pos):
                    self.MapEditor.level = 3
                    self.MapEditor.background_update()
                    MOD.playbackmusic(3)
                    self.MapEditor.run()
                    MOD.playbackmusic(0)
                    return True
                if self.rect_b4.collidepoint(m_pos):
                    self.MapEditor.level = 4
                    self.MapEditor.background_update()
                    MOD.playbackmusic(4)
                    self.MapEditor.run()
                    MOD.playbackmusic(0)
                    return True
                if self.rect_b5.collidepoint(m_pos):
                    self.MapEditor.level = 5
                    self.MapEditor.background_update()
                    MOD.playbackmusic(5)
                    self.MapEditor.run()
                    MOD.playbackmusic(0)
                    return True
                if self.rect_b6.collidepoint(m_pos):
                    return False
