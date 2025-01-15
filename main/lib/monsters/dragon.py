import pygame as pg
from settings import *
import math
from lib import MOD
from lib.monsters.life_bar import lifebar
import random
class Dragon(pg.sprite.Sprite):
    def __init__(self,game):
        self.name = "Dragon"
        self.game = game
        pg.sprite.Sprite.__init__(self) 
        # 基本属性
        self.hp = DRAGON_MAXHP
        self.max_hp = DRAGON_MAXHP
        self.atk = DRAGON_ATK
        self.speedx = DRAGON_SPEEDX
        self.vy = 0
        self.vx = self.speedx
        self.isalive = True
        self.onground = False
        self.facing_left = True

        # 攻击相关
        self.attack_radius = DRAGON_ATTACK_RADIUS  # 攻击范围
        self.notice_radius = DRAGON_NOTICE_RADIUS  # 发现玩家范围
        self.min_distance = DRAGON_MIN_DISTANCE
        self.can_attack = True
        self.attack_cooldown = DRAGON_ATTACK_COOLDOWN  # 攻击冷却时间(毫秒)
        self.last_attack = 0
        self.atk1_range = DRAGON_ATK1_RANGE
        self.atk2_ready = True
        self.atk2_timer = pg.time.get_ticks()  # 添加计时器


        self.anim_finished = True
        self.active = True

        self.scale = DRAGON_SCALE
        self.statussheet = {
            "idle":DRAGON_IDLE_PATH,
            "walk":DRAGON_WALK_PATH,
            "atk1":DRAGON_ATK1_PATH,
            "atk2":DRAGON_ATK2_PATH,
            "atk3":DRAGON_ATK3_PATH,
        }
        self.lstatusani = {"idle": [], "walk": [], "atk1": [], "atk2": [], "atk3": []}
        self.rstatusani = {"idle": [], "walk": [], "atk1": [], "atk2": [], "atk3": []}
        self.framenums = {"idle": 1, "walk": 1, "atk1": 4, "atk2": 12, "atk3": 26}
        self.load_frames()
        self.cf = 0  # 当前帧
        self.lt = pg.time.get_ticks()  # 上次更新时间
        self.status = "idle"
        self.prev_status = "idle"  # 添加前一个状态的记录
        self.attacking = False  # 添加攻击状态标记

        self.image = self.lstatusani[self.status][self.cf]
        self.rect = pg.Rect(0,0,256,256)
        self.rect.center = (100, 100)
        

        self.mask = pg.mask.from_surface(self.image)

        self.fireball_count = DRAGON_ATK2_FIREBALL_NUM  
        # 火球数量
        
        # 分离不同技能的冷却时间和计时器
        self.atk1_cd = DRAGON_ATK1_CD
        self.atk2_cd = DRAGON_ATK2_CD
        self.atk3_cd = DRAGON_ATK3_CD
        
        self.last_atk1 = 0  # atk1的上次使用时间
        self.last_atk2 = 0  # atk2的上次使用时间
        self.last_atk3 = 0  # atk3的上次使用时间
        
        self.atk2_ready = True

        self.blood = lifebar(self)
    def load_frames(self):
        for status in self.statussheet:
            sheet = pg.image.load(self.statussheet[status]).convert_alpha()
            width = sheet.get_width()
            height = sheet.get_height()
            if status == "idle":
                img = sheet
                img = pg.transform.scale(img,self.scale)
                self.lstatusani[status].append(img)
                self.rstatusani[status].append(pg.transform.flip(img,True,False))
            elif status == "walk":
                img = sheet
                img = pg.transform.scale(img,self.scale)
                self.lstatusani[status].append(img)
                self.rstatusani[status].append(pg.transform.flip(img,True,False))
            elif status == "atk1":
                wpf = width / 3
                hpf = height / 2
                for i in range(self.framenums[status]):
                    x = i % 3 * wpf
                    y = i // 3 * hpf
                    img = sheet.subsurface(x,y,wpf,hpf)
                    img = pg.transform.scale(img,self.scale)
                    self.lstatusani[status].append(img)
                    self.rstatusani[status].append(pg.transform.flip(img,True,False))
            elif status == "atk2":
                wpf = width / 3
                hpf = height / 4
                for i in range(self.framenums[status]):
                    x = i % 3 * wpf
                    y = i // 3 * hpf
                    img = sheet.subsurface(x,y,wpf,hpf)
                    img = pg.transform.scale(img,self.scale)
                    self.lstatusani[status].append(img)
                    self.rstatusani[status].append(pg.transform.flip(img,True,False))
            elif status == "atk3":
                wpf = width / 3
                hpf = height / 9
                for i in range(self.framenums[status]):
                    x = i % 3 * wpf
                    y = i // 3 * hpf
                    img = sheet.subsurface(x,y,wpf,hpf)
                    img = pg.transform.scale(img,self.scale)
                    self.lstatusani[status].append(img)
                    self.rstatusani[status].append(pg.transform.flip(img,True,False))

    def update_animation(self):
        duration = 100
        ct = pg.time.get_ticks()
        if ct - self.lt > duration:
            self.cf = (self.cf + 1) % len(self.lstatusani[self.status])
            
            # 检查动画是否完成
            if self.cf == 0:
                self.anim_finished = True
                # 如果是攻击动画完成，恢复到idle状态
                if self.status in ["atk1", "atk2", "atk3"]:
                    self.status = "idle"
                    self.attacking = False
            else:
                self.anim_finished = False
                
            self.lt = ct
            
        if self.facing_left:
            self.image = self.lstatusani[self.status][self.cf]
        else:
            self.image = self.rstatusani[self.status][self.cf]
            
        self.game.screen.blit(self.image,self.rect)
        self.mask = pg.mask.from_surface(self.image)

    def update_status(self):
        # 更新朝向
        if self.game.player.rect.x < self.rect.x:
            self.facing_left = True
        else:
            self.facing_left = False

        # 检查atk2是否冷却完成
        current_time = pg.time.get_ticks()
        if not self.atk2_ready and current_time - self.last_atk2 >= self.atk2_cd:
            self.atk2_ready = True
            
        # 如果不在攻击状态且动画完成，切换到idle
        if not self.attacking and self.anim_finished:
            self.status = "idle"

    def check_player_distance(self):
        player = self.game.player
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = math.sqrt(dx**2 + dy**2)
        return dist
    # 近身攻击
    def atk1(self):
        if self.attacking:
            return
            
        current_time = pg.time.get_ticks()
        if current_time - self.last_atk1 < self.atk1_cd:
            return
            
        if self.check_player_distance() > self.atk1_range:
            return
            
        self.status = "atk1"
        self.attacking = True
        self.cf = 0  # 重置动画帧
        self.anim_finished = False
        
        # 创建攻击圆形范围
        attack_center = self.rect.center
        attack_radius = self.atk1_range/2
        
        # 计算玩家中心点是否在攻击圆内
        player_center = self.game.player.rect.center
        dx = player_center[0] - attack_center[0]
        dy = player_center[1] - attack_center[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # 如果玩家在攻击范围内则造成伤害
        if distance <= attack_radius:
            self.game.player.hp -= self.atk
            self.game.player.play_hurt_sound()
            
        # 绘制攻击范围（调试用）
        # pg.draw.circle(self.game.screen, (255,0,0), attack_center, attack_radius, 2)
        
        self.last_atk1 = current_time
    # 直线火球攻击
    def atk3(self):
        if self.attacking:
            return
            
        current_time = pg.time.get_ticks()
        if current_time - self.last_atk3 < self.atk3_cd:
            return
            
        self.status = "atk3"
        self.attacking = True
        self.cf = 0  # 重置动画帧
        self.anim_finished = False
        
        self.fireball2 = Fireball2(self)
        self.fireball2.active = True
        self.game.enemymagic.add(self.fireball2)
        self.fireball2.facing_left = self.facing_left
        self.last_atk3 = current_time

    # 全屏火球攻击
    def atk2(self):
        if self.attacking:
            return
            
        self.status = "atk2"
        self.attacking = True
        self.cf = 0
        self.anim_finished = False
        self.atk2_ready = False
        self.last_atk2 = pg.time.get_ticks()
        
        # 计算每个火球之间的水平间距
        screen_margin = 100  # 距离屏幕边缘的边距
        spacing = (WIDTH - 2 * screen_margin) / (self.fireball_count - 1) + 50 # 计算间距
        
        # 创建火球
        self.fireballs = []
        for i in range(self.fireball_count):
            fireball = Fireball(self)
            # 设置火球初始位置
            x_pos = self.game.player.rect.x - 200 + (i * spacing)  # 均匀分布的x坐标
            fireball.rect.centerx = x_pos
            fireball.rect.top = -50  # 从屏幕上方开始
            
            self.fireballs.append(fireball)
            fireball.active = True
            self.game.enemymagic.add(fireball)


    def attack(self):
        current_time = pg.time.get_ticks()
        dist = self.check_player_distance()
        
        # 优先使用 atk2 (如果就绪)
        if self.atk2_ready:
            self.atk2()
            return
        
        # 根据距离选择 atk1 或 atk3
        if dist < self.atk1_range:
            if current_time - self.last_atk1 > self.atk1_cd:
                self.atk1()
        elif dist >= self.atk1_range and dist <= self.notice_radius:
            if current_time - self.last_atk3 > self.atk3_cd:
                self.atk3()

    def target(self):
        current_time = pg.time.get_ticks()
        self.track_space = 1500
        self.last_track = 0
        if current_time - self.last_track < self.track_space:
            return
        self.last_track = current_time
        # 在水平方向上追踪,update_position中遇到障碍自动爬坡
        if self.game.player.rect.x < self.rect.x:
            self.direction = -1
        else:
            self.direction = 1
        self.vx = self.direction * self.speedx

    def update_position(self):
        self.target()
        MOD.Apply_gravity(self, GRAVITY)  # 先根据重力来解决下落和上升
        dx = self.vx
        dy = self.vy
        dx, dy = MOD.Check_Tile_Collision(self, self.game.obstacles, dx, dy)  # 阻塞要跳起来的逻辑已经在
        dist = self.check_player_distance()
        if dist > self.notice_radius:
            dx = 0
            dy = self.vy
        self.rect.x += dx
        self.rect.y += dy

    def kill(self):
        self.active = False
        self.game.enemies.remove(self)
        super().kill()

    def update(self):
        if self.hp <= 0:
            self.kill()
        self.update_animation()
        self.update_status()
        self.update_position()
        self.attack()
        self.blood.update()
        MOD.ensure_entity_in_screen(self)

class Fireball(pg.sprite.Sprite):
    def __init__(self,monster):
        pg.sprite.Sprite.__init__(self)
        self.monster = monster
        self.image = pg.image.load(DRAGON_FIREBALL_PATH).convert_alpha()
        self.image = pg.transform.scale(self.image,ATK2_FIREBALL_SCALE)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.speedy = ATK2_SPEED_Y  # 增加下落速度
        self.player = monster.game.player
        self.atk = ATK2_FIREBALL_DAMAGE
        self.active = True
        self.born_time = pg.time.get_ticks()
        self.lifetime = ATK2_FIREBALL_LIFETIME  # 火球存活时间(ms)

    def check_hit(self):
        if self.rect.colliderect(self.player.rect):
            self.player.hp -= self.atk
            self.player.play_hurt_sound()
            self.kill()
        if MOD.Check_Tile_Collision_no_direction(self,self.monster.game.obstacles):
            self.kill()

    def kill(self):
        self.monster.game.enemymagic.remove(self)
        self.active = False
        super().kill()
    
    def update_position(self):
        self.rect.y += self.speedy
        
        # 检查是否超出屏幕或存活时间已到
        current_time = pg.time.get_ticks()
        if current_time - self.born_time > self.lifetime:
            self.kill()
    
    def update(self):
        if self.active:
            self.update_position()
            self.check_hit()


class Fireball2(pg.sprite.Sprite):
    def __init__(self,monster):
        pg.sprite.Sprite.__init__(self)
        self.monster = monster
        self.facing_left = monster.facing_left
        self.image = pg.image.load(DRAGON_FIREBALL_HORIZON_PATH).convert_alpha()
        self.images = {"left":self.image,
                       "right":pg.transform.flip(self.image,True,False)}
        if self.facing_left:
            self.image = self.images["left"]
        else:
            self.image = self.images["right"]
        self.rect = self.image.get_rect()
        self.rect.center = monster.rect.center
        self.speed = ATK3_FIREBALL_SPEED
        self.player = monster.game.player
        self.atk = ATK3_FIREBALL_DAMAGE
        self.isactive = True
        self.born_time = pg.time.get_ticks()
        self.lifetime = ATK3_FIREBALL_LIFETIME  # 火球存活时间(ms)

    def check_hit(self):
        if self.rect.colliderect(self.player.rect):
            self.player.hp -= self.atk
            self.player.play_hurt_sound()
            self.kill()

        if MOD.Check_Tile_Collision_no_direction(self,self.monster.game.obstacles):
            self.kill()


    def kill(self):
        self.monster.game.enemymagic.remove(self)
        self.isactive = False
        super().kill()
    
    def update_position(self):
        if self.facing_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    
    def update(self):
        if pg.time.get_ticks() - self.born_time > self.lifetime:
            self.kill() 
        if self.isactive:
            self.update_position()
            self.check_hit()

        