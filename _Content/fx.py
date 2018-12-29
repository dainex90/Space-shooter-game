

from _Content.Main import *


class Effect(pygame.sprite.Sprite):

    """" Datastructure """
    all_effects = pygame.sprite.Group()

    def __init__(self):
        super(Effect, self).__init__()

        self.image = SCALED_EXPLOSION_FRAMES[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect.centerx = self.rect.x + self.rect.center[0]
        self.rect.centery = self.rect.y + self.rect.center[1]
        self.frame = -1

        self.asteroidExpframes = AST_EXP_SHEETS[0]
        self.astexp_rect = self.asteroidExpframes.get_rect()
        self.singleframe_width = self.astexp_rect.width / 4
        self.singleframe_height = self.astexp_rect.height / 4
        self.numImages = 16
        self.curImageX = 0
        self.curimageY = 0
        self.playerexp = False
        self.astexp = False
        self.enemyexp = False
        self.astPosX = 0
        self.astPosY = 0
        self.sheetType = 0

    def ast_exp(self, posX, posY):
        if self.astexp or self.playerexp or self.enemyexp:

            screen.blit(self.asteroidExpframes, (posX, posY),
                        (self.curImageX, self.curimageY, self.singleframe_width, self.singleframe_height))
            self.curImageX += self.singleframe_width
            if self.curImageX == self.astexp_rect.width:
                self.curImageX %= self.astexp_rect.width
                self.curimageY += self.singleframe_height
                if self.curimageY == self.astexp_rect.height:
                    self.curimageY %= self.astexp_rect.height
                    self.astexp = False
                    self.playerexp = False
                    self.enemyexp = False
                    if player.health <= 0:
                        game_over()


class Explosion(Effect):
    def __init__(self):
        super().__init__()


class Star(pygame.sprite.Sprite):

    all_stars = pygame.sprite.Group()

    def __init__(self):
        super(Star, self).__init__()

        self.image = pygame.Surface([1, 1])
        self.image.fill(white)
        self.rect = self.image.get_rect()

    @classmethod
    def createstarobjects(cls):
        for i in range(100):
            x_loc = random.randint(0, screen_width - 1)
            y_loc = random.randint(0, screen_height - 1)
            star = Star()
            star.rect.x = x_loc
            star.rect.y = y_loc

            cls.all_stars.add(star)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, posx=0, posy=0):
        super(Projectile, self).__init__()

        self.original_image = pygame.image.load('Proj_1.png')
        self.rotated_image = pygame.transform.rotate(self.original_image, 90)
        self.image = pygame.transform.smoothscale(self.rotated_image, [8, 15])
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.rect.centerx = self.rect.x + self.rect.center[0]
        self.rect.centery = self.rect.y + self.rect.center[1]

    def update(self, dir_and_speed):
        self.rect.y += dir_and_speed

        if self.rect.y < 0 - self.rect.height:
            self.kill()
