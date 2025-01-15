import pygame as pg
import sys
from settings import *
from lib.menus.StartMenu import StartMenu
from lib.Player import Player
import lib.MOD
from lib.menus.pauseMenu import pauseMenu
from lib.Levels import Level1,Level2,Level3,Level4,Level5
from lib.saves import files

class Game:
    # 初始化游戏类aaaa
    def __init__(self):
        # 关卡解锁状态
        self.level_Lock = {
            1: True,  # 第一关默认解锁
            2: False,
            3: False,
            4: False,
            5: True,
            6: False
        }

        # 技能锁
        self.magic_lock = True
        self.cure_lock = True
        
        self.playing = None
        pg.init()
        # 窗口
        self.screen = pg.display.set_mode((WIDTH, HEIGTH))
        # 标题
        pg.display.set_caption(TITLE)
        # 时钟
        self.clock = pg.time.Clock()
        #存档按钮
        self.files=files.files()
        self.files.game = self  # 添加对游戏实例的引用
        # 主菜单
        self.startMenu = StartMenu(self)
        # 音乐播放器
        pg.mixer.init()

        # 暂停状态
        self.ispaused = False
        self.pauseMenu = pauseMenu(self)

        # 记录玩家等级
        self.player_lv = 1

        # 关卡
        self.level1 = Level1(self)
        self.level2 = Level2(self)
        self.level3 = Level3(self)
        self.level4 = Level4(self)
        self.level5 = Level5(self)


if __name__ == '__main__':
    game = Game()
    game.startMenu.run()