import pygame as pg

class lifebar(pg.sprite.Sprite):
    def __init__(self, monster):
        super().__init__()
        self.monster = monster
        self.health_bar_height = 4
        self.health_bar_length = 60
        self.rect = pg.Rect(0, 0, self.health_bar_length, self.health_bar_height)
        
    def update(self):
        # 计算血条位置 - 放在怪物矩形正上方
        # 考虑相机偏移，直接计算屏幕上的位置
        monster_screen_rect = self.monster.game.camera.apply(self.monster)
        
        # 血条位置：居中于怪物上方
        bar_x = monster_screen_rect.centerx - self.health_bar_length // 2
        bar_y = monster_screen_rect.top - 10  # 在怪物上方10像素
        
        # 计算血条填充宽度
        self.fill_width = (self.monster.hp / self.monster.max_hp) * self.health_bar_length
        
        # 绘制血条背景(灰色)
        pg.draw.rect(self.monster.game.screen, (104, 100, 112),
                    (bar_x, bar_y, self.health_bar_length, self.health_bar_height))
        
        # 绘制血条填充部分(红色)
        if self.fill_width > 0:  # 只在血量大于0时绘制
            pg.draw.rect(self.monster.game.screen, (255, 0, 0),
                        (bar_x, bar_y, self.fill_width, self.health_bar_height))
