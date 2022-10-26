
from abc import abstractclassmethod
import random
import time
from types import ClassMethodDescriptorType
import pygame

from Content.Game.Characters import enemy_module, player
from Content.Game.Effects import ast, game_effects
from Content.Game.Logic import game_logic
from Content.Game.Main import tiles
from Content.Game.Settings.config import Cfg
from Content.Game.States import gamestates
from Content.Game.States.gamestates import GameStates
from Content.Game.States.levelstates import LevelStates
from Content.Game.UI import text, ui   
from Content.Game.Main.main import game_state, level_state, explosion, energy_resource


class GameHandler(pygame.sprite.Sprite):

    # Class members 
    background = tiles.TileSet()

    player_hit_asteroids: list = []
    proj_hit_asteroids: list = []
    enemy_projectile_hit_player: list = []
    player_projectile_hit_enemies: list = []
    player_hit_enemies: list = []
    new_player: player.SpaceShip


    @classmethod
    def game_over(cls) -> None:

        cls.new_player.idling_engine_soundfx.stop()
        cls.text_to_screen(text='Game Over!')
        pygame.display.update()
        time.sleep(5)
        cls.new_player.score = 0
        cls.new_player.health = cls.new_player.maxhealth
        cls.background.PosY = 0 

        " Remove all sprites in data-structure/group."
        ast.Asteroid.kill_all_asteroids()
        enemy_module.Enemy.killallenemies()
    

    @staticmethod
    def text_to_screen(text:str, font=R'C:\Users\danba\PycharmProjects\Space-shooter-game\Fonts'
                    R'\spaceport1i.ttf', size:int =50, color: tuple =Cfg.silver, pos_x:float =Cfg.half_width,
                   pos_y: float=Cfg.half_height) -> None:

        font = pygame.font.Font(font, size)
        textsurf = font.render(text, True, color)
        text_rect = textsurf.get_rect()
        text_rect.center = (pos_x, pos_y)
        Cfg.screen.blit(textsurf, text_rect)


    @staticmethod
    def in_main_menu() -> None:

        play_button = text.Button(Cfg.half_width, Cfg.half_height, 140, 32, 'Play')
        exit_button = text.Button(Cfg.half_width, Cfg.half_height + 50, 140, 32, 'Exit')
        buttons:list = [play_button, exit_button]

        # Keep on looping the Menu
        while game_state.get_state() == 1:
            "You Are in Main Menu!"
            Cfg.screen.fill(Cfg.deepblue)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quitting Game
                    game_state.set_game_state(4)

                for button in buttons:
                    button.handle_event(event)

            for button in buttons:
                if button.pressed:

                    # Some button is pressed , checking which one ->!
                    if button.text == "Play":
                        # todo - Let the cls.new_player enter its name before playing!
                        _text = text.Button(Cfg.half_width, (Cfg.half_height-50), 140, 32, 'Enter Name')
                        input_name_box = text.InputBox(Cfg.half_width, Cfg.half_height, 140, 32)

                        while game_state.get_state() == 1:

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    game_state.set_game_state(4)
                                    continue

                                input_name_box.handle_event(event)

                            _text.update()
                            input_name_box.update()
                            Cfg.fill()
                            _text.draw(Cfg.screen)
                            input_name_box.draw(Cfg.screen)
                            Cfg.refresh()
                    elif button.text == "Exit":
                        game_state.set_game_state(4)

            for button in buttons:
                button.draw(Cfg.screen)
            Cfg.refresh()


    @classmethod
    def in_game(cls) -> None:
        
        cls.new_player = player.SpaceShip()
        game_state.set_game_state(2)
        level_state.set_level_state(1)
        while game_state.get_state() == 2 and level_state.get_level_state() == 1:
                
            if cls.new_player.cur_velocity_x == 0:
                cls.new_player.left = False
                cls.new_player.right = False

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
                            cls.new_player.right = False
                        else:
                            cls.new_player.right = True
                            cls.new_player.left = False

                    if event.key == pygame.K_a:
                        if explosion.player_explosion:
                            cls.new_player.left = False
                        else:
                            cls.new_player.left = True
                            cls.new_player.right = False

                    if event.key == pygame.K_w:
                        if explosion.player_explosion:
                            cls.new_player.forward = False
                        else:
                            cls.new_player.acceleration_fire = True
                            cls.new_player.forward = True
                            cls.new_player.backward = False

                    if event.key == pygame.K_s:
                        if explosion.player_explosion:
                            cls.new_player.backward = False
                        else:
                            cls.new_player.acceleration_fire = False
                            cls.new_player.backward = True
                            cls.new_player.forward = False

                    if event.key == pygame.K_SPACE:
                        if not energy_resource.overload:
                            cls.new_player.isshooting = True
                            projectile = game_effects.PlayerProjectile(posx=cls.new_player.rect.x, posy=cls.new_player.rect.y)
                            projectile.rect.centerx = cls.new_player.rect.centerx
                            projectile.rect.bottom = cls.new_player.rect.y - (projectile.rect.height * 2)
                            game_effects.PlayerProjectile.all_projectiles.add(projectile)
                            energy_resource.energyCur -= energy_resource.energyDrain
                    if event.key == pygame.K_p:
                        cls.new_player.pause = True

    @staticmethod
    def update_all_sprites() -> None:
        # UPDATE ALL MOVING SPRITES!  UPDATE LOGIC ->  --------------
        enemy_module.Enemy.all_enemies.update()
        ast.Asteroid.all_asteroids.update()
        game_effects.PlayerProjectile.all_projectiles.update(-50)
        game_effects.EnemyProjectile.all_projectiles.update(60)
            

    @classmethod
    def create_collide_groups(cls) -> None:
        # Creating the collide groups to check for collitions later -
        cls.player_hit_asteroids = pygame.sprite.spritecollide(cls.new_player, ast.Asteroid.all_asteroids, True)
        cls.proj_hit_asteroids = pygame.sprite.groupcollide(ast.Asteroid.all_asteroids, game_effects.PlayerProjectile
                                                        .all_projectiles, True,
                                                        True)
        cls.enemy_projectile_hit_player = pygame.sprite.spritecollide(cls.new_player, game_effects.EnemyProjectile.all_projectiles
                                                            , False)
        cls.player_projectile_hit_enemies = pygame.sprite.groupcollide(enemy_module.Enemy.all_enemies, game_effects.PlayerProjectile
                                                            .all_projectiles, False,
                                                            True)
        cls.player_hit_enemies = pygame.sprite.spritecollide(cls.new_player, enemy_module.Enemy.all_enemies, True)

    @classmethod
    def checking_collide_groups(cls) -> None:
        # Collition Detection -> "
        # looping through the collide-groups-

        for asteroid in cls.proj_hit_asteroids:
            asteroid.sound_effect.set_volume(1.0)
            asteroid.sound_effect.play()
            explosion.sheetType = random.randint(0, 2)
            explosion.asteroidExpframes = game_effects.ASTEROID_EXPLOSION_SHEETS[explosion.sheetType]
            explosion.astPosX = asteroid.rect.x
            explosion.astPosY = asteroid.rect.y
            explosion.astexp = True

        for enemy in cls.player_projectile_hit_enemies:
            enemy.health -= 20
            if not enemy.isalive():
                game_logic.Score.set_score(amount=5)
                explosion.sheetType = random.randint(0, 2)
                explosion.asteroidExpframes = game_effects.ASTEROID_EXPLOSION_SHEETS[explosion.sheetType]
                explosion.astPosX = enemy.rect.x
                explosion.astPosY = enemy.rect.y
                explosion.enemyexp = True
                enemy.kill()

        for projectile in cls.enemy_projectile_hit_player:
            explosion.asteroidExpframes = game_effects.ASTEROID_EXPLOSION_SHEETS[1]
            explosion.astPosX = projectile.rect.x
            explosion.astPosY = projectile.rect.y
            explosion.player_explosion = True
            cls.new_player.acceleration_fire = False
            cls.new_player.health -= 1
            projectile.kill()
            if not cls.new_player.isalive():
                cls.game_over()

        for asteroid in cls.player_hit_asteroids:
            explosion.asteroidExpframes = game_effects.ASTEROID_EXPLOSION_SHEETS[1]
            explosion.astPosX = cls.new_player.rect.x
            explosion.astPosY = cls.new_player.rect.y
            explosion.player_explosion = True
            cls.new_player.acceleration_fire = False
            cls.new_player.health -= 2
            ast.Asteroid.create_asteroid(count=3)

        for enemy in cls.player_hit_enemies:
            explosion.asteroidExpframes = game_effects.ASTEROID_EXPLOSION_SHEETS[0]
            explosion.astPosX = cls.new_player.rect.x
            explosion.astPosY = cls.new_player.rect.y
            explosion.player_explosion = True
            cls.new_player.acceleration_fire = False
            cls.new_player.health -= 2
            ast.Asteroid.create_asteroid(count=3)

    @classmethod
    def create_new_enemies(cls, treshhold: int) -> None:
        # create new enemies if under treshhold
        if (ast.Asteroid.all_asteroids.__len__()) < treshhold:
            ast.Asteroid.create_asteroid(count=2)

        if (enemy_module.Enemy.all_enemies.__len__()) < treshhold:
            for _ in range(2):
                newspeed: int = random.randint(4, 8)
                enemy_module.Enemy.create_enemy(speed=newspeed, maxhealth=100, timebetweenshooting=30, count=1)
    
    @classmethod
    def blit_all_sprites(cls) -> None:
        " Blitting all Sprites "
        Cfg.screen.fill(Cfg.deepblue)
        cls.background.set_bgnd()
        game_effects.Star.all_stars.draw(Cfg.screen)
        ast.Asteroid.all_asteroids.draw(Cfg.screen)
        enemy_module.Enemy.all_enemies.draw(Cfg.screen)
        game_effects.PlayerProjectile.all_projectiles.draw(Cfg.screen)
        game_effects.EnemyProjectile.all_projectiles.draw(Cfg.screen)
        cls.new_player.draw_ship()
        cls.new_player.draw_ui()
        cls.new_player.muzzle_flash_effect()

        """enemy_ship.draw()
        enemy_ship.checkenemyposition()"""

        explosion.ast_exp(explosion.astPosX, explosion.astPosY, cls.new_player)
        cls.text_to_screen(text='Score: {0}'.format(cls.new_player.score), size=12, pos_x=400, pos_y=15)
        cls.text_to_screen(text='Highscore: {0}'.format(cls.new_player.highscore), size=15, color=Cfg.vegasgold, pos_y=15)
        energy_resource.draw_bar()  

    @classmethod
    def game_pause(cls) -> None:
        # checking if game is paused.
        if cls.new_player.pause:
            pause: bool = True
            while pause:
                cls.new_player.idling_engine_soundfx.stop()
                cls.text_to_screen("PAUSE", color=Cfg.steelblue)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            cls.new_player.idling_engine_soundfx.play(loops=-1)
                            cls.new_player.pause = False
                            pause = False