
import pygame as pg
from .InputBox import InputBox
from .Config import Cfg
import sys


"""for creating the buttons in game"""


class Button(InputBox, pg.sprite.Sprite):
    def __init__(self, x, y, width, height, text=''):

        super(Button, self).__init__(x, y, width, height, text)
        self.pressed = False

    "Overrides base/super class, additional functionality"
    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]):
                self.rect_color = self.RECT_COLOR_ACTIVE

            else:
                self.rect_color = self.RECT_COLOR_INACTIVE
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]):

                "Button is pressed"
                self.pressed = True

            else:
                "Button is not pressed"
                self.pressed = False

    "Checks which button is pressed"
    # def button_check(self):
    #
    #     if self.text == "Play":
    #         #todo - Let the user enter its name before playing using InputBox!
    #         return InputBox(Cfg.half_width, Cfg.half_height, 140, 32)
    #
    #     elif self.text == "Exit":
    #         return None
