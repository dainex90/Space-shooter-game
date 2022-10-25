import pygame
from Content.Game.Settings.config import Cfg

class TileSet(pygame.sprite.Sprite):
    def __init__(self):
        super(TileSet, self).__init__()
        self.image = pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites'
                                       R'\Tiles\background_scifigame.png').convert()
        self.rect = self.image.get_rect()
        self.PosY = 0
        self.rel_y = self.PosY % self.rect.height

    def set_bgnd(self):
        self.rel_y = self.PosY % self.rect.height
        Cfg.screen.blit(self.image, (0, self.rel_y - self.rect.height))
        if self.rel_y < Cfg.screen_height:
            Cfg.screen.blit(self.image, (0, self.rel_y))
        self.PosY += 0.6
