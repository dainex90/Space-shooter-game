import pygame
import sys
import os
import random
import time
import math

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

screen_width = 1280
screen_height = 720
half_width = screen_width/2
half_height = screen_height/2

screen = pygame.display.set_mode([screen_width, screen_height])
Title = pygame.display.set_caption('Space Mash')
clock = pygame.time.Clock()
fps = 30

all_sprites_list = pygame.sprite.Group()

# List comprehension

ENGINE_FIRE = list([pygame.image.load('jet_fire_{0}.png'.format(i)) for i in range(1, 9)])
SCALED_ENGINE_FIRE = list([])

for frame in ENGINE_FIRE:
    SCALED_ENGINE_FIRE.append(pygame.transform.smoothscale(frame, (70, 60)))


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, width=30, height=30, color=white):
        super(Spaceship, self).__init__()

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
        self.accelFire = False
        self.frame = 0
        self.score = 0
        self.highscore = 0
        self.pause = False

               #Movement--------------------

        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

        self.top_speed = 7
        self.current_speed = 0
        self.acceleration = 0.2
        self.deceleration = 0.3
        self.turn_acceleration = 0.5
        self.max_velX = 16
        self.velX = 0

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
        if abs(self.current_speed) > self.top_speed:
            self.current_speed = (self.top_speed * dir)

    def setMax_Velocity_x(self, dir):
        if abs(self.velX) > self.max_velX:
            self.velX = (self.max_velX * dir)

    def accelerate_ship(self,):

        if self.forward:
            self.current_speed -= self.acceleration
            self.rect.y += self.current_speed
            self.setMax_Velocity_y(dir=-1)

        if self.backward:
            self.current_speed += self.deceleration
            self.rect.y += self.current_speed
            self.setMax_Velocity_y(dir=1)

        if self.left:
            self.velX -= self.turn_acceleration
            self.rect.x += self.velX
            self.setMax_Velocity_x(dir=-1)

        if self.right:
            self.velX += self.turn_acceleration
            self.rect.x += self.velX
            self.setMax_Velocity_x(dir=1)

    def draw_ship(self):
        self.accelerate_ship()
        self.outside_border_pos()
        screen.blit(self.image, [self.rect.x, self.rect.y])
        if self.accelFire:
            self.frame += 1
            self.frame %= len(SCALED_ENGINE_FIRE)
            self.engine_fire = SCALED_ENGINE_FIRE[self.frame]
            screen.blit(self.engine_fire, (self.rect.centerx - 34, self.rect.bottom))

    def muzzle_flash_effect(self):
        screen.blit(self.muzzle_flash, (self.rect.centerx - 400, self.rect.y - 325))

player_spaceship = Spaceship()
player_spaceship.set_image("F5S4.png")
player_spaceship.center_set_position(half_width, screen_height)


