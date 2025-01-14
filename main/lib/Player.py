import pygame as pg
from lib import MOD
from settings import *

# 继承精灵类
class Player(pg.sprite.Sprite):

    def __init__(self, game):
        # 获取游戏状态
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.status = "idle"
        # 状态表
        self.statussheet = {"jumping": PLAYER_JUMP_SHEET_PATH,
                            "idle": PLAYER_IDLE_SHEET_PATH,
                            "walk": PLAYER_WALK_SHEET_PATH,
                            "attack": PLAYER_ATTACK_SHEET_PATH, }
        # 状态帧表
        self.statusani = {"jumping": [], "idle": [], "walk": [], "attack": []}
        self.framenums = {"jumping": 15, "idle": 4, "walk": 8, "attack": 8}
        self.load_frames()
        self.cf = 0  # 当前帧索引
        self.lt = pg.time.get_ticks()  # 储存上一次更新的时间
        #精灵组
        self.setgroup(self.game)
        # 移动方向
        self.movingleft = False
        self.isonground = False

        # 额外属性：控制动画切换
        self.anim_finished = True

        self.image = self.statusani[self.status][self.cf]
        self.rect = pg.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        # self.rect = self.image.get_rect()
        # 初始化位置
        self.rect.center = (WIDTH / 2, HEIGTH / 2)
        # 移动参数
        # 速度与加速度分量
        self.vx = 0
        self.vy = 0
        self.speed = SPEED

        self.lv = self.game.player_lv
        # 先初始化基础属性

        self.max_hp = MAXHP
        self.max_mp = MAXMP
        self.hp = self.max_hp  # 添加初始值
        self.mp = self.max_mp  # 添加初始值
        self.atk = ATK_PER_FAMRE
        self.attackrange = ATK_RANGE
        
        # 然后更新属性
        self.update_stats()

        # 创建遮罩
        self.mask = pg.mask.from_surface(self.image)

        self.atk_timer = pg.time.get_ticks()
        self.sounds = {"attack": None, "hurt": None, "cure": None, "error": None}
        self.load_sounds()
        # 回血术
        self.cure_cd = CURE_CD  # ms
        self.cure_timer = 0
        self.cure_ready = True
        # 魔法箭
        self.magic_arrow_cd = MAGIC_ARROW_CD
        self.magic_arrow_timer = 0
        self.magic_arrow_ready = True

        # 技能锁
        self.magic_lock = True
        self.cure_lock = True

    def setgroup(self, level):
        self.obstacles = level.obstacles
        self.enemies = level.enemies
        self.enemymagic = level.enemymagic
        self.objects = level.objects
        self.water = level.water

    # 加载帧
    def load_frames(self):
        for status, sheetpath in self.statussheet.items():
            sheet = pg.image.load(sheetpath).convert_alpha()
            width = sheet.get_width()
            heigth = sheet.get_height()
            num = self.framenums[status]
            wpf = width // num
            for i in range(num):
                img = sheet.subsurface(i * wpf, 0, wpf, heigth)
                self.statusani[status].append(img)

    def load_sounds(self):
        self.sounds["attack"] = pg.mixer.Sound(PLAYER_ATTACK_SOUND)
        self.sounds["hurt"] = pg.mixer.Sound(PLAYER_HURT_SOUND)
        self.sounds["cure"] = pg.mixer.Sound(PLAYER_CURE_SOUND)
        self.sounds["error"] = pg.mixer.Sound(ERROR_SOUND)

    def load_cure_img(self):
        sheet = pg.image.load(self.cure_imgpath).convert_alpha()
        width = sheet.get_width()
        height = sheet.get_height()
        wpf = width // self.cure_nums
        for i in range(self.cure_nums):
            x = i * wpf  # 修正：直接使用 i * wpf
            img = sheet.subsurface(x, 0, wpf, height)
            self.cure_frames.append(img)
        self.cure_rect = pg.Rect(0, 0, wpf, height)

    def attack(self):
        current_time = pg.time.get_ticks()
        if current_time - self.atk_timer < ATK_CD:
            return
        self.atk_timer = current_time
        self.sounds['attack'].play()
        # 绘制攻击范围矩形
        if not self.movingleft:
            attackrect = pg.Rect(self.rect.right, self.rect.top, self.attackrange, self.rect.height)
        else:
            attackrect = pg.Rect(self.rect.left - self.attackrange, self.rect.top, self.attackrange, self.rect.height)
        # 伤害判定
        for enemy in self.game.enemies:
            if attackrect.colliderect(enemy.rect):
                enemy.hp -= self.atk
                print(enemy.hp)

    # 处理输入
    def handle_input(self,keys=None,mouses=None):
        if keys == None:
            keys = pg.key.get_pressed()
        if mouses == None:
            mouses = pg.mouse.get_pressed()

        if keys[pg.K_a]:
            if not self.anim_finished:
                pass
            self.status = "walk"
            self.movingleft = True
            self.vx = -self.speed
        elif keys[pg.K_d]:
            if not self.anim_finished:
                pass
            self.status = "walk"
            self.movingleft = False
            self.vx = self.speed
        else:
            self.vx = 0

        if keys[pg.K_w]:
            if not self.anim_finished:
                pass
            self.status = "jumping"
            if self.isonground:
                self.vy = -JUMP_POWER
                self.isonground = False

        # 回血术
        if keys[pg.K_h]:
            self.health()

        # 魔法箭
        if keys[pg.K_g]:
            self.magic_arrow()

        if mouses[0]:
            if not self.anim_finished:
                pass
                self.status = "attack"
                self.attack()

    def play_hurt_sound(self):
        self.sounds["hurt"].play()

    def update_animation(self):
        # 一帧持续时间ms
        duration = 100
        # 记录当前时间
        ct = pg.time.get_ticks()

        # 更新帧
        if ct - self.lt > duration:
            self.cf = (self.cf + 1) % len(self.statusani[self.status])
            if self.cf >= len(self.statusani[self.status]):
                self.cf = 0  # 设置为初始帧
            # 如果当前状态动画播放完毕，标记动画完成
            if self.cf == 0:
                self.anim_finished = True
            else:
                self.anim_finished = False
            self.lt = ct

        self.image = self.statusani[self.status][self.cf % len(self.statusani[self.status])]
        if self.movingleft:
            self.image = pg.transform.flip(self.image, True, False)

        # 更新遮罩
        self.mask = pg.mask.from_surface(self.image)

    def health(self):
        if self.cure_lock:
            return
        if self.mp - CURE_COST_MP <= 0:
            self.sounds["error"].play()
            return
        if not self.cure_ready:
            return
        current_time = pg.time.get_ticks()
        self.cure_timer = current_time
        delta_hp = self.max_hp - self.hp
        delta_hp = delta_hp * 0.6
        self.hp += delta_hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.mp -= CURE_COST_MP
        self.sounds["cure"].play()
        self.cure_ready = False
    
    def magic_arrow(self):
        if self.magic_lock:
            return
        if self.mp - MAGIC_ARROW_COST_MP <= 0:
            return
        current_time = pg.time.get_ticks()
        if current_time - self.magic_arrow_timer < self.magic_arrow_cd:
            return
        self.magic_arrow_timer = current_time
        self.mp -= MAGIC_ARROW_COST_MP
        self.arrow = Magic_Arrow(self.game)
        self.game.player_magic.add(self.arrow)
        
    def check_magic_ready(self):
        current_time = pg.time.get_ticks()
        self.magic_arrow_ready = current_time - self.magic_arrow_timer <= self.magic_arrow_cd
        return self.magic_arrow_ready

    def update_position(self):

        # 引力判定
        if self.isonground:
            self.ay = 0
        else:
            self.ay = GRAVITY
        self.isonground = False

        # 位置更新
        dx = 0
        dy = 0

        # 最大速度限制

        if abs(self.vx) > MAXVX:
            if self.vx > 0:
                self.vx = MAXVX
            else:
                self.vx = - MAXVX

        # 应用摩擦因素
        if self.vx > 0:
            self.vx -= FRICTION
        elif self.vx < 0:
            self.vx += FRICTION

        self.vy += self.ay

        dx = self.vx
        dy = self.vy

        dx, dy = MOD.check_tile_collision(self, self.game.obstacles, dx, dy)
        self.rect.x += dx
        self.rect.y += dy
        self.mask = pg.mask.from_surface(self.image)

    # def handle_collide(self,dx,dy):
    #     for tile in self.obstacles:
    #         # x方向碰撞检测
    #         if tile.rect.colliderect(self.rect.x+dx ,self.rect.y ,self.width,self.height):
    #             dx = 0
    #         # y方向碰撞检测
    #         elif tile.rect.colliderect(self.rect.x ,self.rect.y+dy ,self.width,self.height):
    #             if dy <0:
    #                 dy = tile.rect.bottom - self.rect.top

    #             elif dy >=0:
    #                 dy = tile.rect.top - self.rect.bottom
    #                 self.isonground = True

            # rectdx = pg.Rect(self.rect.x+dx,self.rect.y,self.width,self.height)
            # rectdy = pg.Rect(self.rect.x,self.rect.y+dy,self.width,self.height)

            # # 计算玩家和障碍物的偏移量
            # xoffset_x = tile.rect.x - (rectdx.x)
            # xoffset_y = tile.rect.y - (rectdx.y)
            # # 检测 y 方向的遮罩碰撞
            # yoffset_x = tile.rect.x - rectdy.x
            # yoffset_y = tile.rect.y - rectdy.y
            # # 检测 x 方向的遮罩碰撞
            # if self.mask.overlap(tile.mask, (xoffset_x, xoffset_y)):
            #     dx = 0
            # elif self.mask.overlap(tile.mask, (yoffset_x, yoffset_y)):
            #     if dy < 0:
            #         dy = tile.rect.bottom - self.rect.top
            #     elif dy >= 0:
            #         dy = tile.rect.top - self.rect.bottom
            #         self.isonground = True
        # return dx,dy

    # 更新函数
    def update(self, keys=None, mouses=None):
        # 还原状态
        if self.anim_finished:
            self.status = "idle"

        # 处理输入
        self.handle_input(keys, mouses)
        # 处理更新动画
        self.update_animation()
        # 更新位置
        self.update_position()

        current_time = pg.time.get_ticks()
        if current_time - self.cure_timer >= self.cure_cd:
            self.cure_ready = True

        # 自然魔力恢复
        if self.mp < self.max_mp:
            self.mp += MP_RECOVER_SPEED
        if self.mp > self.max_mp:
            self.mp = self.max_mp

        return self.status
    
    def update_stats(self):
        """更新玩家属性"""
        self.max_hp = MAXHP * (1 + HPRATE_PER_LV * (self.lv - 1))
        self.max_mp = MAXMP * (1 + MPRATE_PER_LV * (self.lv - 1))
        self.atk = ATK_PER_FAMRE * (1 + ATKRATE_PER_LV * (self.lv - 1))
            
        # 确保当前HP/MP不超过最大值
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.mp > self.max_mp:
            self.mp = self.max_mp

class Magic_Arrow(pg.sprite.Sprite):

    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(PLAYER_MAGIC_ARROW_SHEET_PATH).convert_alpha()
        self.image = pg.transform.scale(self.image, (96, 64))
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center
        self.mask = pg.mask.from_surface(self.image)
        self.speed = MAGIC_ARROW_SPEED
        self.direction = 1 if not self.game.player.movingleft else -1
        self.atk = self.game.player.atk * MAGIC_ARROW_ATK_RATE
        self.lt = 0
        self.atk_range = MAGIC_ARROW_ATK_RANGE
        if self.direction == -1:
            self.image = pg.transform.flip(self.image, True, False)
    
    def kill(self):
        self.game.player_magic.remove(self)
        super().kill()

    def check_hit(self):
        for enemy in self.game.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.hp -= self.atk
        
        if MOD.Check_Tile_Collision_no_direction(self,self.game.obstacles):
            self.kill()
    
    def update_position(self):
        self.rect.x += self.speed * self.direction
        self.check_hit()
        distance = abs(self.rect.x - self.game.player.rect.x)
        if distance > self.atk_range:
            self.kill()
    
    def update(self):
        self.update_position()
        self.check_hit()

