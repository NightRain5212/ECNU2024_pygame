import pygame as pg
import sys
import csv
from settings import *
from lib import tiles

from lib import MOD
class MapEditor:
    def __init__(self):
        self.level=0
        self.screen=MOD.get_screen()
        self.FONTfont=pg.font.Font(FONT,40)
        self.scroll=0
        self.scroll_left=False
        self.scroll_right = False
        self.scroll_speed=1
        self.current_tile=0#记录鼠标的选中
        #按钮列表
        self.button_list=[]
        self.button_row=0
        self.button_col=0

        self.iseditor=1

    #部分初始化MapEditor,以便后序实现函数封装
    def reset(self):
        self.scroll=0
        self.scroll_left=False
        self.scroll_right = False
        self.scroll_speed=1
        self.current_tile=0
        self.iseditor=1
    def renew(self):
        self.button_list=[]
        self.button_row=0
        self.button_col=0
    #清屏
    def screen_clear(self):
        __world_data = []
        for row in range(ROW):
            r = [-1] * COL
            __world_data.append(r)
        for tile in range(COL):
            __world_data[ROW - 1][tile] = 29
            __world_data[ROW - 2][tile] = 29
        return __world_data
    #画网格
    def draw_lines(self):
        for c in range(COL + 1):#画竖线
            pg.draw.line(self.screen, WHITE,( c * TILE_SIZE+self.scroll, 0), (c * TILE_SIZE+self.scroll, HEIGTH))
        for c in range(ROW + 1):#画横线
            pg.draw.line(self.screen, WHITE, (0,c*TILE_SIZE), (WIDTH, c*TILE_SIZE))#坐标原点是左上角
        if self.iseditor:
            pg.draw.rect(self.screen, GRAY, (WIDTH-SIDESIZE, 0,SIDESIZE , HEIGTH))
    #更新背景地图列表
    def background_update(self):
        self.backgroundlist = MOD.load_level_map(self.level)

    def run(self):
        page=1#按钮页面为1
        #加载按钮图标
        save_img = pg.image.load(MAP_EDITOR_SAVE_BUTTON_PATH).convert_alpha()
        load_img = pg.image.load(MAP_EDITOR_LOAD_BUTTON_PATH).convert_alpha()
        quit_img = pg.image.load(MAP_EDITOR_QUIT_BUTTON_PATH).convert_alpha()
        clear_img = pg.image.load(MAP_EDITOR_CLEAR_BUTTON_PATH).convert_alpha()
        up_img = pg.image.load(MAP_EDITOR_UP_BUTTON_PATH).convert_alpha()
        down_img = pg.image.load(MAP_EDITOR_DOWN_BUTTON_PATH).convert_alpha()
        left_img = pg.image.load(MAP_EDITOR_LEFT_BUTTON_PATH).convert_alpha()
        right_img = pg.image.load(MAP_EDITOR_RIGHT_BUTTON_PATH).convert_alpha()

        save_img =pg.transform.scale(save_img,(GAP+2*TILE_SIZE,TILE_SIZE))
        load_img = pg.transform.scale(load_img, (GAP + 2*TILE_SIZE, TILE_SIZE))
        quit_img = pg.transform.scale(quit_img, (GAP + 2*TILE_SIZE, TILE_SIZE))
        clear_img = pg.transform.scale(clear_img, (GAP + 2*TILE_SIZE, TILE_SIZE))
        up_img = pg.transform.scale(up_img, (2*TILE_SIZE, TILE_SIZE))
        down_img = pg.transform.scale(down_img, (2*TILE_SIZE, TILE_SIZE))
        left_img = pg.transform.scale(left_img, (TILE_SIZE, TILE_SIZE))
        right_img = pg.transform.scale(right_img, (TILE_SIZE, TILE_SIZE))
        clear2_img = pg.transform.scale(clear_img, (TILE_SIZE, TILE_SIZE))
        #加载图标图片
        img_tiles=MOD.load_world_usualpic_tileslist()

        world_data=self.screen_clear()

        for i in range(len(img_tiles)):
            temp_tile= pg.transform.scale(img_tiles[i], (TILE_SIZE,TILE_SIZE ))
            tile_button=MOD.BUTTON(WIDTH-SIDESIZE+self.button_col*(GAP+TILE_SIZE)+GAP,(GAP+self.button_row*(GAP+TILE_SIZE)),temp_tile)
            self.button_list.append(tile_button)
            if self.button_col==3:
                self.button_col = 0
                self.button_row+=1
                self.button_row%=12
            else:
                self.button_col+=1
        save_button = MOD.BUTTON(WIDTH - 4 * (GAP + TILE_SIZE) - TILE_SIZE, HEIGTH - 2 * (GAP + TILE_SIZE), save_img)
        load_button = MOD.BUTTON(WIDTH - 2 * (GAP + TILE_SIZE) - TILE_SIZE, HEIGTH - 2 * (GAP + TILE_SIZE), load_img)
        quit_button = MOD.BUTTON(WIDTH - 4 * (GAP + TILE_SIZE) - TILE_SIZE, HEIGTH - GAP - TILE_SIZE, quit_img)
        clear_button = MOD.BUTTON(WIDTH - 2 * (GAP + TILE_SIZE) - TILE_SIZE, HEIGTH - GAP - TILE_SIZE, clear_img)
        up_button = MOD.BUTTON(WIDTH - 4*GAP - 4*TILE_SIZE, HEIGTH -2* (GAP + TILE_SIZE)-TILE_SIZE, up_img)
        down_button = MOD.BUTTON(WIDTH - 3 * GAP -2* TILE_SIZE, HEIGTH -2*(GAP + TILE_SIZE) -TILE_SIZE, down_img)
        left_button = MOD.BUTTON(WIDTH -  2*TILE_SIZE, HEIGTH - 2* TILE_SIZE, left_img)
        right_button = MOD.BUTTON(WIDTH -  2*TILE_SIZE, HEIGTH - 2* TILE_SIZE, right_img)
        clear2_button = MOD.BUTTON(WIDTH - 2 * (GAP + TILE_SIZE) - 2 * TILE_SIZE, HEIGTH - GAP - 2 * TILE_SIZE,clear2_img)
        #运行
        while(True):
            CLOCK.tick(FPS)

            #处理键盘事件
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    MOD.QUIT()
                if event.type==pg.KEYDOWN:
                    #暂停该功能
                    # if event.key==pg.K_UP:
                    #     if self.level==5:
                    #         self.level = 1
                    #     else:
                    #         self.level+=1
                    #     world_data=self.screen_clear()
                    #     #world_data = MOD.load_seed(self.level)#功能暂不启用
                    #     self.reset()#复位屏幕显示为最左边
                    # if event.key==pg.K_DOWN:
                    #     if self.level==1:
                    #         self.level = 5
                    #     else:
                    #         self.level-=1
                    #     world_data=self.screen_clear()
                    #     #world_data = MOD.load_seed(self.level)#功能暂不启用
                    #     self.reset()#复位屏幕显示为最左边
                    if event.key==pg.K_LEFT:
                        if self.scroll<0:
                            self.scroll_left = True
                    if event.key==pg.K_RIGHT:
                        if self.scroll+COL*TILE_SIZE>WIDTH:
                            self.scroll_right = True
                    if event.key==pg.K_LSHIFT:
                        self.scroll_speed=5
                if event.type==pg.KEYUP:
                    if event.key==pg.K_LEFT:
                        self.scroll_left = False
                    if event.key==pg.K_RIGHT:
                        self.scroll_right = False
                    if event.key==pg.K_LSHIFT:
                        self.scroll_speed=1
            #编辑窗口滑动(存在5的窗口缓冲区）
            if self.scroll_left==True and self.scroll+5*self.scroll_speed<=0:
                self.scroll += 5 * self.scroll_speed
            if self.scroll_right==True and self.scroll-5*self.scroll_speed+COL*TILE_SIZE>=WIDTH:
                self.scroll-=5*self.scroll_speed

            if self.iseditor:
                #处理按钮事件
                if save_button.Active():
                    with open(f"mapseed\level{self.level}_seed.csv","w",newline="") as csvfile:
                        writer= csv.writer(csvfile,delimiter=",")
                        for row in world_data:
                            writer.writerow(row)
                if load_button.Active():
                    world_data=MOD.load_seed(self.level)
                if quit_button.Active():
                    self.reset()
                    self.renew()
                    break
                if clear_button.Active():
                    world_data=self.screen_clear()
                if up_button.Active():
                    page+=1
                    if page>=2:
                        page=2
                if down_button.Active():
                    page-=1
                    if page<=1:
                        page=1
                if right_button.Active():
                    self.iseditor=0
                if clear2_button.Active():
                    for i, row in enumerate(world_data):
                        for j, element in enumerate(row):
                            if element>=0:
                                if tiles.TILES[element]["type"]=="enemy":  # 假设满足某个条件
                                    world_data[i][j] = -1
            else:
                if left_button.Active():
                    self.iseditor=1

            PO=pg.mouse.get_pos()#返回鼠标位置(x,y),左上角为原点
            a=(PO[0]-self.scroll)//TILE_SIZE
            b=PO[1]//TILE_SIZE
            if self.iseditor:
                if PO[0]<WIDTH-SIDESIZE-5 and PO[1]<HEIGTH:
                    if pg.mouse.get_pressed()[0]==1:
                        if world_data[b][a] !=self.current_tile:
                            world_data[b][a] = self.current_tile
                    if pg.mouse.get_pressed()[2]==1:
                        world_data[b][a] = -1#再次点击删除
            else:
                if (PO[0]<WIDTH-2*TILE_SIZE-5 and PO[1]<HEIGTH)or(PO[0]<WIDTH and PO[1]<HEIGTH-2*TILE_SIZE-5):
                    if pg.mouse.get_pressed()[0]==1:
                        if world_data[b][a] !=self.current_tile:
                            world_data[b][a] = self.current_tile
                    if pg.mouse.get_pressed()[2]==1:
                        world_data[b][a] = -1#再次点击删除

            #通过循环延长背景图长度，多图叠加
            MOD.draw_background(self.level,self.backgroundlist,self.screen,self.scroll)
            #画瓷砖
            for y, row in enumerate(world_data):
                for x, tile in enumerate(row):
                    if tile >= 0:
                        self.screen.blit(img_tiles[tile], (x * TILE_SIZE + self.scroll, y * TILE_SIZE))

            #画网格
            self.draw_lines()
            if self.iseditor:
                 #显示按钮
                 for button_count,i in enumerate(self.button_list[page*48-48:page*48]):
                     i.draw()
                     button_count=button_count+page*48-48
                     temp_color=WHITE
                     if tiles.TILES[button_count]["type"] =="decoration":
                         temp_color = YELLOW
                     elif tiles.TILES[button_count]["type"] =="impassable":
                         temp_color =RED
                     elif tiles.TILES[button_count]["type"] == "water":
                         temp_color = BLUE
                     elif tiles.TILES[button_count]["type"] == "object":
                         temp_color = GREEN
                     elif tiles.TILES[button_count]["type"] == "enemy":
                         temp_color = BLACK
                     #绘制图标名称
                     MOD.draw_text(tiles.TILES[button_count]["name"],FONT,temp_color,20,i.rect.x, i.rect.y+TILE_SIZE+5)
                     if i.Active():
                         self.current_tile=button_count
                 save_button.draw()
                 load_button.draw()
                 quit_button.draw()
                 clear_button.draw()
                 up_button.draw()
                 down_button.draw()
                 right_button.draw()
                 clear2_button.draw()
                 #按钮高亮显示
                 pg.draw.rect(self.screen,GREEN,self.button_list[self.current_tile].rect,3)
            else:
                left_button.draw()
            #停止启用该功能
            # #显示文本
            # MOD.draw_text(f"level:{self.level}",self.FONTfont,WHITE,30,HEIGTH-100)
            # MOD.draw_text("按下上下键进行切换", self.FONTfont, WHITE, 30, HEIGTH - 50)

            pg.display.update()
