from typing import Any
import pygame as pg
from settings import *
from lib.Player import Player
from lib.menus.pauseMenu import pauseMenu
from lib import MOD
from lib import tiles
from lib.monsters.wolf import DarkWolf
from lib.monsters.Paraflower import Flower
from lib.monsters.snake import Snake
from lib.monsters.Warrant import Warrant
from lib.monsters.zhiyin_box import Box
from lib.monsters.dragon import Dragon
from lib.monsters.prop import  precious_box,Luckycloud
from lib.monsters.firegiant import Firegiant
class Level:
    # 初始化关卡
    def __init__(self,game,num):
        self.game=game
        self.screen=MOD.get_screen()
        #处理精灵组
        self.obstacles=pg.sprite.Group()
        self.water=pg.sprite.Group()
        self.decoration=pg.sprite.Group()
        self.enemies=pg.sprite.Group()
        self.enemymagic=pg.sprite.Group()
        self.objects=pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.player_magic = pg.sprite.Group()
        self.fractions=pg.sprite.Group()
        self.boss = None
        self.garbage_bin = pg.sprite.Group()  # 存放待销毁精灵的精灵组
        self.prop = pg.sprite.Group()  # 道具组
        self.isPaused=False
        self.levelnum=num
        #按钮背景图相关
        self.backgrounds=MOD.load_level_map(num)
        self.menu_img=pg.image.load(MENU_ICON_PATH).convert_alpha()
        self.menu_img=pg.transform.scale(self.menu_img,MENU_ICON_SCALE)
        self.menu_button=MOD.BUTTON(WIDTH-130,20,self.menu_img)
        self.tileimages=MOD.load_world_usualpic_tileslist()

        self.map_width=COL*TILE_SIZE
        self.map_height=ROW*TILE_SIZE
        #类相关
        self.pauseMenu=pauseMenu(self.game)

        self.player_lv = self.game.player_lv
        self.player = Player(self)
        self.camera=Camera(0,0,WIDTH,HEIGTH,self.map_width,self.map_height)
        self.camera.update(self.player)
        self.load_Sprites()
        self.load_npc()

        self.cure_lock = self.game.cure_lock
        self.magic_lock = self.game.magic_lock
        self.cure_ready_icon = pg.image.load(CURE_READY_ICON_PATH).convert_alpha()
        self.cure_ready_icon = pg.transform.scale(self.cure_ready_icon, CURE_READY_ICON_SCALE)
        self.cure_not_ready_icon = pg.image.load(CURE_CD_ICON_PATH).convert_alpha()
        self.cure_not_ready_icon = pg.transform.scale(self.cure_not_ready_icon, CURE_CD_ICON_SCALE)
        self.cure_rect = self.cure_ready_icon.get_rect()

        self.magic_arrow_ready_icon = pg.image.load(MAGIC_ARROW_READY_ICON_PATH).convert_alpha()
        self.magic_arrow_ready_icon = pg.transform.scale(self.magic_arrow_ready_icon,MAGIC_ARROW_READY_ICON_SCALE)
        self.magic_arrow_cd_icon = pg.image.load(MAGIC_ARROW_CD_ICON_PATH).convert_alpha()
        self.magic_arrow_cd_icon = pg.transform.scale(self.magic_arrow_cd_icon,MAGIC_ARROW_CD_ICON_SCALE)
        self.magic_rect = self.magic_arrow_ready_icon.get_rect()

        self.first_load_player=True
        self.first_load_player_status=True
        self.is_display_rect_borders=False
        self.is_display_player_position=False
        self.backgroundimg = pg.image.load(STARTMENU_BACKGROUND).convert_alpha()
        self.backgroundimg = pg.transform.scale(self.backgroundimg,(WIDTH,HEIGTH))
    # 加载地图数据
    def load_Sprites(self):
        self.mapseed=MOD.load_seed(self.levelnum)
        for y,row in enumerate(self.mapseed):
            for x,tile in enumerate(row):
                if tile>=0:
                    rect_x=x*TILE_SIZE
                    rect_y = y * TILE_SIZE
                    tileimage = self.tileimages[tile]
                    tilesprite = tiles.Tile(x * TILE_SIZE, y * TILE_SIZE, tileimage)
                    if tiles.TILES[tile]["type"]=="impassable":
                        self.obstacles.add(tilesprite)
                    elif tiles.TILES[tile]["type"] == "player":
                        #暂未启用
                        #print("初始化角色",rect_x,rect_y)
                        MOD.set_position(self.player,rect_x,rect_y)
                        self.player.update()
                        self.camera.update(self.player)
                    elif tiles.TILES[tile]["type"]=="water":
                        self.water.add(tilesprite)
                    elif tiles.TILES[tile]["type"]=="enemy":
                        if tiles.TILES[tile]["name"]=="wolf":
                            wolf=DarkWolf(self)
                            MOD.set_position(wolf, rect_x, rect_y)
                            self.enemies.add(wolf)
                        elif tiles.TILES[tile]["name"]=="warrent":
                            warrent=Warrant(self)
                            MOD.set_position(warrent, rect_x, rect_y)
                            self.enemies.add(warrent)
                        elif tiles.TILES[tile]["name"]=="Fantasy":
                            paraflower=Flower(self)
                            MOD.set_position(paraflower, rect_x, rect_y)
                            self.enemies.add(paraflower)
                        elif tiles.TILES[tile]["name"] == "snake":
                            snake =Snake (self)
                            MOD.set_position(snake, rect_x, rect_y)
                            self.enemies.add(snake)
                        elif tiles.TILES[tile]["name"] == "zhiyin":
                            zhiyin =Box(self)
                            MOD.set_position(zhiyin, rect_x, rect_y)
                            self.enemies.add(zhiyin)
                        elif tiles.TILES[tile]["name"] == "dragon":
                            dragon = Dragon(self)
                            MOD.set_position(dragon, rect_x, rect_y)
                            self.enemies.add(dragon)
                            self.boss = dragon
                        elif tiles.TILES[tile]["name"] == "firegiant":
                            firegiant = Firegiant(self)
                            MOD.set_position(firegiant, rect_x, rect_y)
                            self.enemies.add(firegiant)
                            self.boss = firegiant
                    elif tiles.TILES[tile]["type"]=="decoration":
                        self.decoration.add(tilesprite)
                    elif tiles.TILES[tile]["type"]=="object":
                        if tiles.TILES[tile]["name"]=="fragment":
                            self.fractions.add(tilesprite)
                        self.objects.add(tilesprite)
                    elif tiles.TILES[tile]["type"]=="prop":
                        if tiles.TILES[tile]["name"]=="precious_box":
                            one=precious_box(self)
                            MOD.set_position(one, rect_x, rect_y)
                            self.prop.add(one)
                        elif tiles.TILES[tile]["name"]=="lucky_rain":
                            one=Luckycloud(self)
                            MOD.set_position(one, rect_x, rect_y)
                            self.prop.add(one)
    # 绘制矩形边界
    def draw_rect_borders(self):
        for sprite in self.obstacles:
            pg.draw.rect(self.screen,RED,self.camera.apply(sprite),1)
        for sprite in self.water:
            pg.draw.rect(self.screen,RED,self.camera.apply(sprite),1)
        for sprite in self.decoration:
            pg.draw.rect(self.screen,RED,self.camera.apply(sprite),1)
        for sprite in self.objects:
            pg.draw.rect(self.screen,RED,self.camera.apply(sprite),1)
        pg.draw.rect(self.screen, RED, self.camera.apply(self.player), 1)
        for sprite in self.enemies:
            if sprite.alive():
                pg.draw.rect(self.screen,RED,self.camera.apply(sprite),1)

    # 显示HP
    def display_hp(self):
        self.hp_rate=self.player.hp/self.player.max_hp
        self.hp_w=self.hp_rate*HP_BAR_WIDTH
        pg.draw.rect(self.screen,GRAY,(HP_RECT_X,HP_RECT_Y,HP_BAR_WIDTH,HP_BAR_HEIGHT))
        pg.draw.rect(self.screen,GREEN,(HP_RECT_X,HP_RECT_Y,self.hp_w,HP_BAR_HEIGHT))
        self.hp_text_font=pg.font.Font(FONT,25)
        self.hp_text=self.hp_text_font.render(f"{self.player.hp:.2f}/{self.player.max_hp:.2f}",True,WHITE)
        self.hp_title=self.hp_text_font.render("HP:",True,WHITE)
        self.game.screen.blit(self.hp_title,(HP_RECT_X-50,HP_RECT_Y))
        self.game.screen.blit(self.hp_text,(HP_RECT_X+HP_BAR_WIDTH/2,HP_RECT_Y))

    # 显示MP
    def display_mp(self):
        self.mp_rate=self.player.mp/self.player.max_mp
        self.mp_w=self.mp_rate*MP_BAR_WIDTH
        pg.draw.rect(self.screen,GRAY,(MP_RECT_X,MP_RECT_Y,MP_BAR_WIDTH,MP_BAR_HEIGHT))
        pg.draw.rect(self.screen,BLUE,(MP_RECT_X,MP_RECT_Y,self.mp_w,MP_BAR_HEIGHT))    
        self.mp_text_font=pg.font.Font(FONT,25)
        self.mp_text=self.mp_text_font.render(f"{self.player.mp:.2f}/{self.player.max_mp:.2f}",True,WHITE)
        self.mp_title=self.mp_text_font.render("MP:",True,WHITE)
        self.game.screen.blit(self.mp_title,(MP_RECT_X-50,MP_RECT_Y))
        self.game.screen.blit(self.mp_text,(MP_RECT_X+MP_BAR_WIDTH/2,MP_RECT_Y))

    # 显示治疗状态
    def display_cure_state(self):
        if self.player.cure_lock:
            return
        # 将图标放在血条右侧
        self.cure_rect.x = HP_RECT_X + HP_BAR_WIDTH + 50  # 调整水平位置
        self.cure_rect.centery = HP_RECT_Y + HP_BAR_HEIGHT // 2  # 垂直居中对齐

        # 根据技能状态显示对应图标
        if self.player.cure_ready:
            self.game.screen.blit(self.cure_ready_icon, self.cure_rect)
        else:
            self.game.screen.blit(self.cure_not_ready_icon, self.cure_rect)

    # 显示技能状态
    def display_magic_state(self):
        if self.player.magic_lock:
            return
        self.magic_rect.x = HP_RECT_X + HP_BAR_WIDTH + 50  + self.cure_rect.width + 10
        self.magic_rect.centery = HP_RECT_Y + HP_BAR_HEIGHT // 2
        iscd = self.player.check_magic_ready()
        if iscd:
            self.game.screen.blit(self.magic_arrow_cd_icon, self.magic_rect)
        else:
            self.game.screen.blit(self.magic_arrow_ready_icon, self.magic_rect)

    # 显示boss血条
    def display_boss_hp(self):
        if self.boss is None:
            return
        self.boss_hp_rate=self.boss.hp/self.boss.max_hp
        self.boss_hp_w=self.boss_hp_rate*HP_BAR_WIDTH
        pg.draw.rect(self.screen,GRAY,(HP_RECT_X+WIDTH/2,HP_RECT_Y,HP_BAR_WIDTH,HP_BAR_HEIGHT))
        pg.draw.rect(self.screen,RED,(HP_RECT_X+WIDTH/2,HP_RECT_Y,self.boss_hp_w,HP_BAR_HEIGHT))
        self.boss_hp_text_font=pg.font.Font(FONT,25)
        self.boss_hp_text=self.boss_hp_text_font.render("{:.2f}/{}".format(self.boss.hp,self.boss.max_hp),True,WHITE)
        self.boss_hp_title=self.boss_hp_text_font.render("BOSS HP:",True,WHITE)
        self.game.screen.blit(self.boss_hp_title,(HP_RECT_X+WIDTH/2-50,HP_RECT_Y))
        self.game.screen.blit(self.boss_hp_text,(HP_RECT_X+WIDTH/2+HP_BAR_WIDTH/2,HP_RECT_Y))

    # 显示玩家位置
    def display_player_position(self):
        self.player_position_text_font=pg.font.Font(FONT,40)
        self.player_position_text=self.player_position_text_font.render(f"(x: {self.player.rect.x}, y: {self.player.rect.y})",True,WHITE)
        self.game.screen.blit(self.player_position_text,(10,MP_RECT_Y+MP_BAR_HEIGHT+40))

    def reset_player_status(self):
        if self.first_load_player_status:
            self.player.lv = self.game.player_lv
            self.player.max_hp = MAXHP * (1 + HPRATE_PER_LV * (self.player.lv - 1))
            self.player.max_mp = MAXMP * (1 + MPRATE_PER_LV * (self.player.lv - 1))
            self.player.atk = ATK_PER_FAMRE * (1 + ATKRATE_PER_LV * (self.player.lv - 1))
            self.player.hp = self.player.max_hp
            self.player.mp = self.player.max_mp
            self.first_load_player_status=False
        
    # 游戏结束
    def gameover(self):
        text = pg.font.Font(FONT3, 200)
        gameover_text = text.render(GAME_OVER_TEXTS, True, RED)
        text_rect = gameover_text.get_rect(center=(WIDTH // 2, HEIGTH // 2))
        alpha = 0
        fade_complete = False
        while not fade_complete:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MOD.QUIT()

            if alpha < 255:
                alpha += 5
                gameover_text.set_alpha(alpha)
            else:
                fade_complete = True
            self.screen.fill(BLACK)
            self.screen.blit(gameover_text, text_rect)
            pg.display.update()
        pg.time.delay(2000)
        self.playing = False

    # 游戏胜利
    def gamewin(self):
        text = pg.font.Font(FONT, 50)
        tests = GAME_WIN_TEXTS[self.levelnum]
        lines = tests.split("\n")
        x = 100
        y = 100
        self.screen.blit(self.backgroundimg,(0,0))
        for line in lines:
            gamewin_text = text.render(line, True, WHITE)
            alpha = 0
            fade_complete = False
            while not fade_complete:
                if alpha < 255:
                    alpha += 2
                    gamewin_text.set_alpha(alpha)
                else:
                    fade_complete = True
                self.screen.blit(gamewin_text, (x, y))
                pg.display.update()
            pg.time.delay(3000)
            y += 100
        self.playing = False

        if self.levelnum < 6:  # 确保不会超出索引范围
            self.game.level_Lock[self.levelnum + 1] = True  # 解锁下一关
            self.game.player_lv += 1
            self.player.update_stats()
            self.player.hp = self.player.max_hp
            self.player.mp = self.player.max_mp

    # 显示等级
    def display_lv(self):
        self.lv_img = pg.image.load(LV_ICON_PATH).convert_alpha()
        self.lv_img = pg.transform.scale(self.lv_img, LV_ICON_SCALE)
        self.lv_rect = self.lv_img.get_rect()
        x = 10
        y = MP_RECT_Y + MP_BAR_HEIGHT + 10
        for i in range(self.game.player_lv):
            self.screen.blit(self.lv_img, (x, y))
            x += 32

    # 更新玩家属性
    def update_player_stats(self):
        self.player.lv = self.game.player_lv
        self.player.update_stats()
        if self.first_load_player:
            self.first_load_player=False
            self.player.hp=self.player.max_hp
            self.player.mp=self.player.max_mp

    # # 游戏主循环
    # def run(self):
    #     self.playing = True
    #     while self.playing:
    #         # 控制游戏速度
    #         self.game.clock.tick(FPS)
    #         # 获取事件
    #         for event in pg.event.get():
    #             # 退出游戏
    #             if event.type == pg.QUIT:
    #                 if self.playing:
    #                     self.playing = False
    #                 MOD.QUIT()
    #             # 处理事件
    #             if event.type == pg.KEYDOWN:
    #                 if event.key == pg.K_ESCAPE:
    #                     self.game.ispaused = True
    #                 if event.key == pg.K_f:
    #                     self.is_display_rect_borders = not self.is_display_rect_borders
    #                 if event.key == pg.K_p:
    #                     self.is_display_player_position = not self.is_display_player_position
    #         keys = pg.key.get_pressed()
    #         mouses = pg.mouse.get_pressed()
    #
    #         # 画图
    #         self.screen.fill((0, 0, 0))
    #         MOD.draw_background(self.levelnum, self.backgrounds, self.screen, self.camera.view.x)
    #         for sprite in self.decoration:
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #         for sprite in self.obstacles:
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #         for sprite in self.water:
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #         for sprite in self.npcs:
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #         for sprite in self.objects:
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #
    #         # 画角色
    #         self.game.screen.blit(self.player.image, self.camera.apply(self.player))
    #         # 更新并绘制敌人
    #         for enemy in list(self.enemies):  # 使用list创建副本来遍历
    #             enemy.blood.update()
    #             if enemy.active:
    #                 self.game.screen.blit(enemy.image, self.camera.apply(enemy))
    #
    #                 # 更新并绘制敌人魔法效果
    #                 for sprite in list(self.enemymagic):  # 使用list创建副本来遍历
    #                     if sprite.active:
    #                         self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #         for sprite in list(self.enemymagic):
    #             if sprite.active:
    #                 sprite.update()
    #
    #         # 更新玩家技能特效
    #         for sprite in list(self.player_magic):
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #             sprite.update()
    #
    #         # 更新npc
    #         for sprite in self.npcs:
    #             sprite.update_animation()
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #             # 更新道具
    #         for prop in self.prop:
    #             prop.update()
    #             if prop.active:
    #                 self.game.screen.blit(prop.image, self.camera.apply(prop))
    #
    #         # 画物体
    #         for sprite in self.objects:
    #             self.game.screen.blit(sprite.image, self.camera.apply(sprite))
    #         # 静态图像最后画
    #         self.display_lv()
    #         self.display_hp()
    #         self.display_mp()
    #         self.update_player_stats()
    #         self.display_cure_state()
    #         self.display_magic_state()
    #         self.display_boss_hp()
    #         self.menu_button.draw()
    #         if self.is_display_rect_borders:
    #             self.draw_rect_borders()
    #         if self.is_display_player_position:
    #             self.display_player_position()
    #         pg.display.flip()
    #
    #         self.player.update(keys, mouses)
    #         if self.player.hp <= 0:
    #             self.gameover()
    #         self.camera.update(self.player)
    #         for enemy in self.enemies:
    #             enemy.update()
    #             # 在小怪类中有检查生命值，并且自己投递废物(子类以及自身)投到garbage_bin行为
    #         for garbage in list(self.garbage_bin):
    #             garbage.kill()
    #
    #         # 检查npc碰撞
    #         if self.check_npc_collision():
    #             if self.npc.name == "Eilin":
    #                 self.game.cure_lock = False
    #                 if self.npc_plot.active:
    #                     self.npc_plot.play_plot()
    #             elif self.npc.name == "Renault":
    #                 self.game.magic_lock = False
    #                 if self.npc_plot.active:
    #                     self.npc_plot.play_plot()
    #
    #         # 检查object碰撞
    #         if MOD.check_object_collision(self.player, self.objects):
    #             pass
    #
    #         # 更新技能锁
    #         self.update_magic_lock()
    #
    #         # 检查传送碰撞
    #         self.check_tp()
    #
    #         # 处理按钮事件
    #         if self.menu_button.Active():
    #             self.game.ispaused = True
    #             self.pauseMenu.run()
    #             self.game.ispaused = False
    #         # 暂停游戏
    #         if self.game.ispaused:
    #             self.pauseMenu.run()
    #             self.game.ispaused = False
    #
    #         # 检查游戏胜利
    #         self.check_game_win()

    # 游戏主循环
    
    def run(self):
        self.playing = True
        while self.playing:
            self.reset_player_status()
            # 控制游戏速度
            self.game.clock.tick(FPS)
            # 获取事件
            for event in pg.event.get():
                # 退出游戏
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    MOD.QUIT()
                # 处理事件
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.ispaused = True
                    if event.key == pg.K_f:
                        self.is_display_rect_borders = not self.is_display_rect_borders
                    if event.key == pg.K_p:
                        self.is_display_player_position = not self.is_display_player_position
            # 处理按钮事件
            if self.menu_button.Active():
                self.game.ispaused = True
                self.pauseMenu.run()
                self.game.ispaused = False
            # 暂停游戏
            if self.game.ispaused:
                self.pauseMenu.run()
                self.game.ispaused = False
            keys = pg.key.get_pressed()
            mouses = pg.mouse.get_pressed()

            self.update(keys, mouses)
            self.draw()
            pg.display.flip()

    def update(self, keys, mouses):
        self.player.update(keys, mouses)
        if self.player.hp <= 0:
            self.gameover()
        self.update_player_stats()
        self.camera.update(self.player)
        # 检查传送碰撞
        self.check_tp()
        # 检查npc碰撞
        if self.check_npc_collision():
            if self.npc.name == "Eilin":
                self.game.cure_lock = False
                if self.npc_plot.active:
                    self.npc_plot.play_plot()
            elif self.npc.name == "Renault":
                self.game.magic_lock = False
                if self.npc_plot.active:
                    self.npc_plot.play_plot()
        # 更新技能锁
        self.update_magic_lock()
        # 检查object碰撞
        if MOD.check_object_collision(self.player, self.objects):
            pass
        # 更新玩家技能特效
        for sprite in list(self.player_magic):
            sprite.update()
        # 更新敌人
        for enemy in self.enemies:
            enemy.update()
            enemy.blood.update()
        # 更新魔法
        for sprite in list(self.enemymagic):
            if sprite.active:
                sprite.update()
        # 在小怪类中有检查生命值，并且自己投递废物(子类以及自身)投到garbage_bin行为
        for garbage in list(self.garbage_bin):
            garbage.kill()
        for prop in self.prop:
            prop.update()
        # 更新npc
        for sprite in self.npcs:
            sprite.update_animation()
        # 检查游戏胜利
        self.check_game_win()

    def draw(self):
        # 画图
        self.screen.fill((0, 0, 0))
        MOD.draw_background(self.levelnum, self.backgrounds, self.screen, self.camera.view.x)
        for sprite in self.decoration:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.obstacles:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.water:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.npcs:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.objects:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        # 画角色
        self.game.screen.blit(self.player.image, self.camera.apply(self.player))
        # 绘制敌人
        for enemy in list(self.enemies):  # 使用list创建副本来遍历
            if enemy.active:
                self.game.screen.blit(enemy.image, self.camera.apply(enemy))
                enemy.blood.update()
        # 画npc
        for sprite in self.npcs:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        # 绘制玩家技能特效
        for sprite in list(self.player_magic):
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        # 绘制敌人魔法效果
        for sprite in list(self.enemymagic):  # 使用list创建副本来遍历
            if sprite.active:
                self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        for prop in self.prop:
            if prop.active:
                self.game.screen.blit(prop.image, self.camera.apply(prop))
        # 静态图像最后画
        self.display_lv()
        self.display_hp()
        self.display_mp()
        self.display_cure_state()
        self.display_magic_state()
        self.display_boss_hp()
        self.menu_button.draw()
        if self.is_display_rect_borders:
            self.draw_rect_borders()
        if self.is_display_player_position:
            self.display_player_position()

    # 检查游戏胜利
    def check_game_win(self):
        if not self.enemies.sprites():
            if self.levelnum==1 or self.levelnum==2 or self.levelnum==3 or self.levelnum==4:
                if MOD.check_fraction_collision(self.player,self.fractions):
                    MOD.play_levelup_sound()
                    self.gamewin()
            else:
                MOD.play_levelup_sound()
                self.gamewin()

    # 加载npc
    def load_npc(self):
        if self.levelnum == 2:
            self.npc = Eilin(self)
            self.npcs.add(self.npc)
            MOD.set_position(self.npc,EILIN_POSITION[0],EILIN_POSITION[1])
            self.npc_plot = Plot_Eilin(self)
        elif self.levelnum == 3:
            self.npc = Renault(self)
            self.npcs.add(self.npc)
            MOD.set_position(self.npc,RENAULT_POSITION[0],RENAULT_POSITION[1])
            self.npc_plot = Plot_Renault(self)

    # 检查npc碰撞
    def check_npc_collision(self):
        for npc in self.npcs:
            if npc.check_collision():
                return True
        return False

    # 更新技能锁
    def update_magic_lock(self):
        self.magic_lock = self.game.magic_lock
        self.cure_lock = self.game.cure_lock
        self.player.magic_lock = self.magic_lock
        self.player.cure_lock = self.cure_lock

    # 检查传送碰撞
    def check_tp(self):
        if self.levelnum == 1:
            return
        width = self.player.width
        height = self.player.height
        if self.levelnum == 2:
            tp_gate = pg.Rect(TP_GATE_LEVEL2[0],TP_GATE_LEVEL2[1],width,height)
            target = TP_TARGET_LEVEL2
        elif self.levelnum == 3:
            tp_gate = pg.Rect(TP_GATE_LEVEL3[0],TP_GATE_LEVEL3[1],width,height)
            target = TP_TARGET_LEVEL3
        elif self.levelnum == 4:
            tp_gate = pg.Rect(TP_GATE_LEVEL4[0],TP_GATE_LEVEL4[1],width,height)
            target = TP_TARGET_LEVEL4
        elif self.levelnum == 5:
            tp_gate = pg.Rect(TP_GATE_LEVEL5[0],TP_GATE_LEVEL5[1],width,height)
            target = TP_TARGET_LEVEL5
        if self.player.rect.colliderect(tp_gate):
            self.player.rect.x = target[0]
            self.player.rect.y = target[1]
            self.camera.update(self.player)

class Camera:
    def __init__(self, x, y, width, height,mapwidth,mapheight):
        self.view = pg.Rect(x, y, width, height)  # (x,y)是视野的左上角（世界坐标）,并且取符号
        self.width = width
        self.height = height
        self.mapwidth=mapwidth
        self.mapheight = mapheight
    def apply(self, entity):  # 将sprite对象的世界坐标转换为摄像机（屏幕）的相对坐标
        return entity.rect.move(self.view.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)  # 让目标居中
        y = -target.rect.centery + int(HEIGTH / 2)

        # 限制摄像机范围在地图内
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.mapwidth - self.width), x)
        y = max(-(self.mapheight - self.height), y)

        self.view = pg.Rect(x, y, self.width, self.height)