all_sprites_list.add(player_spaceship)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.orig_image = pygame.image.load('Sp_station.png')
        self.image = pygame.transform.smoothscale(self.orig_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = 0 - self.rect.height
        self.speed = 1

    def draw(self):
        if bgnd.PosY >= 300:
            #self.rotation()
            self.rect.y += self.speed
            screen.blit(self.image, (self.rect.x, self.rect.y))

    #def rotation(self):
        #self.image = pygame.transform.rotate(self.rect.center, 5)

enemyShip = Enemy()


class TileSet(pygame.sprite.Sprite):
    def __init__(self):
        super(TileSet, self).__init__()
        self.image = pygame.image.load('background_scifigame.png').convert()
        self.rect = self.image.get_rect()
        self.PosY = 0
        self.rel_y = self.PosY % self.rect.height

    def setBgnd(self):
        self.rel_y = self.PosY % self.rect.height
        screen.blit(self.image, (0, self.rel_y - self.rect.height))
        if self.rel_y < screen_height:
            screen.blit(self.image, (0, self.rel_y))
        self.PosY += 0.4

bgnd = TileSet()


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
                text_ToScreen('Overload!', color=red)
                self.cooldown -= 25
            else:
                self.cooldown = 1000
                self.overload = False
                self.energyRecharge = 1
                self.update_bar()

ammo = EnergyBar()


class Projectiles(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectiles, self).__init__()

        self.original_image = pygame.image.load('Proj_1.png')
        self.rotated_image = pygame.transform.rotate(self.original_image, 90)
        self.image = pygame.transform.smoothscale(self.rotated_image, [8, 15])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect.centerx = self.rect.x + self.rect.center[0]
        self.rect.centery = self.rect.y + self.rect.center[1]

    def update(self):
        self.rect.y += -50
        if self.rect.y < (0 - self.rect.height):
            self.kill()


projectile_list = pygame.sprite.Group()

# List comprehension!

AST_EXP_SHEETS = list([pygame.image.load('Asteroid_explosions_{0}.png'.format(i)) for i in range(1, 4)])
ASTEROID_FRAMES = list([pygame.image.load('Asteroid_{0}.png'.format(i)) for i in range(1, 61)])
EXPLOSION_FRAMES = list([pygame.image.load('Explosion_animation{0}.png'.format(i)) for i in range(1, 34)])
SCALED_EXPLOSION_FRAMES = []

for frames in EXPLOSION_FRAMES:
    SCALED_EXPLOSION_FRAMES.append(pygame.transform.smoothscale(frames, (60, 60)))


class Effects(pygame.sprite.Sprite):
    def __init__(self, frame=0):
        super(Effects, self).__init__()

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
        self.astPosX = 0
        self.astPosY = 0
        self.sheetType = 0

    def ast_exp(self, posX, posY):
        if self.astexp == True or self.playerexp == True:

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
                    if player_spaceship.health <= 0:
                        game_over()

explosion = Effects()
# Datastructure

effects_list = pygame.sprite.Group()
effects_list.add(explosion)


class Asteroids(pygame.sprite.Sprite):

    next_level_count = 0

    def __init__(self, xpos=0, ypos=0, start_frame=0):
        super(Asteroids, self).__init__()

        self.image = ASTEROID_FRAMES[start_frame]
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.frame = start_frame
        self.speed = 4

    def set_random_attr(self):
        self.reset_position()
        self.frame = random.randint(0, 59)
        self.image = ASTEROID_FRAMES[self.frame]

    def reset_position(self):
        self.rect.y = random.randrange(-900, -400)
        self.rect.x = random.randrange(0, (screen_width - self.rect.width))

    def update(self, speed):
        self.rect.y += speed

        if self.rect.y > screen_height + 150:
            self.reset_position()
            #Asteroids.next_level_count += 1
            asteroid = Asteroids()
            asteroid.set_random_attr()
            asteroids_list.add(asteroid)

        self.frame += 1

        # Remainder-Division.
        self.frame %= len(ASTEROID_FRAMES)
        self.image = ASTEROID_FRAMES[self.frame]


asteroids_list = pygame.sprite.Group()


class Stars(pygame.sprite.Sprite):
    def __init__(self):
        super(Stars, self).__init__()

        self.image = pygame.Surface([1, 1])
        self.image.fill(white)
        self.rect = self.image.get_rect()

    @staticmethod
    def making_star_objects():
        for i in range(100):
            x_loc = random.randint(0, screen_width - 1)
            y_loc = random.randint(0, screen_height - 1)
            star = Stars()
            star.rect.x = x_loc
            star.rect.y = y_loc

            stars_list.add(star)

stars_list = pygame.sprite.Group()


def game_over():

    text_ToScreen(text='Game Over!')
    pygame.display.update()
    time.sleep(5)
    player_spaceship.score = 0
    player_spaceship.health = player_spaceship.maxhealth
    bgnd.PosY = 0
    for asteroid in asteroids_list:
        #Remove all sprites in data-structure.
        asteroid.kill()

    gameloop()

#def randgen(set_max, objdimension):

    #return random.randrange(0, set_max - objdimension)


def text_ToScreen(text, font='spaceport1i.ttf', size=50, color=silver, pos_X=half_width, pos_Y=half_height):

    font = pygame.font.Font(font, size, bold=True)
    textsurf = font.render(text, True, color)
    text_rect = textsurf.get_rect()
    text_rect.center = (pos_X, pos_Y)
    screen.blit(textsurf, text_rect)


def gameloop():
    ending = False
    Stars.making_star_objects()
    asteroid = Asteroids(xpos=750, ypos=-500, start_frame=0)
    asteroids_list.add(asteroid)
    all_sprites_list.add(asteroid)
    while not ending:

        if player_spaceship.velX == 0:
            player_spaceship.left = False
            player_spaceship.right = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_d:
                    if explosion.playerexp:
                        player_spaceship.right = False
                    else:
                        player_spaceship.right = True
                        player_spaceship.left = False

                if event.key == pygame.K_a:
                    if explosion.playerexp:
                        player_spaceship.left = False
                    else:
                        player_spaceship.left = True
                        player_spaceship.right = False

                if event.key == pygame.K_w:
                    if explosion.playerexp:
                        player_spaceship.forward = False
                    else:
                        player_spaceship.accelFire = True
                        player_spaceship.forward = True
                        player_spaceship.backward = False

                if event.key == pygame.K_s:
                    if explosion.playerexp:
                        player_spaceship.backward = False
                    else:
                        player_spaceship.accelFire = False
                        player_spaceship.backward = True
                        player_spaceship.forward = False

                if event.key == pygame.K_SPACE:
                    if not ammo.overload:
                        player_spaceship.muzzle_flash_effect()
                        pygame.display.update()
                        projectile = Projectiles()
                        projectile.rect.centerx = player_spaceship.rect.centerx
                        projectile.rect.bottom = player_spaceship.rect.y - (projectile.rect.height * 2)
                        projectile_list.add(projectile)
                        ammo.energyCur -= ammo.energyDrain
                if event.key == pygame.K_p:
                    player_spaceship.pause = True

        asteroids_list.update(asteroid.speed)
        projectile_list.update()

        # Collition Detection!
        player_hit_asteroids = pygame.sprite.spritecollide(player_spaceship, asteroids_list, True)
        proj_hit_asteroids = pygame.sprite.groupcollide(asteroids_list, projectile_list, True, True)

        for asteroid in proj_hit_asteroids:
            player_spaceship.score += 1
            explosion.sheetType = random.randint(0, 2)
            explosion.asteroidExpframes = AST_EXP_SHEETS[explosion.sheetType]
            explosion.astPosX = asteroid.rect.x
            explosion.astPosY = asteroid.rect.y
            explosion.astexp = True

        for asteroid in player_hit_asteroids:
            explosion.asteroidExpframes = AST_EXP_SHEETS[1]
            explosion.astPosX = player_spaceship.rect.x
            explosion.astPosY = player_spaceship.rect.y
            explosion.playerexp = True
            player_spaceship.accelFire = False
            player_spaceship.health -= 1
            for i in range(3):
                asteroid = Asteroids()
                asteroid.set_random_attr()
                asteroids_list.add(asteroid)

        if len(asteroids_list) < 3:
            for i in range(3):
                asteroid = Asteroids()
                asteroid.set_random_attr()
                asteroids_list.add(asteroid)


        # Blitting all Sprites.

        screen.fill(deepblue)
        bgnd.setBgnd()
        stars_list.draw(screen)
        asteroids_list.draw(screen)
        projectile_list.draw(screen)
        player_spaceship.draw_ship()
        player_spaceship.draw_UI()
        enemyShip.draw()
        explosion.ast_exp(explosion.astPosX, explosion.astPosY)
        text_ToScreen(text='Score: {0}'.format(player_spaceship.score), size=12, pos_X=400, pos_Y=15)
        text_ToScreen(text='Highscore: {0}'.format(player_spaceship.highscore), size=15, color=vegasgold, pos_Y=15)
        ammo.draw_bar()
        pygame.display.update()
        clock.tick(30)

        if player_spaceship.pause:
            pause = True
            while pause:
                text_ToScreen("PAUSE", color=steelblue)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            player_spaceship.pause = False
                            pause = False

    pygame.quit()
    quit()

gameloop()