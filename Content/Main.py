
from Content import Player, Enums, Config, Tiles, fx, Enemies, GUI
from .Config import Cfg
from .Button import Button
from .InputBox import InputBox
from .fx import Explosion, Effect
import pygame
import os
import random
import time

# todo - setting up the game/level states
curgamestate = Enums.GameStates.MainMenu.name
curlevelstate = Enums.LevelStates.Level1.name

all_sprites_list = pygame.sprite.Group()

" list comprehension, loading the ship fire effect "
ENGINE_FIRE = list([pygame.image.load(R'C:\Users\danba\PycharmProjects\Space-shooter-game\Sprites\jet_fire_{0}.png'
                                      .format(i)) for i in range(1, 9)])
SCALED_ENGINE_FIRE = list([])

"and scales the effect.."
for frame in ENGINE_FIRE:
    SCALED_ENGINE_FIRE.append(pygame.transform.smoothscale(frame, (70, 60)))

player = Player.SpaceShip()

player.set_image(R"C:\Users\danba\PycharmProjects\Space-shooter-game\Sprites\F5S4.png")
player.center_set_position(Config.Cfg.half_width, Config.Cfg.screen_height)

all_sprites_list.add(player)

bgnd = Tiles.TileSet()


" Loading the asteroid explosion sprite sheets into a list "
AST_EXP_SHEETS = list([pygame.image.load(R'C:\Users\danba\PycharmProjects\Space-shooter-game\Sprites'
                                         R'\fx\Asteroid_explosions_{0}.png'.format(i)) for i in range(1, 4)])

"loading all the asteroid sprites to a list"
ASTEROID_FRAMES = list([pygame.image.load(R'C:\Users\danba\PycharmProjects\Space-shooter-game\Sprites'
                                          R'\Asteroid sprites\Asteroid_{0}.png'.format(i)) for i in range(1, 61)])

# todo - what is this?
"""
EXPLOSION_FRAMES = list([pygame.image.load('Explosion_animation{0}.png'.format(i)) for i in range(1, 34)])
SCALED_EXPLOSION_FRAMES = []

for frames in EXPLOSION_FRAMES:
    SCALED_EXPLOSION_FRAMES.append(pygame.transform.smoothscale(frames, (60, 60)))
    """

explosion = Effect()
Effect.all_effects.add(explosion)


def game_over():

    player.idling_engine_soundfx.stop()
    text_to_screen(text='Game Over!')
    pygame.display.update()
    time.sleep(5)
    player.score = 0
    player.health = player.maxhealth
    bgnd.PosY = 0

    " Remove all sprites in data-structure/group."
    Enemies.Asteroid.killallasteroids()
    Enemies.Enemy.killallenemies()
    game_loop()


def text_to_screen(text, font=R'C:\Users\danba\PycharmProjects\Space-shooter-game\Fonts'
                              R'\spaceport1i.ttf', size=50, color=Config.Cfg.silver, pos_x=Config.Cfg.half_width,
                   pos_y=Config.Cfg.half_height):

    font = pygame.font.Font(font, size, bold=True)
    textsurf = font.render(text, True, color)
    text_rect = textsurf.get_rect()
    text_rect.center = (pos_x, pos_y)
    Config.Cfg.screen.blit(textsurf, text_rect)


""" Game Loop """


