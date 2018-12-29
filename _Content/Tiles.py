

if __name__ == '__main__':
    from _Content.Main import *


class TileSet(pygame.sprite.Sprite):
    def __init__(self):
        super(TileSet, self).__init__()
        self.image = pygame.image.load('background_scifigame.png').convert()
        self.rect = self.image.get_rect()
        self.PosY = 0
        self.rel_y = self.PosY % self.rect.height

    def setBgnd(self):
        self.rel_y = self.PosY % self.rect.height
        screen.blit(self.image, (0, self.rel_y - self.rect.height))
        if self.rel_y < screen_height:
            screen.blit(self.image, (0, self.rel_y))
        self.PosY += 0.4
