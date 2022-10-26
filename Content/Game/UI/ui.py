import pygame

from Content.Game.Settings.config import Cfg
from Content.Game.Main import main

class EnergyBar(pygame.sprite.Sprite):
    def __init__(self):
        super(EnergyBar, self).__init__()
        self.energyMax = 100
        self.energyCur = self.energyMax
        self.energyMin = 0
        self.energyDrain = 5
        self.energyRecharge = 0.3
        self.image = pygame.Surface((100, 15))
        self.rect = self.image.get_rect()
        self.image.fill(Cfg.white)
        self.rect.center = (Cfg.half_width / 3, 700)
        self.color = Cfg.green
        self.overload = False
        self.cooldown = 1000
        #print(os.getcwd())  # Log this line.
        self.overload_soundfx = pygame.mixer.Sound(R'C:\Users\danie\PycharmProjects\Space-shooter-game\sound_fx'
                                                   R'\354049__pauldihor__gun-fire-for-futuristic-game.wav')

    def draw_bar(self):
        self.update_bar()
        pygame.draw.rect(Cfg.screen, self.color, [self.rect.x, self.rect.y, self.energyCur, 15])

    def update_bar(self):

        if not self.overload:
            if self.energyCur >= self.energyMax:
                self.energyRecharge = 0.3

            if self.energyCur < self.energyMax:
                self.energyDrain = 5
                self.energyCur += self.energyRecharge
                self.color = Cfg.green

            if self.energyCur <= int(self.rect.width / 2):
                self.color = Cfg.orange
                self.energyDrain = 10

            if self.energyCur <= int(self.rect.width / 3):
                self.color = Cfg.red

            if self.energyCur <= self.energyMin:
                self.overload = True
        else:
            if self.cooldown > 0:

                self.overload_soundfx.play()
                main.text_to_screen('Overload!', color=Cfg.red)
                self.cooldown -= 25
            else:
                self.cooldown = 1000
                self.overload = False
                self.energyRecharge = 1
                self.update_bar()


