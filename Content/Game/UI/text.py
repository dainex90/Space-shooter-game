from typing import overload
import pygame

from Content.Game.Main import main
from Content.Game.Settings.config import Cfg
from Content.Game.States.gamestates import GameStates


class InputBox(pygame.sprite.Sprite):

    # Constants
    RECT_COLOR_INACTIVE:tuple = Cfg.darkgray
    RECT_COLOR_ACTIVE:tuple = Cfg.green
    DEFAULT_TEXT_COLOR:tuple = Cfg.silver
    FONT = pygame.font.Font(R'C:\Users\danie\PycharmProjects\Space-shooter-game\Fonts\spaceport1i.ttf', 32, bold=True)

    def __init__(self, x, y, width, height, text=''):

        super(InputBox, self).__init__()
        self.center_align_x = x - (width/2)
        self.center_align_y = y - (height/2)
        self.rect = pygame.Rect(self.center_align_x, self.center_align_y, width, height)
        self.rect_color = self.RECT_COLOR_INACTIVE
        self.text = text
        self.text_color = self.DEFAULT_TEXT_COLOR
        self.txt_surface = InputBox.FONT.render(text, True, self.text_color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            " If the user clicked on the input_box rectangle"
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                "Toggle the active variable"
                self.active = not self.active
            else:
                self.active = False
                'Change the current color of the input box'

            self.rect_color = InputBox.RECT_COLOR_ACTIVE if self.active else InputBox.RECT_COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active and event.key == pygame.K_RETURN and len(self.text) > 0:
            # todo - Save player name in a text file if not empty and start the game! 
                print('OK')
                main.curGameState = GameStates.inGame
                 #todo - i removed the game_loop in main.py! what to do here now? 
                 # game_loop()
            else:
                # todo - player has not entered a name.

                alert_text = InputBox(Cfg.screen_width, (Cfg.screen_height + 50), 140, 32, 'Enter a name!')
                alert_text.draw(Cfg.screen)
                print("Invalid Action!")

        elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

        else:
            self.text += event.unicode
            'Re-render the text'
            self.txt_surface = InputBox.FONT.render(self.text, True, self.text_color)

    def update(self):

        """Resize the box if the text is too long."""
        _width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = _width

    def draw(self, screen) -> None:
        """Blit the rect"""
        pygame.draw.rect(screen, self.rect_color, self.rect, 0)
        """Blit the text"""
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


"""Class for creating buttons in the game"""
class Button(InputBox, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text=''):

        super(Button, self).__init__(x, y, width, height, text)
        self.pressed:bool = False

    "Overrides base/super class, additional functionality"
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.rect_color = self.RECT_COLOR_ACTIVE

            else:
                self.rect_color = self.RECT_COLOR_INACTIVE
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                "Button is pressed"
                self.pressed = True

            else:
                "Button is not pressed"
                self.pressed = False

