
# Packages
from Content.Game import Characters
import pygame
import os
import random
import time
import math


# Local Packages
from Content.Game.States import gamestates
from Content.Game.States import levelstates
from Content.Game.Characters import player
from Content.Game.Main import tiles
from Content.Game.Effects import game_effects
from Content.Game.Characters import enemy_module
from Content.Game.Effects import ast
from Content.Game.UI import text
from Content.Game.UI import ui
from Content.Game.Logic import game_logic
from Content.Game.Settings import config

# todo - setting up the game/level states

gameStates =  gamestates.GameStates("MainMenu", "InGame", "Pause", "Exit")
curGameState: str = gameStates.mainMenu
levelStates = levelstates.LevelStates("level1", "level2", "level3")
curLevelState: str = levelStates.level1

all_sprites_list: list = pygame.sprite.Group()
game_ending: bool = False

" list comprehension, loading the ship fire effect "
ENGINE_FIRE = list([pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites\jet_fire_{0}.png'
                                      .format(i)) for i in range(1, 9)])
SCALED_ENGINE_FIRE = list([])

"and scales the effect.."
for frame in ENGINE_FIRE:
    SCALED_ENGINE_FIRE.append(pygame.transform.smoothscale(frame, (70, 60)))

player = player.SpaceShip()

player.set_image(R"C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites\F5S4.png")
player.center_set_position(config.Cfg.half_width, config.Cfg.screen_height)

all_sprites_list.add(player)

background = tiles.TileSet()

" Loading the asteroid explosion sprite sheets into a list "
ASTEROID_EXPLOSION_SHEETS: list = list([pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites'
                                         R'\fx\Asteroid_explosions_{0}.png'.format(i)) for i in range(1, 4)])

"loading all the asteroid sprites to a list"
ASTEROID_FRAMES: list = list([pygame.image.load(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Sprites'
                                          R'\Asteroid sprites\Asteroid_{0}.png'.format(i)) for i in range(1, 61)])

explosion = game_effects.Effect(ASTEROID_EXPLOSION_SHEETS)
game_effects.Effect.all_effects.add(explosion)


def game_over() -> None:

    player.idling_engine_soundfx.stop()
    text_to_screen(text='Game Over!')
    pygame.display.update()
    time.sleep(5)
    player.score = 0
    player.health = player.maxhealth
    background.PosY = 0

    " Remove all sprites in data-structure/group."
    ast.Asteroid.kill_all_asteroids()
    enemy_module.Enemy.killallenemies()
    # TODO I removed the game_loop, need to do it another way!
    #game_loop()


def text_to_screen(text:str, font=R'C:\Users\danba\PycharmProjects\Space-shooter-game\Fonts'
                    R'\spaceport1i.ttf', size:int =50, color: tuple =config.Cfg.silver, pos_x:float =config.Cfg.half_width,
                   pos_y: float=config.Cfg.half_height) -> None:

    font = pygame.font.Font(font, size, bold=True)
    textsurf = font.render(text, True, color)
    text_rect = textsurf.get_rect()
    text_rect.center: tuple = (pos_x, pos_y)
    config.Cfg.screen.blit(textsurf, text_rect)


player.idling_engine_soundfx.set_volume(0.1)
player.idling_engine_soundfx.play(loops=-1)

game_effects.Star.createstarobjects()
asteroid = ast.Asteroid(ASTEROID_FRAMES, xpos=750, ypos=-500, start_frame=0)
ast.Asteroid.all_asteroids.add(asteroid)
enemy_ship = enemy_module.Enemy(speed=4, maxhealth=100, timebetweenshooting=30)
enemy_module.Enemy.all_enemies.add(enemy_ship)
energy_resource = ui.EnergyBar()

all_sprites_list.add([asteroid, enemy_ship])


