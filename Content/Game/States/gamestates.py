

class GameStates:

    mainMenu = ""
    inGame = ""
    pause = ""
    exit = ""

    def __init__(self, mainMenu, inGame, pause, exit):
        super().__init__()

        self.mainMenu = mainMenu
        self.inGame = inGame
        self.pause = pause
        self.exit = exit

