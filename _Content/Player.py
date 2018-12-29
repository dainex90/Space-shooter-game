
from _Content.Main import *
from _Content.fx import Projectile


class SpaceShip(pygame.sprite.Sprite):

    def __init__(self, width=30, height=30, color=white):
        super(SpaceShip, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect.centerx = self.rect.x + self.rect.center[0]
        self.rect.centery = self.rect.y + self.rect.center[1]
        self.UI_image = pygame.transform.smoothscale(self.image, (30, 30))
        self.muzzle_flash = pygame.image.load('Ship_muzzle_flash.png').convert()
        self.muzzle_flash.set_colorkey(black)
        self.engine_fire = SCALED_ENGINE_FIRE[0]
        self.maxhealth = 3
        self.health = self.maxhealth
        self.accelerationFire = False
        self.frame = 0
        self.score = 0
        self.highscore = 0
        self.pause = False
        self.isshooting = False
        self.idling_engine_soundfx = pygame.mixer.Sound(file='33503__cosmicd__engine-hum-new.wav')
        self.shoot_soundfx = pygame.mixer.Sound(file='368736__fins__shoot-5.wav')

        " MOVEMENT ------------> "

        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

        self.cur_velocity_x = 0
        self.cur_velocity_y = 0
        self.acceleration = 0.3
        self.deceleration = 0.3
        self.turn_acceleration = 0.7
        self.max_velocity_x = 12
        self.max_velocity_y = 6

    def transform_image(self):
        self.image = pygame.transform.smoothscale(self.image, (65, 65))
        self.rect = self.image.get_rect()

    def set_image(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.UI_image = pygame.transform.smoothscale(self.image, (30, 30))
        self.transform_image()

    def center_set_position(self, x, y):
        self.rect.x = x - self.rect.center[0]
        self.rect.y = y - self.rect.width

    def draw_UI(self):

        if self.health == self.maxhealth:
            screen.blit(self.UI_image, (half_width/10, 650))
            screen.blit(self.UI_image, (half_width/7, 650))
            screen.blit(self.UI_image, (half_width/5.5, 650))
        elif self.health == 2:
            screen.blit(self.UI_image, (half_width / 10, 650))
            screen.blit(self.UI_image, (half_width / 7, 650))
        elif self.health == 1:
            screen.blit(self.UI_image, (half_width / 10, 650))

    def outside_border_pos(self):
        if self.rect.x > screen_width:
            self.rect.x = (0 - self.rect.width)
        if self.rect.x < (0 - self.rect.width):
            self.rect.x = screen_width
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        if self.rect.top < 0:
            self.rect.top = 0

    def setMax_Velocity_y(self, dir):
        if abs(self.cur_velocity_y) > self.max_velocity_y:
            self.cur_velocity_y = (self.max_velocity_y * dir)

    def setMax_Velocity_x(self, dir):
        if abs(self.cur_velocity_x) > self.max_velocity_x:
            self.cur_velocity_x = (self.max_velocity_x * dir)

    def accelerate_ship(self,):

        if self.forward:
            self.cur_velocity_y -= self.acceleration
            self.rect.y += self.cur_velocity_y
            self.setMax_Velocity_y(dir=-1)

        if self.backward:
            self.cur_velocity_y += self.deceleration
            self.rect.y += self.cur_velocity_y
            self.setMax_Velocity_y(dir=1)

        if self.left:
            self.cur_velocity_x -= self.turn_acceleration
            self.rect.x += self.cur_velocity_x
            self.setMax_Velocity_x(dir=-1)

        if self.right:
            self.cur_velocity_x += self.turn_acceleration
            self.rect.x += self.cur_velocity_x
            self.setMax_Velocity_x(dir=1)

    def draw_ship(self):
        self.accelerate_ship()
        self.outside_border_pos()
        screen.blit(self.image, [self.rect.x, self.rect.y])
        if self.accelerationFire:
            self.frame += 1
            self.frame %= len(SCALED_ENGINE_FIRE)
            self.engine_fire = SCALED_ENGINE_FIRE[self.frame]
            screen.blit(self.engine_fire, (self.rect.centerx - 34, self.rect.bottom))

    def muzzle_flash_effect(self):
        if self.isshooting:
            screen.blit(self.muzzle_flash, (self.rect.centerx - 400, self.rect.y - 325))
            self.shoot_soundfx.play(fade_ms=100)
            self.isshooting = False

    def isalive(self):
        if self.health > 0:
            return True
        else:
            return False


class PlayerProjectile(Projectile):

    all_projectiles = pygame.sprite.Group()

    def __init__(self, posx, posy):
        super().__init__(posx, posy)

    @classmethod
    def createprojectile(cls, posx, posy, howmany):
        for i in range(howmany):
            player_projectile = PlayerProjectile(posx=posx, posy=posy)
            player_projectile.rect.x = posx
            player_projectile.rect.y = posy
            cls.all_projectiles.add(player_projectile)
