import random

import pygame

from Content.Game.Effects.game_effects import EnemyProjectile

# LOCAL IMPORTS
from Content.Game.Main import main
from Content.Game.Settings.config import Cfg


class Enemy(pygame.sprite.Sprite):
    all_enemies = pygame.sprite.Group()

    def __init__(self, speed: int, maxhealth: int, timebetweenshooting: int):
        super(Enemy, self).__init__()
        self.orig_image = pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites\Sp_station.png')
        self.image = pygame.transform.smoothscale(self.orig_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, Cfg.screen_width - self.rect.width)
        self.rect.y = 0 - self.rect.height
        self.speed = speed
        self.maxhealth = maxhealth
        self.health = self.maxhealth
        self.timebetweenshooting = timebetweenshooting
        self.shoot_soundfx = pygame.mixer.Sound(file=R'C:\Users\danie\PycharmProjects\Space-shooter-game\sound_fx'
                                                     R'\391635__edo333__sci-fi-laser-gun.wav')

        # Physics ->

        self.cur_velocity_x: int = 0
        self.cur_velocity_y: int = 0

        self.acceleration: float = 0.8
        self.deceleration: float = 0.8
        self.turn_acceleration: float = 1.2
        self.max_velocity_x: int = 18
        self.max_velocity_y: int = 10

        self.moveleft: bool = True
        self.moveright: bool = False

    def update(self, *args, **kwargs) -> None:
        if main.background.PosY >= 250:
            self.move()
            self.timebetweenshooting -= 1
            if self.isshooting():
                self.shoot_soundfx.play(fade_ms=300)
                EnemyProjectile.createprojectile(self.rect.x, self.rect.y, howmany=1)
                EnemyProjectile.createprojectile(self.rect.x + self.rect.width, self.rect.y, howmany=1)

            if self.rect.y > Cfg.screen_height + self.rect.height:
                self.kill()
                newspeed = random.randint(4, 8)
                Enemy.create_enemy(speed=newspeed, maxhealth=100, timebetweenshooting=30, count=1)

    def setposition(self) -> None:
        self.rect.x = random.randrange(0 + self.max_velocity_x, (Cfg.screen_width - (self.rect.width +
                                                                                     self.max_velocity_x)))
        self.rect.y = random.randrange(-1200, -600)

    def rotation(self) -> None:
        self.image = pygame.transform.rotate(self.image, 5)

    def isshooting(self) -> bool:
        if self.timebetweenshooting <= 0 and self.rect.bottom > self.rect.height:
            self.timebetweenshooting = 30
            return True
        else:
            return False

    def isalive(self) -> bool:
        if self.health > 0:
            return True
        else:
            return False

    @classmethod
    def create_enemy(cls, speed, maxhealth, timebetweenshooting, count=1) -> None:
        for _ in range(count):
            enemy = Enemy(speed, maxhealth, timebetweenshooting)
            enemy.setposition()
            cls.all_enemies.add(enemy)

    @classmethod
    def killallenemies(cls) -> None:
        for enemy in cls.all_enemies:
            enemy.kill()

    def move(self) -> None:

        """Move the enemy down at a constant speed"""

        self.rect.y += self.speed

        "turn the enemy left and right with acceleration physics"

        if self.moveleft:
            self.cur_velocity_x -= self.turn_acceleration
            self.rect.x += self.cur_velocity_x

        if self.moveright:
            self.cur_velocity_x += self.turn_acceleration
            self.rect.x += self.cur_velocity_x

        self.setMovementDirection()

    def setMovementDirection(self) -> None:
        if abs(self.cur_velocity_x) > self.max_velocity_x:
            if self.cur_velocity_x < 0:
                self.moveright = True
                self.moveleft = False
            else:
                self.moveleft = True
                self.moveright = False
