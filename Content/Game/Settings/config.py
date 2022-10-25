import pygame


class Cfg(pygame.sprite.Sprite):

    pygame.mixer.pre_init(44100, 16, 2, 4096)

    pygame.init()

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (200, 40, 60)
    green = (50, 180, 50)
    blue = (50, 30, 200)
    skyblue = (135, 206, 250)
    silver = (192, 192, 192)
    darkgray = (47, 79, 79)
    vegasgold = (197, 179, 88)
    nightblue = (25, 25, 112)
    steelblue = (70, 130, 180)
    deepblue = (0, 26, 51)
    orange = (255, 69, 0)

    screen_width: int = 1280
    screen_height: int = 720
    half_width: float = screen_width / 2
    half_height: float = screen_height / 2

    screen = pygame.display.set_mode([screen_width, screen_height])
    Title = pygame.display.set_caption('Imago Hunters')
    clock = pygame.time.Clock()
    fps = 30

    @classmethod
    def refresh(cls, fps: int = 30) -> None:
        pygame.display.update()
        cls.clock.tick(fps)

    @classmethod
    def fill(cls, color: tuple = black):
        cls.screen.fill(color)