def game_loop():

    player.idling_engine_soundfx.set_volume(0.1)
    player.idling_engine_soundfx.play(loops=-1)
    ending = False
    fx.Star.createstarobjects()
    asteroid = Enemies.Asteroid(xpos=750, ypos=-500, start_frame=0)
    Enemies.Asteroid.all_asteroids.add(asteroid)
    enemy_ship = Enemies.Enemy(speed=4, maxhealth=100, timebetweenshooting=30)
    Enemies.Enemy.all_enemies.add(enemy_ship)
    ammo = GUI.EnergyBar()

    all_sprites_list.add([asteroid, enemy_ship])

    if curgamestate == Enums.GameStates.MainMenu.name:

        play_button = Button(Cfg.half_width, Cfg.half_height, 140, 32, 'Play')
        exit_button = Button(Cfg.half_width, Cfg.half_height + 50, 140, 32, 'Exit')
        buttons = [play_button, exit_button]
        in_main_menu = True
        "You Are in Main Menu!"
        "..."
        while in_main_menu:
            Cfg.screen.fill(Cfg.deepblue)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_main_menu = False

                for button in buttons:
                    button.handle_event(event)

            for button in buttons:
                if button.pressed:
                    # Some button is pressed , checking which one ->!
                    if button.text == "Play":
                        # todo - Let the player enter its name before gaming!
                        _text = Button(Cfg.half_width, (Cfg.half_height-50), 140, 32, 'Enter Name')
                        input_name_box = InputBox(Cfg.half_width, Cfg.half_height, 140, 32)
                        while in_main_menu:

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    in_main_menu = False
                                    continue
                                input_name_box.handle_event(event)

                            _text.update()
                            input_name_box.update()
                            Cfg.fill()
                            _text.draw(Cfg.screen)
                            input_name_box.draw(Cfg.screen)
                            Cfg.refresh()
                    elif button.text == "Exit":
                        in_main_menu = False

            for button in buttons:
                button.draw(Cfg.screen)
            Cfg.refresh()

    elif curgamestate == Enums.GameStates.InGame.name:

        "You are InGame!!"
        "..." \

        "WHAT LEVEL? ->"
        if curlevelstate == Enums.LevelStates.Level1.name:

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
                                projectile = Player.PlayerProjectile(posx=player.rect.x, posy=player.rect.y)
                                projectile.rect.centerx = player.rect.centerx
                                projectile.rect.bottom = player.rect.y - (projectile.rect.height * 2)
                                Player.PlayerProjectile.all_projectiles.add(projectile)
                                ammo.energyCur -= ammo.energyDrain
                        if event.key == pygame.K_p:
                            player.pause = True

                    """if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            player.acceleration_sound.stop()"""
                " UPDATE ALL MOVING SPRITES!   -------------- "

                Enemies.Enemy.all_enemies.update()
                Enemies.Asteroid.all_asteroids.update()
                Player.PlayerProjectile.all_projectiles.update(-50)
                Enemies.EnemyProjectile.all_projectiles.update(60)

                " Collition Detection! "

                player_hit_asteroids = pygame.sprite.spritecollide(player, Enemies.Asteroid.all_asteroids, True)
                proj_hit_asteroids = pygame.sprite.groupcollide(Enemies.Asteroid.all_asteroids, Player.PlayerProjectile
                                                                .all_projectiles, True,
                                                                True)
                enemyproj_hit_player = pygame.sprite.spritecollide(player, Enemies.EnemyProjectile.all_projectiles
                                                                   , False)
                playerproj_hit_enemies = pygame.sprite.groupcollide(Enemies.Enemy.all_enemies, Player.PlayerProjectile
                                                                    .all_projectiles, False,
                                                                    True)
                player_hit_enemies = pygame.sprite.spritecollide(player, Enemies.Enemy.all_enemies, True)

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
                    Enemies.Asteroid.createasteroid(count=3)

                for enemy in player_hit_enemies:
                    explosion.asteroidExpframes = AST_EXP_SHEETS[0]
                    explosion.astPosX = player.rect.x
                    explosion.astPosY = player.rect.y
                    explosion.playerexp = True
                    player.accelerationFire = False
                    player.health -= 2
                    Enemies.Asteroid.createasteroid(count=3)

                if (Enemies.Asteroid.all_asteroids.__len__()) < 3:
                    Enemies.Asteroid.createasteroid(count=2)

                if (Enemies.Enemy.all_enemies.__len__()) < 3:
                    newspeed = random.randint(3, 6)
                    Enemies.Enemy.createenemy(speed=newspeed, maxhealth=100, timebetweenshooting=30, count=2)

                " Blitting all Sprites "

                Cfg.screen.fill(Cfg.deepblue)
                bgnd.setBgnd()
                fx.Star.all_stars.draw(Cfg.screen)
                Enemies.Asteroid.all_asteroids.draw(Cfg.screen)
                Enemies.Enemy.all_enemies.draw(Cfg.screen)
                Player.PlayerProjectile.all_projectiles.draw(Cfg.screen)
                Enemies.EnemyProjectile.all_projectiles.draw(Cfg.screen)
                player.draw_ship()
                player.draw_UI()
                player.muzzle_flash_effect()
                """enemy_ship.draw()
                enemy_ship.checkenemyposition()"""
                explosion.ast_exp(explosion.astPosX, explosion.astPosY)
                text_to_screen(text='Score: {0}'.format(player.score), size=12, pos_x=400, pos_y=15)
                text_to_screen(text='Highscore: {0}'.format(player.highscore), size=15, color=Cfg.vegasgold, pos_y=15)
                ammo.draw_bar()
                pygame.display.update()
                Cfg.clock.tick(30)

                if player.pause:
                    pause = True
                    while pause:
                        player.idling_engine_soundfx.stop()
                        text_to_screen("PAUSE", color=Cfg.steelblue)
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    player.idling_engine_soundfx.play(loops=-1)
                                    player.pause = False
                                    pause = False

            pygame.quit()
            quit()


"calling the game loop"
game_loop()
