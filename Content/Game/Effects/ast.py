from Content.Game.Settings.config import Cfg
import pygame
import random


class Asteroid(pygame.sprite.Sprite):

    next_level_count: int = 0
    all_asteroids = pygame.sprite.Group()
    ASTEROID_FRAMES = []

    def __init__(self, xpos: int = 0, ypos: int = 0, start_frame: int = 0, ):
        super(Asteroid, self).__init__()

        self.load_asteroid_frames()
        self.image = self.ASTEROID_FRAMES[start_frame]
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.frame = start_frame
        self.speed = random.randint(5, 8)
        self.sound_effect = pygame.mixer.Sound(file=R'C:\Users\danie\PycharmProjects\Space-shooter-game\sound_fx'
                                                    R'\244345__willlewis__musket-explosion.wav')

    @classmethod
    def load_asteroid_frames(cls) -> None:
        # loading all the asteroid sprites to a list
        cls.ASTEROID_FRAMES = list([pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites'
                                                  R'\Asteroid sprites\Asteroid_{0}.png'.format(i)) for i in
                                range(1, 61)])

    def set_random_attr(self):
        self.reset_position()
        self.frame = random.randint(0, 59)
        self.image = self.ASTEROID_FRAMES[self.frame]

    def reset_position(self):
        self.rect.y = random.randrange(-900, -400)
        self.rect.x = random.randrange(0, (Cfg.screen_width - self.rect.width))

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > Cfg.screen_height + 150:
            self.kill()
            Asteroid.create_asteroid(count=2)

        self.frame += 1
        " Remainder-Division."
        self.frame %= len(self.ASTEROID_FRAMES)
        self.image = self.ASTEROID_FRAMES[self.frame]

    @classmethod
    def create_asteroid(cls, count:int = 1) -> None:
        for _ in range(count):
            asteroid = Asteroid()
            asteroid.set_random_attr()
            cls.all_asteroids.add(asteroid)

    @classmethod
    def kill_all_asteroids(cls):
        for asteroid in cls.all_asteroids:
            asteroid.kill()


