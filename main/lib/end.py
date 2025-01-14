import pygame as pg
from settings import *
from lib import MOD

class EndPlot:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
        self.texts = END_PLOT_TEXTS
        self.during = 1500
        self.index = 0
        self.backgroundimg = pg.transform.scale(pg.image.load(STARTMENU_BACKGROUND).convert_alpha(),(WIDTH,HEIGTH))
        self.timer = 0

    def run(self):
        font = pg.font.Font(FONT,100)
        text = font.render(self.texts[self.index],True,WHITE)
        text_rect = text.get_rect(center=(WIDTH//2,HEIGTH//2))
        self.screen.blit(self.backgroundimg,(0,0))
        for text in self.texts:
            text = font.render(text,True,WHITE)
            text_rect = text.get_rect(center=(WIDTH//2,HEIGTH//2))
            alpha = 0
            fade_complete = False
            while not fade_complete:
                if alpha < 255:
                    alpha += 2
                    text.set_alpha(alpha)
                else:
                    fade_complete = True
                self.screen.blit(self.backgroundimg,(0,0))
                self.screen.blit(text,text_rect)
                pg.display.update()
            pg.time.delay(self.during)


