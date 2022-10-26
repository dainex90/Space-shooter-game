
import pygame


# LOCAL IMPORTS
from Content.Game.Settings.config import Cfg


class SpaceShip(pygame.sprite.Sprite):

    def __init__(self, width: int = 30, height: int = 30, color=Cfg.white):
        super().__init__()

        self.ENGINE_FIRE = []
        self.SCALED_ENGINE_FIRE = []
        self.load_engine_effects()
        self.transform_engine_effects()
        self.engine_fire = self.SCALED_ENGINE_FIRE[0]

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect.centerx = self.rect.x + self.rect.center[0]
        self.rect.centery = self.rect.y + self.rect.center[1]
        self.UI_image = pygame.transform.smoothscale(self.image, (30, 30))
        self.muzzle_flash = pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites'
                                              R'\Ship_muzzle_flash.png').convert()
        self.muzzle_flash.set_colorkey(Cfg.black)
        self.maxhealth: int = 3
        self.health = self.maxhealth
        self.acceleration_fire: bool = False
        self.frame: int = 0
        self.score: int = 0
        self.highscore: int = 0
        self.pause: bool = False
        self.isshooting: bool = False
        self.idling_engine_soundfx = pygame.mixer.Sound(file=R'C:\Users\danie\PycharmProjects\Space-shooter-game\sound_fx\33503__cosmicd__engine-hum-new.wav')
        self.shoot_soundfx = pygame.mixer.Sound(file=R'C:\Users\danie\PycharmProjects\Space-shooter-game\sound_fx\368736__fins__shoot-5.wav')

        " MOVEMENT ------------> "

        self.forward: bool = False
        self.backward: bool = False
        self.left: bool = False
        self.right: bool = False

        self.cur_velocity_x = 0
        self.cur_velocity_y = 0

        "physics"
        self.acceleration: float = 0.4
        self.deceleration: float = 1.4
        self.turn_acceleration: float = 2.2
        self.max_velocity_x: int = 16
        self.max_velocity_y: int = 5


    def load_engine_effects(self) -> None:
        " list comprehension, loading the ship fire effect "
        self.ENGINE_FIRE = list(
            [pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites\jet_fire_{0}.png'
                               .format(i)) for i in range(1, 9)])

    def transform_engine_effects(self) -> None:
        "and scales the effect"
        for frame in self.ENGINE_FIRE:
            self.SCALED_ENGINE_FIRE.append(pygame.transform.smoothscale(frame, (70, 60)))

    def transform_image(self) -> None:
        self.image = pygame.transform.smoothscale(self.image, (65, 65))
        self.rect = self.image.get_rect()

    def set_image(self, filename: str) -> None:
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.UI_image = pygame.transform.smoothscale(self.image, (30, 30))
        self.transform_image()

    def center_set_position(self, x: float, y: float) -> None:
        self.rect.x = x - self.rect.center[0]
        self.rect.y = y - self.rect.width

    def draw_ui(self):

        if self.health == self.maxhealth:
            Cfg.screen.blit(self.UI_image, (Cfg.half_width/10, 650))
            Cfg.screen.blit(self.UI_image, (Cfg.half_width/7, 650))
            Cfg.screen.blit(self.UI_image, (Cfg.half_width/5.5, 650))
        elif self.health == 2:
            Cfg.screen.blit(self.UI_image, (Cfg.half_width / 10, 650))
            Cfg.screen.blit(self.UI_image, (Cfg.half_width / 7, 650))
        elif self.health == 1:
            Cfg.screen.blit(self.UI_image, (Cfg.half_width / 10, 650))

    def outside_border_pos(self):
        if self.rect.x > Cfg.screen_width:
            self.rect.x = (0 - self.rect.width)
        if self.rect.x < (0 - self.rect.width):
            self.rect.x = Cfg.screen_width

            # todo - Fix magic numbers!
        if self.rect.bottom > Cfg.screen_height - 70:
            self.rect.bottom = Cfg.screen_height - 70
        if self.rect.top < 0:
            self.rect.top = 0

    def setMax_Velocity_y(self, direction):
        if abs(self.cur_velocity_y) > self.max_velocity_y:
            self.cur_velocity_y = (self.max_velocity_y * direction)

    def setMax_Velocity_x(self, direction):
        if abs(self.cur_velocity_x) > self.max_velocity_x:
            self.cur_velocity_x = (self.max_velocity_x * direction)

    def accelerate_ship(self,):

        if self.forward:
            self.cur_velocity_y -= self.acceleration
            self.rect.y += self.cur_velocity_y
            self.setMax_Velocity_y(direction=-1)

        if self.backward:
            self.cur_velocity_y += self.deceleration
            self.rect.y += self.cur_velocity_y
            self.setMax_Velocity_y(direction=1)

        if self.left:
            self.cur_velocity_x -= self.turn_acceleration
            self.rect.x += self.cur_velocity_x
            self.setMax_Velocity_x(direction=-1)

        if self.right:
            self.cur_velocity_x += self.turn_acceleration
            self.rect.x += self.cur_velocity_x
            self.setMax_Velocity_x(direction=1)

    def draw_ship(self):
        self.accelerate_ship()
        self.outside_border_pos()
        Cfg.screen.blit(self.image, [self.rect.x, self.rect.y])
        if self.acceleration_fire:
            self.frame += 1
            self.frame %= len(self.SCALED_ENGINE_FIRE)
            self.engine_fire = self.SCALED_ENGINE_FIRE[self.frame]
            Cfg.screen.blit(self.engine_fire, (self.rect.centerx - 34, self.rect.bottom))

    def muzzle_flash_effect(self):
        if self.isshooting:
            Cfg.screen.blit(self.muzzle_flash, (self.rect.centerx - 400, self.rect.y - 325))
            self.shoot_soundfx.play(fade_ms=100)
            self.isshooting = False

    def isalive(self) -> bool:
        if self.health > 0:
            return True
        else:
            return False

