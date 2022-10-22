import pygame
import random

# LOCAL IMPORTS
from Content.Game.Settings.config import *


class PlayerProjectile(pygame.sprite.Sprite):

    all_projectiles = pygame.sprite.Group()

    def __init__(self, posx, posy):
        super(PlayerProjectile, self).__init__(posx, posy)

    @classmethod
    def createprojectile(cls, posx, posy, howmany):
        for i in range(howmany):
            player_projectile = PlayerProjectile(posx=posx, posy=posy)
            player_projectile.rect.x = posx
            player_projectile.rect.y = posy
            cls.all_projectiles.add(player_projectile)


class Effect(pygame.sprite.Sprite):

    """" Datastructure """
    all_effects = pygame.sprite.Group()

    def __init__(self, ast_exp_sheets):
        super(Effect, self).__init__()
        self.asteroidExpframes = ast_exp_sheets[0]
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

        # todo what is this?
        """
        self.image = SCALED_EXPLOSION_FRAMES[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect.centerx = self.rect.x + self.rect.center[0]
        self.rect.centery = self.rect.y + self.rect.center[1]
        self.frame = -1 
        """

    def ast_exp(self, posx, posy):
        if self.astexp or self.playerexp or self.enemyexp:

            Cfg.screen.blit(self.asteroidExpframes, (posx, posy),
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
                    if Main.player.health <= 0:
                        Main.game_over()


class Explosion(Effect):
    def __init__(self):
        super().__init__()


class Star(pygame.sprite.Sprite):
    all_stars = pygame.sprite.Group()

    def __init__(self):
        super(Star, self).__init__()

        self.image = pygame.Surface([1, 1])
        self.image.fill(Cfg.white)
        self.rect = self.image.get_rect()

    @classmethod
    def createstarobjects(cls):

        for i in range(100):

            x_loc = random.randint(0, Cfg.screen_width - 1)
            y_loc = random.randint(0, Cfg.screen_height - 1)
            star = Star()
            star.rect.x = x_loc
            star.rect.y = y_loc

            cls.all_stars.add(star)


class Projectile(pygame.sprite.Sprite):

    def __init__(self, posx=0, posy=0):
        super(Projectile, self).__init__()

        self.original_image = pygame.image.load(R'C:\Users\danba\PycharmProjects\Space-shooter-game\Sprites\Proj_1.png')
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


class EnemyProjectile(Projectile):

    all_projectiles = pygame.sprite.Group()

    def __init__(self, posx, posy):
        super().__init__(posx, posy)

        self.image = pygame.transform.rotate(self.image, 180)

    @classmethod
    def createprojectile(cls, posx, posy, howmany):
        for i in range(howmany):
            enemy_projectile = EnemyProjectile(posx=posx, posy=posy)
            enemy_projectile.rect.centerx = posx
            enemy_projectile.rect.y = posy + (enemy_projectile.rect.height * 2)
            cls.all_projectiles.add(enemy_projectile)

    def update(self, dir_and_speed):
        self.rect.y += dir_and_speed

        if self.rect.y > Cfg.screen_height:
            self.kill()
