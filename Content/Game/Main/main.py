
# Packages

from cgitb import handler
import pygame
import math
import random
import time

# Local Packages
from Content.Game.States import gamestates, levelstates
from Content.Game.Characters import player, enemy_module
from Content.Game.Main import game_handler, tiles
from Content.Game.Effects import game_effects, ast
from Content.Game.UI import text, ui
from Content.Game.Logic import game_logic
from Content.Game.Settings import config


# Setting up the game/level states
game_state = gamestates.GameStates()
game_state.set_game_state(1)

level_state = levelstates.LevelStates()
level_state.set_level_state(1)


all_sprites_list = pygame.sprite.Group()

player = player.SpaceShip()

player.set_image(config.Cfg.get_sprite_from_path("F5S4.png"))
player.center_set_position(config.Cfg.half_width, config.Cfg.screen_height)

all_sprites_list.add(player)

explosion = game_effects.Effect()
game_effects.Effect.all_effects.add(explosion)


player.idling_engine_soundfx.set_volume(0.1)
player.idling_engine_soundfx.play(loops=-1)

game_effects.Star.createstarobjects()
asteroid = ast.Asteroid(xpos=750, ypos=-500, start_frame=0)
ast.Asteroid.all_asteroids.add(asteroid)

enemy_ship = enemy_module.Enemy(speed=4, maxhealth=100, timebetweenshooting=30)
enemy_module.Enemy.all_enemies.add(enemy_ship)
energy_resource = ui.EnergyBar()

all_sprites_list.add([asteroid, enemy_ship])

# Initializing the GAMEHANDLER CLASS and creating the player instance inside its constructor .

# checking if we are in Main Menu ->
if game_state.get_state() == 1:
    game_handler.GameHandler.in_main_menu()

# Checking if Game State is IN_GAME 
elif game_state.get_state() == 2:
    
    if level_state.get_level_state == 1:
        " LEVEL 1 HERE "

        game_handler.GameHandler.in_game()

        game_handler.GameHandler.update_all_sprites()

        game_handler.GameHandler.create_collide_groups()

        game_handler.GameHandler.checking_collide_groups()

        game_handler.GameHandler.create_new_enemies(treshhold=3)

        game_handler.GameHandler.game_pause()
    
        pygame.display.update()
        config.Cfg.clock.tick(30)
        pygame.quit()
        quit()

""" END OF MAIN!"""