# Main menu ->
if curGameState == gamestates.GameStates.mainMenu:

    play_button = text.Button(config.Cfg.half_width, config.half_height, 140, 32, 'Play')
    exit_button = text.Button(config.Cfg.half_width, config.Cfg.half_height + 50, 140, 32, 'Exit')
    buttons:list = [play_button, exit_button]

    in_main_menu: bool = True

    while in_main_menu:
        "You Are in Main Menu!"
        config.Cfg.screen.fill(config.Cfg.deepblue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False

            for button in buttons:
                button.handle_event(event)

        for button in buttons:
            if button.pressed:

                # Some button is pressed , checking which one ->!
                if button.text == "Play":
                    # todo - Let the player enter its name before playing!
                    _text = text.Button(config.Cfg.half_width, (config.Cfg.half_height-50), 140, 32, 'Enter Name')
                    input_name_box = text.InputBox(config.Cfg.half_width, config.Cfg.half_height, 140, 32)
                    while in_main_menu:

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                in_main_menu = False
                                continue
                            input_name_box.handle_event(event)

                        _text.update()
                        input_name_box.update()
                        config.Cfg.fill()
                        _text.draw(config.Cfg.screen)
                        input_name_box.draw(config.Cfg.screen)
                        config.Cfg.refresh()
                elif button.text == "Exit":
                    in_main_menu = False

        for button in buttons:
            button.draw(config.Cfg.screen)
        config.Cfg.refresh()

elif curGameState == gamestates.GameStates.inGame:

    "You are InGame!!"
    "..." \

    "WHAT LEVEL? ->"
    if curLevelState == levelstates.LevelStates.Level1:

        " LEVEL 1 HERE "
        while not game_ending:

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
                        if explosion.player_explosion:
                            player.right = False
                        else:
                            player.right = True
                            player.left = False

                    if event.key == pygame.K_a:
                        if explosion.player_explosion:
                            player.left = False
                        else:
                            player.left = True
                            player.right = False

                    if event.key == pygame.K_w:
                        if explosion.player_explosion:
                            player.forward = False
                        else:
                            player.acceleration_fire = True
                            player.forward = True
                            player.backward = False

                    if event.key == pygame.K_s:
                        if explosion.player_explosion:
                            player.backward = False
                        else:
                            player.acceleration_fire = False
                            player.backward = True
                            player.forward = False

                    if event.key == pygame.K_SPACE:
                        if not energy_resource.overload:
                            player.isshooting = True
                            projectile = game_effects.PlayerProjectile(posx=player.rect.x, posy=player.rect.y)
                            projectile.rect.centerx = player.rect.centerx
                            projectile.rect.bottom = player.rect.y - (projectile.rect.height * 2)
                            game_effects.PlayerProjectile.all_projectiles.add(projectile)
                            energy_resource.energyCur -= energy_resource.energyDrain
                    if event.key == pygame.K_p:
                        player.pause = True


            " UPDATE ALL MOVING SPRITES!   -------------- "
            enemy_module.Enemy.all_enemies.update()
            ast.Asteroid.all_asteroids.update()
            game_effects.PlayerProjectile.all_projectiles.update(-50)
            game_effects.EnemyProjectile.all_projectiles.update(60)

            " Collition Detection! "

            player_hit_asteroids = pygame.sprite.spritecollide(player, ast.Asteroid.all_asteroids, True)
            proj_hit_asteroids = pygame.sprite.groupcollide(ast.Asteroid.all_asteroids, game_effects.PlayerProjectile
                                                            .all_projectiles, True,
                                                            True)
            enemy_projectile_hit_player = pygame.sprite.spritecollide(player, game_effects.EnemyProjectile.all_projectiles
                                                                , False)
            player_projectile_hit_enemies = pygame.sprite.groupcollide(enemy_module.Enemy.all_enemies, game_effects.PlayerProjectile
                                                                .all_projectiles, False,
                                                                True)
            player_hit_enemies = pygame.sprite.spritecollide(player, enemy_module.Enemy.all_enemies, True)

            for asteroid in proj_hit_asteroids:
                asteroid.sound_effect.set_volume(1.0)
                asteroid.sound_effect.play()
                explosion.sheetType = random.randint(0, 2)
                explosion.asteroidExpframes = ASTEROID_EXPLOSION_SHEETS[explosion.sheetType]
                explosion.astPosX = asteroid.rect.x
                explosion.astPosY = asteroid.rect.y
                explosion.astexp = True

            for enemy in player_projectile_hit_enemies:
                enemy.health -= 20
                if not enemy.isalive():
                    game_logic.Score.set_score(amount=5)
                    explosion.sheetType = random.randint(0, 2)
                    explosion.asteroidExpframes = ASTEROID_EXPLOSION_SHEETS[explosion.sheetType]
                    explosion.astPosX = enemy.rect.x
                    explosion.astPosY = enemy.rect.y
                    explosion.enemyexp = True
                    enemy.kill()

            for projectile in enemy_projectile_hit_player:
                explosion.asteroidExpframes = ASTEROID_EXPLOSION_SHEETS[1]
                explosion.astPosX = projectile.rect.x
                explosion.astPosY = projectile.rect.y
                explosion.player_explosion = True
                player.acceleration_fire = False
                player.health -= 1
                projectile.kill()
                if not player.isalive():
                    game_over()

            for asteroid in player_hit_asteroids:
                explosion.asteroidExpframes = ASTEROID_EXPLOSION_SHEETS[1]
                explosion.astPosX = player.rect.x
                explosion.astPosY = player.rect.y
                explosion.player_explosion = True
                player.acceleration_fire = False
                player.health -= 2
                ast.Asteroid.create_asteroid(count=3)

            for enemy in player_hit_enemies:
                explosion.asteroidExpframes = ASTEROID_EXPLOSION_SHEETS[0]
                explosion.astPosX = player.rect.x
                explosion.astPosY = player.rect.y
                explosion.player_explosion = True
                player.acceleration_fire = False
                player.health -= 2
                ast.Asteroid.create_asteroid(count=3)

            if (ast.Asteroid.all_asteroids.__len__()) < 3:
                ast.Asteroid.create_asteroid(count=2)

            if (enemy_module.Enemy.all_enemies.__len__()) < 2:
                for _ in range(2):
                    newspeed: int = random.randint(4, 8)
                    enemy_module.Enemy.create_enemy(speed=newspeed, maxhealth=100, timebetweenshooting=30, count=1)


            " Blitting all Sprites "
            config.Cfg.screen.fill(config.Cfg.deepblue)
            background.set_bgnd()
            game_effects.Star.all_stars.draw(config.Cfg.screen)
            ast.Asteroid.all_asteroids.draw(config.Cfg.screen)
            enemy_module.Enemy.all_enemies.draw(config.Cfg.screen)
            game_effects.PlayerProjectile.all_projectiles.draw(config.Cfg.screen)
            game_effects.EnemyProjectile.all_projectiles.draw(config.Cfg.screen)
            player.draw_ship()
            player.draw_ui()
            player.muzzle_flash_effect()
            """enemy_ship.draw()
            enemy_ship.checkenemyposition()"""
            explosion.ast_exp(explosion.astPosX, explosion.astPosY)
            text_to_screen(text='Score: {0}'.format(player.score), size=12, pos_x=400, pos_y=15)
            text_to_screen(text='Highscore: {0}'.format(player.highscore), size=15, color=config.Cfg.vegasgold, pos_y=15)
            energy_resource.draw_bar()
            pygame.display.update()
            config.Cfg.clock.tick(30)

            if player.pause:
                pause: bool = True
                while pause:
                    player.idling_engine_soundfx.stop()
                    text_to_screen("PAUSE", color=config.Cfg.steelblue)
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                player.idling_engine_soundfx.play(loops=-1)
                                player.pause = False
                                pause = False

        pygame.quit()
        quit()


""" END OF MAIN!"""










