

from Content import Main
from Content import Config
from.Config import Cfg
from .fx import Projectile
import pygame
import random


class Enemy(pygame.sprite.Sprite):

    all_enemies = pygame.sprite.Group()

    def __init__(self, speed, maxhealth, timebetweenshooting):
        super(Enemy, self).__init__()
        self.orig_image = pygame.image.load(R'C:\Users\danba\PycharmProjects\Space-shooter-game\Sprites\Sp_station.png')
        self.image = pygame.transform.smoothscale(self.orig_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, Config.Cfg.screen_width - self.rect.width)
        self.rect.y = 0 - self.rect.height
        self.speed = speed
        self.maxhealth = maxhealth
        self.health = self.maxhealth
        self.timebetweenshooting = timebetweenshooting
        self.shoot_soundfx = pygame.mixer.Sound(file=R'C:\Users\danba\PycharmProjects\Space-shooter-game\sound_fx'
                                                     R'\391635__edo333__sci-fi-laser-gun.wav')

        # Physics ->
        self.cur_velocity_x = 0
        # self.cur_velocity_y = 0

        self.acceleration = 0.8
        self.deceleration = 0.8
        self.turn_acceleration = 1.2
        self.max_velocity_x = 18
        # self.max_velocity_y = 10

        self.moveleft = True
        self.moveright = False

    def update(self, *args, **kwargs):
        if Main.bgnd.PosY >= 250:
            self.move()
            self.timebetweenshooting -= 1
            if self.isshooting():
                self.shoot_soundfx.play(fade_ms=300)
                EnemyProjectile.createprojectile(self.rect.x, self.rect.y, howmany=1)
                EnemyProjectile.createprojectile(self.rect.x + self.rect.width, self.rect.y, howmany=1)

            if self.rect.y > Cfg.screen_height + self.rect.height:
                self.kill()
                newspeed = random.randint(4, 8)
                Enemy.createenemy(speed=newspeed, maxhealth=100, timebetweenshooting=30, count=1)

    def setposition(self):
        self.rect.x = random.randrange(0 + self.max_velocity_x, (Config.Cfg.screen_width - (self.rect.width +
                                                                                            self.max_velocity_x)))
        self.rect.y = random.randrange(-1200, -600)

    def rotation(self):
        self.image = pygame.transform.rotate(self.image, 5)

    def isshooting(self):
        if self.timebetweenshooting <= 0 and self.rect.bottom > self.rect.height:
            self.timebetweenshooting = 30
            return True
        else:
            return False

    def isalive(self):
        if self.health > 0:
            return True
        else:
            return False

    @classmethod
    def createenemy(cls, speed, maxhealth, timebetweenshooting, count=1):
        for i in range(count):
            enemy = Enemy(speed, maxhealth, timebetweenshooting)
            enemy.setposition()
            cls.all_enemies.add(enemy)

    @classmethod
    def killallenemies(cls):
        for enemy in cls.all_enemies:
            enemy.kill()

    def move(self):
        "Move the enemy down at a constant speed"
        self.rect.y += self.speed

        "turn the enemy left and right with acceleration physics"
        if self.moveleft:
            self.cur_velocity_x -= self.turn_acceleration
            self.rect.x += self.cur_velocity_x

        if self.moveright:
            self.cur_velocity_x += self.turn_acceleration
            self.rect.x += self.cur_velocity_x

        self.setMovementDirection()

    def setMovementDirection(self):
        if abs(self.cur_velocity_x) > self.max_velocity_x:
            if self.cur_velocity_x < 0:
                self.moveright = True
                self.moveleft = False
            else:
                self.moveleft = True
                self.moveright = False


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


class Asteroid(pygame.sprite.Sprite):

    next_level_count = 0
    all_asteroids = pygame.sprite.Group()

    def __init__(self, xpos=0, ypos=0, start_frame=0):
        super(Asteroid, self).__init__()

        self.image = Main.ASTEROID_FRAMES[start_frame]
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.frame = start_frame
        self.speed = Main.random.randint(5, 8)
        self.sound_effect = pygame.mixer.Sound(file=R'C:\Users\danba\PycharmProjects\Space-shooter-game\sound_fx'
                                                    R'\244345__willlewis__musket-explosion.wav')

    def set_random_attr(self):
        self.reset_position()
        self.frame = random.randint(0, 59)
        self.image = Main.ASTEROID_FRAMES[self.frame]

    def reset_position(self):
        self.rect.y = random.randrange(-900, -400)
        self.rect.x = random.randrange(0, (Config.Cfg.screen_width - self.rect.width))

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > Config.Cfg.screen_height + 150:
            self.kill()
            Asteroid.createasteroid(count=2)

        self.frame += 1
        " Remainder-Division."
        self.frame %= len(Main.ASTEROID_FRAMES)
        self.image = Main.ASTEROID_FRAMES[self.frame]

    @classmethod
    def createasteroid(cls, count=1):
        for i in range(count):

            asteroid = Asteroid()
            asteroid.set_random_attr()
            cls.all_asteroids.add(asteroid)

    @classmethod
    def killallasteroids(cls):
        for asteroid in cls.all_asteroids:
            asteroid.kill()


