import cls as cls
import pygame
import os
import random
import time
from enum import Enum

"Class Namespaces/Modules! --->"


from _Content.Player import *


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
ENGINE_FIRE = list([pygame.image.load(r'C:\Users\danba\PycharmProjects\Space-shooter-game\Sprites\jet_fire_{0}.png'
                                      .format(i)) for i in range(1, 9)])
SCALED_ENGINE_FIRE = list([])

for frame in ENGINE_FIRE:
    SCALED_ENGINE_FIRE.append(pygame.transform.smoothscale(frame, (70, 60)))

player = SpaceShip()

player.set_image("F5S4.png")
player.center_set_position(half_width, screen_height)

all_sprites_list.add(player)

bgnd = TileSet()

" LIST COMPREHENSIONS! "

AST_EXP_SHEETS = list([pygame.image.load('Asteroid_explosions_{0}.png'.format(i)) for i in range(1, 4)])
ASTEROID_FRAMES = list([pygame.image.load('Asteroid_{0}.png'.format(i)) for i in range(1, 61)])
EXPLOSION_FRAMES = list([pygame.image.load('Explosion_animation{0}.png'.format(i)) for i in range(1, 34)])
SCALED_EXPLOSION_FRAMES = []

for frames in EXPLOSION_FRAMES:
    SCALED_EXPLOSION_FRAMES.append(pygame.transform.smoothscale(frames, (60, 60)))

explosion = Effect()
Effect.all_effects.add(explosion)


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


""" Game Loop --> """


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
