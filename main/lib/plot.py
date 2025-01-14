import pygame as pg
from settings import *
from lib import MOD

class Plot():
    def __init__(self):
        self.screen=MOD.get_screen()
        self.pagelist=[]
        self.loadpage()
        self.doc_content = PLOT_TEXTS

        self.FONT1 = pg.font.Font(FONT, 30)
        self.FONT2 = pg.font.Font(FONT1, 30)
        self.FONT3 = pg.font.Font(FONT2, 30)  # 提供三种字体
    # 加载页面文字
    def loadpage(self):
        piclist=[LEVEL1_BACKGROUND1,LEVEL2_BACKGROUND1,LEVEL3_BACKGROUND2,LEVEL4_BACKGROUND2,LEVEL5_BACKGROUND,STARTMENU_BACKGROUND]
        for i in range(6):
            page=pg.image.load(piclist[i]).convert()
            page = pg.transform.scale(page, (WIDTH, HEIGTH))
            self.pagelist.append(page)
        self.back_img = pg.image.load(PLOT_BACKBUTTON_PATH).convert_alpha()
        self.back_img = pg.transform.scale(self.back_img, (50, 50))
        self.back_button = MOD.BUTTON(40, 20, self.back_img)
        self.left_img = pg.image.load(PLOT_LEFTBUTTON_PATH).convert_alpha()
        self.left_img = pg.transform.scale(self.left_img, (100, 100))
        self.left_button = MOD.BUTTON(40, HEIGTH-120, self.left_img)
        self.right_img = pg.image.load(PLOT_RIGHTBUTTON_PATH).convert_alpha()
        self.right_img = pg.transform.scale(self.right_img, (100, 100))
        self.right_button = MOD.BUTTON(WIDTH-140, HEIGTH-120, self.right_img)

    def draw_document(self,page):
        """绘制文档内容"""
        y_pos = 200
        for paragraph in self.doc_content[page-1]:
            lines = paragraph.split("/n")
            for line in lines:
                if page==1:
                    text = self.FONT1.render(line, True, BLACK)
                elif page==5:
                    text = self.FONT1.render(line, True, BLUE)
                else:
                    text = self.FONT1.render(line, True, WHITE)
                self.screen.blit(text, (100, y_pos))
                y_pos += text.get_height() + 10  # 行间距

    def run(self):
        page=1
        while(True):
            self.screen.fill((0, 0, 0))
            if page==6:
                MOD.playbackmusic(5)
            else:
                MOD.playbackmusic(0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if self.back_button.Active():
                    return
                if self.left_button.Active():
                   page-=1
                   if page<=1:
                       page=1
                if self.right_button.Active():
                   page+=1
                   if page>=6:
                       page=6

            self.screen.blit(self.pagelist[page-1],(0,0))
            self.back_button.draw()
            if page>1:
                self.left_button.draw()
            if page <6:
                self.right_button.draw()
            self.draw_document(page)
            pg.display.flip()
