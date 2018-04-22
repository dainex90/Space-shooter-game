import pygame
import sys
import os
import random
import time
import math
from enum import Enum


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

screen_width = 1280
screen_height = 720
half_width = screen_width/2
half_height = screen_height/2

screen = pygame.display.set_mode([screen_width, screen_height])
Title = pygame.display.set_caption('Space Mash')
clock = pygame.time.Clock()
fps = 30

all_sprites_list = pygame.sprite.Group()


" List Comprehension. "
ENGINE_FIRE = list([pygame.image.load('jet_fire_{0}.png'.format(i)) for i in range(1, 9)])
SCALED_ENGINE_FIRE = list([])

for frame in ENGINE_FIRE:
    SCALED_ENGINE_FIRE.append(pygame.transform.smoothscale(frame, (70, 60)))


class States(Enum):

    def __init__(self, *args):
        super(States, self).__init__()


class GameStates(States):

    MainMenu = "MainMenu"
    InGame = "InGame"
    Pause = "Pause"
    Exit = "Exit"

    def __init__(self, *args):
        super().__init__(*args)


class LevelStates(States):

    Level1 = "Level1"
    Level2 = "Level2"
    Level3 = "Level3"
    
    def __init__(self, *args):
        super().__init__(*args)
        

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


player = Spaceship()
player.set_image("F5S4.png")
player.center_set_position(half_width, screen_height)


all_sprites_list.add(player)


