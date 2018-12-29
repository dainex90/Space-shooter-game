
from _Content.Main import *


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
