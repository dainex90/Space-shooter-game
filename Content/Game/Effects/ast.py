import pygame

from Content.Game.Main.main import *


class Asteroid(pygame.sprite.Sprite):

    next_level_count: int = 0
    all_asteroids = pygame.sprite.Group()

    def __init__(self, ASTEROID_FRAMES, xpos: int = 0, ypos: int = 0, start_frame: int = 0, ):
        super(Asteroid, self).__init__()

        self.image = ASTEROID_FRAMES[start_frame]
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.frame = start_frame
        self.speed = random.randint(5, 8)
        self.sound_effect = pygame.mixer.Sound(file=R'C:\Users\danie\PycharmProjects\Space-shooter-game\sound_fx'
                                                    R'\244345__willlewis__musket-explosion.wav')

    def set_random_attr(self):
        self.reset_position()
        self.frame = random.randint(0, 59)
        self.image = ASTEROID_FRAMES[self.frame]

    def reset_position(self):
        self.rect.y = random.randrange(-900, -400)
        self.rect.x = random.randrange(0, (Cfg.screen_width - self.rect.width))

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > Cfg.screen_height + 150:
            self.kill()
            Asteroid.createasteroid(count=2)

        self.frame += 1
        " Remainder-Division."
        self.frame %= len(ASTEROID_FRAMES)
        self.image = ASTEROID_FRAMES[self.frame]

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


