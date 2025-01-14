import pygame
import random
from settings import *
import math
from lib import MOD
from lib.monsters.life_bar import lifebar

class Firegiant(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)

        self.is_berzerk = False #berzerk for not
        self.name="Firegiant"
        self.scale= (100,200)
        self.game = game
        self.statussheet = {
            "stractstart": "src/monsters/firegiant/fire_stract_start.png",
            "stractend": "src/monsters/firegiant/fire_stract_end.png",
            "walk": "src/monsters/firegiant/fire_walk.png",
            "firetoward": "src/monsters/firegiant/fire_open_toward.png",
            "death": "src/monsters/firegiant/fire_death.png",
            "birth": "src/monsters/firegiant/fire_birth.png",
            "crazystart": "src/monsters/firegiant/fire_fire_start.png",
            "crazyend": "src/monsters/firegiant/fire_fire_end.png",
            "fireup": "src/monsters/firegiant/fire_open_up.png",
            "firedown": "src/monsters/firegiant/fire_open_down.png"
        }
        self.lstatusani = {"walk": [], "stractstart": [], "stractend": [],"firetoward":[], "death":[], "birth":[], "crazystart":[], "crazyend":[], "fireup":[], "firedown":[]}
        self.rstatusani = {"walk": [], "stractstart": [], "stractend": [], "firetoward":[], "death":[], "birth":[], "crazystart":[], "crazyend":[], "fireup":[], "firedown":[]}
        self.framenums = {"walk": 7, "stractstart": 7, "stractend": 7, "firetoward":5, "death":7, "birth":16, "crazystart":5, "crazyend":5, "fireup":5, "firedown":5}
        self.load_frames()

        self.anim_finished = True
        self.attacking = False  # 添加攻击状态标记
        self.first_update = True #第一次更新

        self.cf = 0  # 当前帧
        self.lt = pygame.time.get_ticks()  # 上次更新时间
        self.status = "walk"
        self.blood = lifebar(self)

        # 基础属性
        self.image = self.lstatusani[self.status][self.cf]
        self.rect = self.image.get_rect()
        self.rect.x = 800  # 初始位置
        self.rect.y = 400
        self.width = self.rect.width
        self.height = self.rect.height
        self.onground = False
        # 战斗属性
        self.hp = 500
        self.max_hp = 500
        self.atk = 40
        self.active = True
        self.facing_left = False

        # 分离不同技能的冷却时间和计时器
        self.stract_cd = 15000
        self.fireopen_cd = 9000#三种火焰共用一个时间

        
        self.last_stract = 0  # stract的上次使用时间
        self.last_fireopen = 0  # fireopen的上次使用时间

        # 行为控制
        self.attack_range = 300
        self.detect_range = 500
        self.last_attack = 0
        self.speedx = 2
        self.vx = 0
        self.vy = 0
        # 创建遮罩
        self.mask = pygame.mask.from_surface(self.image)


    def load_frames(self):
    # 辅助函数：加载某一状态的动画帧
        def load_animation_frames(sheet_path, frame_count, width_per_frame, height_per_frame, scale_size):
            sheet = pygame.image.load(sheet_path).convert_alpha()
            width = sheet.get_width()
            height = sheet.get_height()
            
            frames = []
            frames_per_row = width // width_per_frame
            frames_per_column = height // height_per_frame
            
            for i in range(frame_count):
                row = i // frames_per_row
                col = i % frames_per_row
                
                if row >= frames_per_column:
                    break
                
                x = col * width_per_frame
                y = row * height_per_frame
                
                img = sheet.subsurface(pygame.Rect(x, y, width_per_frame, height_per_frame))
                img = pygame.transform.scale(img, scale_size)
                frames.append(img)
            
            return frames

        for status, sheet_path in self.statussheet.items():
            num_frames = self.framenums[status]
            sheet = pygame.image.load(sheet_path).convert_alpha()
            width = sheet.get_width()
            height = sheet.get_height()

            if status == "birth":
                frames = load_animation_frames(sheet_path, num_frames, width // 4, height // 4, self.scale)
            elif status in ["walk", "stractstart", "stractend", "death", "firetoward","crazystart","crazyend", "fireup", "firedown"]:
                frames = load_animation_frames(sheet_path, num_frames, width // num_frames, height, self.scale)

            self.lstatusani[status] = frames
            self.rstatusani[status] = [pygame.transform.flip(frame, True, False) for frame in frames]

    def target(self):
        # 在水平方向上追踪,update_position中遇到障碍自动爬坡
        if self.game.player.rect.x < self.rect.x:
            self.direction = -1
        else:
            self.direction = 1
        self.vx = self.direction * self.speedx

    def check_player_distance(self):
        player = self.game.player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)
        self.facing_left = dx > 0
        return dist
    
    def update_animation(self):
        duration = 200
        ct = pygame.time.get_ticks()

        if self.anim_finished:
            # 如果当前是狂暴状态，检查是否从开始到结束的动画播放完成
            if self.status == "crazystart":
                self.status = "crazyend"
                self.attacking = True
                self.cf = 0
                self.anim_finished = False

            elif self.status == "crazyend":
                # 狂暴结束后回到走路状态
                self.status = "walk"
                self.attacking = False
                self.anim_finished = True

            elif self.status == "stractstart":
                self.status = "stractend"
                self.attacking = True
                self.cf = 0
                self.anim_finished = False
            elif self.status == "death" and self.cf == len(self.lstatusani["death"]) - 1:
                self.anim_finished = True  # 确保死亡动画播放完

        if ct - self.lt > duration:
            self.cf = (self.cf + 1) % len(self.lstatusani[self.status])
            
            # 检查动画是否完成
            if self.cf == 0:
                self.anim_finished = True
                # 如果是攻击动画完成，恢复到idle状态
                if self.status in ["stractstart", "firetoward","fireup", "firedown"]:
                    self.status = "walk"
                    self.attacking = False
            else:
                self.anim_finished = False
                
            self.lt = ct
        if 0 <= self.cf < len(self.lstatusani[self.status]):
            if self.facing_left:
                self.image = self.lstatusani[self.status][self.cf]
            else:
                self.image = self.rstatusani[self.status][self.cf]
                
        self.game.screen.blit(self.image,self.rect)
        self.mask = pg.mask.from_surface(self.image)
#攻击逻辑
    def attack_player(self):
        dist = self.check_player_distance()
        if dist > 150:  # 远程攻击（熔岩冲击）
            self.impact_stract()
            if self.is_berzerk == False:
                self.speedx = 2
            else:
                self.speedx = 3
        else:  # 近战攻击（火焰喷射）
            self.fire_attack()
    def impact_stract(self):
        if self.attacking:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_stract < self.stract_cd:
            return
            
        self.status = "stractstart"
        self.attacking = True
        self.cf = 0  # 重置动画帧
        self.anim_finished = False

        self.speedx = 10

        attack_rect = pygame.Rect(self.rect.x - 20, self.rect.y - 20, self.rect.width + 40, self.rect.height + 40)

        if attack_rect.colliderect(self.game.player.rect):
            self.game.player.play_hurt_sound()
            self.game.player.hp -= 75

        if MOD.Check_Tile_Collision_no_direction(self,self.game.obstacles):
            self.kill()        

        self.last_stract = current_time

    def fire_attack(self):

        if self.attacking or pygame.time.get_ticks()- self.last_fireopen < self.fireopen_cd:
            return

            
        # 火焰喷射，根据方向选择图像
        if self.game.player.rect.x < self.rect.y:
            self.status = "firetoward"  # openfire toward
        elif self.game.player.rect.y > self.rect.y:
            self.status = "firedown"  # open fire down
        else:
            self.status = "fireup"  # open fire up
        self.check_hit()

        self.attacking = True
        self.cf = 0  # 重置动画帧
        self.anim_finished = False
        self.last_fireopen = pygame.time.get_ticks()

    def check_hit(self):
        if self.anim_finished and self.rect.colliderect(self.game.player.rect):
            self.game.player.hp -= self.atk
            self.game.player.play_hurt_sound()

    def update_position(self):
        self.target()
        MOD.Apply_gravity(self,GRAVITY)
        dist = self.check_player_distance()
        if dist < self.detect_range:
            direction = -1 if self.game.player.rect.x < self.rect.x else 1
            self.vx = direction * self.speedx
        else:
            self.status = "walk"

        dx = self.vx
        dy = self.vy
        dx, dy = MOD.Check_Tile_Collision(self, self.game.obstacles, dx, dy)
        self.rect.x += dx
        self.rect.y += dy

    def kill(self):
        self.active = False
        self.game.enemies.remove(self)
        super().kill()


    def isalive(self):
        if self.hp <= 0 and self.status == "death" and self.anim_finished:
            return False
        return self.hp > 0

    
    def setposition(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if not self.active or self.hp <= 0:
            self.kill()
            return

        # 确保出生动画只播放一次
        if self.first_update:
            self.status = "birth"
            self.first_update = False
            self.anim_finished = False  # 确保出生动画还没有完成

        #检查是否狂暴
        if self.hp < self.max_hp * 0.3 and not self.is_berzerk:
            self.is_berzerk = True
            self.status = "crazystart"
            self.speedx *= 1.5  # 狂暴状态下移动速度加快
            self.atk = 40 * 1.5  # 狂暴状态伤害加成

        dist = self.check_player_distance()
        self.update_position()
        # 状态机逻辑
        if self.anim_finished:
            if dist <= self.attack_range:
                self.attack_player()
            else:
                if self.first_update:
                    self.status = "birth"
                    self.first_update = False
                else:
                    self.status = "walk"
        self.blood.update()
        self.update_animation()
        MOD.ensure_entity_in_screen(self)