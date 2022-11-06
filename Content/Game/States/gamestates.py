import enum


class GameStates():

    def __init__(self):
        super().__init__()

        self.MAIN_MENU: int = 1
        self.IN_GAME: int = 2
        self.PAUSE: int = 3
        self.EXIT: int = 4

        self.ALL_GAME_STATES = [self.MAIN_MENU, self.IN_GAME, self.PAUSE, self.EXIT]

        self._cur_game_state = None

    def set_game_state(self, state_to_set: int) -> None:
        for game_state in self.ALL_GAME_STATES:
            if game_state == state_to_set:
                self._cur_game_state = game_state

    def get_state(self) -> int:
        return self._cur_game_state
            


