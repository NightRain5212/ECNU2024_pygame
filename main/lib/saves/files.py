import pygame as pg
from settings import *
from lib.Player import Player
from lib.menus.pauseMenu import pauseMenu
import csv
from lib import tiles
from lib import MOD
from lib.saves import saveManager
class files():
    def __init__(self):
        self.screen=MOD.get_screen()
        self.submenu=menu(600,400,400,200)
        self.load_img()

        self.file_num=6#存档槽位数量
        self.create_files()
    def load_img(self):
        self.background= pg.image.load(FILE_BACKGROUND_PATH).convert_alpha()
        self.background=pg.transform.scale(self.background, (WIDTH, HEIGTH))
        self.file_pic=pg.image.load(FILE_PIC_PATH).convert_alpha()
        self.file_pic= pg.transform.scale(self.file_pic, (500, 160))
        self.Back_Button_Pic=pg.image.load(FILE_GO_BACK_BUTTON_PATH).convert_alpha()
        self.Back_Button_Pic=pg.transform.scale(self.Back_Button_Pic, (350,80))

    def create_files(self):
        self.file_list=[]
        for i in range(self.file_num+1):
            temp_file=MOD.BUTTON((i%2+1)*(200+500)-500,i//2*265+105,self.file_pic)
            temp=gear(temp_file,i+1)
            self.file_list.append(temp)
        self.Back_Button=MOD.BUTTON(20,20,self.Back_Button_Pic)

    def run(self):
        ismenurun = False
        loadtip=0
        while True:
            self.screen.fill((0,0,0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MOD.QUIT()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.Back_Button.Active1():
                        return

                    if not ismenurun:
                        for file in self.file_list:
                            if file.button.Active1():
                                self.submenu.entry = file.num
                                ismenurun = True
                    else:
                        if self.submenu.back_button.Active1():
                            self.submenu.entry = 0
                            loadtip = 0
                            ismenurun = False
                        if self.submenu.clear_button.Active1():
                            saveManager.clear_game(self.submenu.entry, self.game)
                            loadtip = 0
                            ismenurun = False
                        if self.submenu.save_button.Active1():
                            saveManager.save_game(self.submenu.entry, self.game)
                            loadtip = 0
                            ismenurun = False
                            self.show_save_success()
                        if self.submenu.load_button.Active1():
                            if saveManager.load_game(self.submenu.entry, self.game):
                                ismenurun = False
                                return True
                            else:
                                #未启用self.show_load_error()
                                loadtip=90#持续时间
                                # 显示加载失败提示

            self.screen.blit(self.background,(0,0))
            self.Back_Button.draw()
            for i in range(self.file_num+1):
                self.file_list[i].draw()
            if ismenurun:
                self.submenu.draw()
            if loadtip>0:
                MOD.draw_text("No Data!",FONT3,RED,40,WIDTH//2-100,HEIGTH//2 )
                loadtip-=1
            pg.display.flip()

    def show_save_success(self):
        font = pg.font.Font(FONT3, 30)
        text = font.render("Save Successful!", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGTH//2))
        self.screen.blit(text, text_rect)
        pg.display.flip()
        pg.time.wait(1000)

    def show_load_error(self):
        font = pg.font.Font(FONT3, 30)
        text = font.render("Load Failed - No Save File!", True, RED)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGTH//2))
        self.screen.blit(text, text_rect)
        pg.display.flip()
        pg.time.wait(1000)

class gear():
    def __init__(self,button,num,statu=0):
        self.num=num#档位编号
        self.button=button
        self.statu=statu
        self.screen=MOD.get_screen()
        self.size_x=self.button.image.get_rect().width
        self.size_y =self.button.image.get_rect().height
    #绘制文本
    def draw(self):
        x = self.button.rect.topleft[0]
        y = self.button.rect.topleft[1]
        self.button.draw()
        save_info = saveManager.get_save_info(self.num)
        if save_info is None:
            MOD.draw_text("Empty Slot", FONT2, BLACK, 40, x + self.size_x//2 - 60, y + self.size_y//2 - 20)
        else:
            MOD.draw_text(f"Save {self.num}", FONT2, BLACK, 40, x + 20, y + 20)
            MOD.draw_text(save_info, FONT2, BLACK, 30, x + 20, y + 70)

class menu():
    def __init__(self,x,y,size_x,size_y):#xy是左上角坐标
        self.screen=MOD.get_screen()
        self.x=x
        self.y=y
        self.size_x=size_x
        self.size_y = size_y
        self.loadimg()
        self.save_button = MOD.BUTTON(self.x+35,self.y+self.size_y-self.size_y//5-5 , self.save_img)
        self.load_button = MOD.BUTTON(self.x-30+self.size_x-self.size_x//4,self.y+self.size_y-self.size_y//5-5 , self.load_img)
        self.back_button=MOD.BUTTON(self.x-size_x//12+self.size_x,self.y , self.back_img)
        self.clear_button = MOD.BUTTON(self.x+40+115, self.y+self.size_y-self.size_y//5-5, self.clear_img)
        self.entry=0#记录是通过那个档位按下的

    def loadimg(self):
        self.menu_pic=pg.image.load(FILE_MENU_PIC_PATH).convert_alpha()
        self.menu_pic=pg.transform.scale(self.menu_pic, (self.size_x,self.size_y))
        self.save_img = pg.image.load(FILE_SAVE_PIC_PATH).convert_alpha()
        self.load_img = pg.image.load(FILE_LOAD_PIC_PATH).convert_alpha()
        self.clear_img = pg.image.load(FILE_CLEAR_PIC_PATH).convert_alpha()
        self.back_img =pg.image.load(FILE_BACK_BUTTON_PATH).convert_alpha()
        self.save_img = pg.transform.scale(self.save_img, (self.size_x//4, self.size_y//5))
        self.load_img = pg.transform.scale(self.load_img, (self.size_x//4, self.size_y//5))
        self.back_img= pg.transform.scale(self.back_img, (self.size_x//12, self.size_x//12))
        self.clear_img = pg.transform.scale(self.clear_img, (self.size_x // 4, self.size_y // 5))

    def draw(self):
        self.screen.blit(self.menu_pic,(self.x,self.y))
        self.save_button.draw()
        self.load_button.draw()
        self.back_button.draw()
        self.clear_button.draw()





