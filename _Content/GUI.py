
from _Content.Main import *


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
        self.image.fill(white)
        self.rect.center = (half_width/3, 700)
        self.color = green
        self.overload = False
        self.cooldown = 1000
        print(os.getcwd())  # Log this line.
        self.overload_soundfx = pygame.mixer.Sound('354049__pauldihor__gun-fire-for-futuristic-game.wav')

    def draw_bar(self):
        self.update_bar()
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.energyCur, 15])

    def update_bar(self):

        if not self.overload:
            if self.energyCur >= self.energyMax:
                self.energyRecharge = 0.3

            if self.energyCur < self.energyMax:
                self.energyDrain = 5
                self.energyCur += self.energyRecharge
                self.color = green

            if self.energyCur <= int(self.rect.width / 2):
                self.color = orange
                self.energyDrain = 10

            if self.energyCur <= int(self.rect.width / 3):
                self.color = red

            if self.energyCur <= self.energyMin:
                self.overload = True
        else:
            if self.cooldown > 0:

                self.overload_soundfx.play()
                texttoscreen('Overload!', color=red)
                self.cooldown -= 25
            else:
                self.cooldown = 1000
                self.overload = False
                self.energyRecharge = 1
                self.update_bar()