class Level1(Level):
    def __init__(self,game):
        super().__init__(game,1)
        self.resetplayer()

    def resetplayer(self):
        self.player.setgroup(self)
        MOD.set_position(self.player, LEVEL1_START_POSITION[0], LEVEL1_START_POSITION[1])  # 角色默认位置设置，否则以地图中角色位置为准
        self.camera.update(self.player)

class Level2(Level):
    def __init__(self,game):
        super().__init__(game,2)
        self.resetplayer()

    def resetplayer(self):
        self.player.setgroup(self)
        MOD.set_position(self.player, LEVEL2_START_POSITION[0], LEVEL2_START_POSITION[1])  # 角色默认位置
        self.camera.update(self.player)

class Level3(Level):
    def __init__(self,game):
        super().__init__(game,3)
        self.resetplayer()

    def resetplayer(self):
        self.player.setgroup(self)
        MOD.set_position(self.player, LEVEL3_START_POSITION[0], LEVEL3_START_POSITION[1])  # 角色默认位置
        self.camera.update(self.player)

class Level4(Level):
    def __init__(self,game):
        super().__init__(game,4)
        self.resetplayer()

    def resetplayer(self):
        self.player.setgroup(self)
        MOD.set_position(self.player, LEVEL4_START_POSITION[0], LEVEL4_START_POSITION[1])  # 角色默认位置
        self.camera.update(self.player)