class Enemy(pygame.sprite.Sprite):

    all_enemies = pygame.sprite.Group()

    def __init__(self, speed, maxhealth, timebetweenshooting):
        super(Enemy, self).__init__()
        self.orig_image = pygame.image.load('Sp_station.png')
        self.image = pygame.transform.smoothscale(self.orig_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = 0 - self.rect.height
        self.speed = speed
        self.maxhealth = maxhealth
        self.health = self.maxhealth
        self.timebetweenshooting = timebetweenshooting
        self.shoot_soundfx = pygame.mixer.Sound(file='391635__edo333__sci-fi-laser-gun.wav')

    def update(self, *args, **kwargs):
        if bgnd.PosY >= 300:
            self.rect.y += self.speed
            self.timebetweenshooting -= 1
            if self.isshooting():
                self.shoot_soundfx.play(fade_ms=300)
                EnemyProjectile.createprojectile(self.rect.x, self.rect.y, howmany=1)
                EnemyProjectile.createprojectile(self.rect.x + self.rect.width, self.rect.y, howmany=1)

            if self.rect.y > screen_height + self.rect.height:
                self.kill()
                newspeed = random.randint(3, 6)
                Enemy.createenemy(speed=newspeed, maxhealth=100, timebetweenshooting=30, count=1)

    def setposition(self):
        self.rect.x = random.randrange(0, (screen_width - self.rect.width))
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
        print(os.getcwd())  # Log this line.
        self.overload_soundfx = pygame.mixer.Sound('354049__pauldihor__gun-fire-for-futuristic-game.wav')

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

                self.overload_soundfx.play()
                texttoscreen('Overload!', color=red)
                self.cooldown -= 25
            else:
                self.cooldown = 1000
                self.overload = False
                self.energyRecharge = 1
                self.update_bar()


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

        if self.rect.y > screen_height:
            self.kill()


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


" LIST COMPREHENSIONS! "

AST_EXP_SHEETS = list([pygame.image.load('Asteroid_explosions_{0}.png'.format(i)) for i in range(1, 4)])
ASTEROID_FRAMES = list([pygame.image.load('Asteroid_{0}.png'.format(i)) for i in range(1, 61)])
EXPLOSION_FRAMES = list([pygame.image.load('Explosion_animation{0}.png'.format(i)) for i in range(1, 34)])
SCALED_EXPLOSION_FRAMES = []

for frames in EXPLOSION_FRAMES:
    SCALED_EXPLOSION_FRAMES.append(pygame.transform.smoothscale(frames, (60, 60)))


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


explosion = Effect()
Effect.all_effects.add(explosion)


class Asteroid(pygame.sprite.Sprite):

    next_level_count = 0
    all_asteroids = pygame.sprite.Group()

    def __init__(self, xpos=0, ypos=0, start_frame=0):
        super(Asteroid, self).__init__()

        self.image = ASTEROID_FRAMES[start_frame]
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.frame = start_frame
        self.speed = random.randint(3, 6)
        self.sound_effect = pygame.mixer.Sound(file='244345__willlewis__musket-explosion.wav')

    def set_random_attr(self):
        self.reset_position()
        self.frame = random.randint(0, 59)
        self.image = ASTEROID_FRAMES[self.frame]

    def reset_position(self):
        self.rect.y = random.randrange(-900, -400)
        self.rect.x = random.randrange(0, (screen_width - self.rect.width))

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > screen_height + 150:
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


def game_over():

    player.idling_engine_soundfx.stop()
    texttoscreen(text='Game Over!')
    pygame.display.update()
    time.sleep(5)
    player.score = 0
    player.health = player.maxhealth
    bgnd.PosY = 0

    " Remove all sprites in data-structure/group."
    Asteroid.killallasteroids()
    Enemy.killallenemies()
    gameloop()


def texttoscreen(text, font='spaceport1i.ttf', size=50, color=silver, pos_X=half_width, pos_Y=half_height):

    font = pygame.font.Font(font, size, bold=True)
    textsurf = font.render(text, True, color)
    text_rect = textsurf.get_rect()
    text_rect.center = (pos_X, pos_Y)
    screen.blit(textsurf, text_rect)


def gameloop():
    player.idling_engine_soundfx.set_volume(0.1)
    player.idling_engine_soundfx.play(loops=-1)
    curgamestate = GameStates.InGame.name
    curlevelstate = LevelStates.Level1.name
    ending = False
    Star.createstarobjects()
    asteroid = Asteroid(xpos=750, ypos=-500, start_frame=0)
    Asteroid.all_asteroids.add(asteroid)
    enemy_ship = Enemy(speed=4, maxhealth=100, timebetweenshooting=30)
    Enemy.all_enemies.add(enemy_ship)
    ammo = EnergyBar()

    all_sprites_list.add([asteroid, enemy_ship])

    if curgamestate == GameStates.MainMenu.name:
        
        "You Are in Main Menu!"
        "..."

    elif curgamestate == GameStates.InGame.name:

        "You are InGame!!"
        "..." \

        "WHAT LEVEL? ->"
        if curlevelstate == LevelStates.Level1.name:

            " LEVEL 1 HERE "
            while not ending:

                if player.cur_velocity_x == 0:
                    player.left = False
                    player.right = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()

                        if event.key == pygame.K_d:
                            if explosion.playerexp:
                                player.right = False
                            else:
                                player.right = True
                                player.left = False

                        if event.key == pygame.K_a:
                            if explosion.playerexp:
                                player.left = False
                            else:
                                player.left = True
                                player.right = False

                        if event.key == pygame.K_w:
                            if explosion.playerexp:
                                player.forward = False
                            else:
                                player.accelerationFire = True
                                player.forward = True
                                player.backward = False

                        if event.key == pygame.K_s:
                            if explosion.playerexp:
                                player.backward = False
                            else:
                                player.accelerationFire = False
                                player.backward = True
                                player.forward = False

                        if event.key == pygame.K_SPACE:
                            if not ammo.overload:
                                player.isshooting = True
                                projectile = PlayerProjectile(posx=player.rect.x, posy=player.rect.y)
                                projectile.rect.centerx = player.rect.centerx
                                projectile.rect.bottom = player.rect.y - (projectile.rect.height * 2)
                                PlayerProjectile.all_projectiles.add(projectile)
                                ammo.energyCur -= ammo.energyDrain
                        if event.key == pygame.K_p:
                            player.pause = True

                    """if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            player.acceleration_sound.stop()"""
                " UPDATE ALL MOVING SPRITES!   -------------- "

                Enemy.all_enemies.update()
                Asteroid.all_asteroids.update()
                PlayerProjectile.all_projectiles.update(-50)
                EnemyProjectile.all_projectiles.update(60)

                " Collition Detection! "

                player_hit_asteroids = pygame.sprite.spritecollide(player, Asteroid.all_asteroids, True)
                proj_hit_asteroids = pygame.sprite.groupcollide(Asteroid.all_asteroids, PlayerProjectile.all_projectiles, True,
                                                                True)
                enemyproj_hit_player = pygame.sprite.spritecollide(player, EnemyProjectile.all_projectiles, False)
                playerproj_hit_enemies = pygame.sprite.groupcollide(Enemy.all_enemies, PlayerProjectile.all_projectiles, False,
                                                                    True)
                player_hit_enemies = pygame.sprite.spritecollide(player, Enemy.all_enemies, True)

                for asteroid in proj_hit_asteroids:
                    asteroid.sound_effect.set_volume(1.0)
                    asteroid.sound_effect.play()
                    player.score += 1
                    explosion.sheetType = random.randint(0, 2)
                    explosion.asteroidExpframes = AST_EXP_SHEETS[explosion.sheetType]
                    explosion.astPosX = asteroid.rect.x
                    explosion.astPosY = asteroid.rect.y
                    explosion.astexp = True

                for enemy in playerproj_hit_enemies:
                    enemy.health -= 20
                    if not enemy.isalive():
                        player.score += 5
                        explosion.sheetType = random.randint(0, 2)
                        explosion.asteroidExpframes = AST_EXP_SHEETS[explosion.sheetType]
                        explosion.astPosX = asteroid.rect.x
                        explosion.astPosY = asteroid.rect.y
                        explosion.enemyexp = True
                        enemy.kill()

                for proj in enemyproj_hit_player:
                    explosion.asteroidExpframes = AST_EXP_SHEETS[1]
                    explosion.astPosX = proj.rect.x
                    explosion.astPosY = proj.rect.y
                    explosion.playerexp = True
                    player.accelerationFire = False
                    player.health -= 1
                    proj.kill()
                    if not player.isalive():
                        game_over()

                for asteroid in player_hit_asteroids:
                    explosion.asteroidExpframes = AST_EXP_SHEETS[1]
                    explosion.astPosX = player.rect.x
                    explosion.astPosY = player.rect.y
                    explosion.playerexp = True
                    player.accelerationFire = False
                    player.health -= 1
                    Asteroid.createasteroid(count=3)

                for enemy in player_hit_enemies:
                    explosion.asteroidExpframes = AST_EXP_SHEETS[0]
                    explosion.astPosX = player.rect.x
                    explosion.astPosY = player.rect.y
                    explosion.playerexp = True
                    player.accelerationFire = False
                    player.health -= 2
                    Asteroid.createasteroid(count=3)

                if (Asteroid.all_asteroids.__len__()) < 3:
                    Asteroid.createasteroid(count=2)

                if (Enemy.all_enemies.__len__()) < 3:
                    newspeed = random.randint(3, 6)
                    Enemy.createenemy(speed=newspeed, maxhealth=100, timebetweenshooting=30, count=2)

                " Blitting all Sprites "

                screen.fill(deepblue)
                bgnd.setBgnd()
                Star.all_stars.draw(screen)
                Asteroid.all_asteroids.draw(screen)
                Enemy.all_enemies.draw(screen)
                PlayerProjectile.all_projectiles.draw(screen)
                EnemyProjectile.all_projectiles.draw(screen)
                player.draw_ship()
                player.draw_UI()
                player.muzzle_flash_effect()
                """enemy_ship.draw()
                enemy_ship.checkenemyposition()"""
                explosion.ast_exp(explosion.astPosX, explosion.astPosY)
                texttoscreen(text='Score: {0}'.format(player.score), size=12, pos_X=400, pos_Y=15)
                texttoscreen(text='Highscore: {0}'.format(player.highscore), size=15, color=vegasgold, pos_Y=15)
                ammo.draw_bar()
                pygame.display.update()
                clock.tick(30)

                if player.pause:
                    pause = True
                    while pause:
                        player.idling_engine_soundfx.stop()
                        texttoscreen("PAUSE", color=steelblue)
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    player.idling_engine_soundfx.play(loops=-1)
                                    player.pause = False
                                    pause = False

            pygame.quit()
            quit()


gameloop()