class Level5(Level):
    def __init__(self,game):
        super().__init__(game,5)
        self.resetplayer()

    def resetplayer(self):
        self.player.setgroup(self)
        MOD.set_position(self.player, LEVEL5_START_POSITION[0], LEVEL5_START_POSITION[1])  # 角色默认位置
        self.camera.update(self.player)

class Npc(pg.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        self.frames = None
        self.frame_index = 0
        self.image = None
        self.rect = None
        self.lt = 0

    def check_collision(self):
        if self.rect.colliderect(self.game.player.rect):
            return True
        return False

class Eilin(Npc):
    def __init__(self,game):
        super().__init__()
        self.path = EILIN_PATH
        self.frames = []
        self.framenums = 9
        self.load_frames()
        self.game = game
        self.rect = pg.Rect(0,0,80,96)
        self.screen = self.game.screen
        self.image = self.frames[0]
        self.lt = 0
        self.name = "Eilin"

    def load_frames(self):
        for i in range(self.framenums):
            img = pg.image.load(f"{self.path}\\Idle{i+1}.png").convert_alpha()
            img = pg.transform.scale(img, (80, 96))
            self.frames.append(img)

    def update_animation(self):
        duration = 100
        ct = pg.time.get_ticks()
        if ct - self.lt > duration:
            self.frame_index = (self.frame_index + 1) % self.framenums
            self.lt = ct
        self.image = self.frames[self.frame_index]

class Renault(Npc):
    def __init__(self,game):
        super().__init__()
        self.path = RENAULT_PATH
        self.frames = []
        self.framenums = 6
        self.load_frames()
        self.game = game
        self.rect = pg.Rect(0,0,80,96)
        self.screen = self.game.screen
        self.image = self.frames[0]
        self.lt = 0
        self.name = "Renault"

    def load_frames(self):
        for i in range(self.framenums):
            img = pg.image.load(f"{self.path}\\Idle{i+1}.png").convert_alpha()
            img = pg.transform.scale(img, (80, 96))
            self.frames.append(img)
    
    def update_animation(self):
        duration = 100
        ct = pg.time.get_ticks()
        if ct - self.lt > duration:
            self.frame_index = (self.frame_index + 1) % self.framenums
            self.lt = ct
        self.image = self.frames[self.frame_index]

class Plot:
    def __init__(self,game):
        self.plots = []
        self.plot_index = 0
        self.gallery_img = pg.image.load(GALLERY_PATH).convert_alpha()
        self.gallery_img = pg.transform.scale(self.gallery_img, GALLERY_SCALE)
        self.gallery_rect = self.gallery_img.get_rect()
        self.gallery_rect.center = (WIDTH // 2, HEIGTH // 2)
        self.font = pg.font.Font(FONT, GALLERY_TEXT_SIZE)
        self.lt = 0
        self.duration = GALLERY_TEXT_DURATION
        self.game = game
        self.screen = self.game.screen
        self.active = True
        self.text_rect = pg.Rect(self.gallery_rect.x+50,self.gallery_rect.y+50,500,300)

    def play_plot(self):
        while self.active:
            self.screen.blit(self.gallery_img, self.gallery_rect)
            current_time = pg.time.get_ticks()
            # 更新对话
            if current_time - self.lt > self.duration:
                self.plot_index = self.plot_index + 1
                self.lt = current_time
                if self.plot_index == len(self.plots):
                    self.active = False
                    break
            # 显示当前对话
            lines = self.plots[self.plot_index].split("\n")
            y = self.text_rect.y
            for line in lines:
                self.screen.blit(self.font.render(line, True, BLACK), (self.text_rect.x, y))
                y += 30
            
            pg.display.flip()
            # 如果对话结束，退出循环
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MOD.QUIT()

class Plot_Eilin(Plot):
    def __init__(self,game):
        super().__init__(game)
        self.plots = EILIN_PLOT_TEXTS
        self.plot_index = 0

class Plot_Renault(Plot):
    def __init__(self,game):
        super().__init__(game)
        self.plots = RENAULT_PLOT_TEXTS
        self.plot_index = 0
