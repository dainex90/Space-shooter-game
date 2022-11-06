import enum
from typing import Literal


class LevelStates():

    def __init__(self):
        super().__init__()

        self.LEVEL_1: int = 1
        self.LEVEL_2: int  = 2
        self.LEVEL_3: int = 3

        self.ALL_LEVEL_STATES = [self.LEVEL_1, self.LEVEL_2, self.LEVEL_3]
        self.cur_level_state = None

    def set_level_state(self, state_to_set: int) -> None:
        # set to a new state 
        for level_state in self.ALL_LEVEL_STATES:
            if level_state == state_to_set:
                self.cur_level_state = level_state

    def get_level_state(self) -> int:
        # get the current level state 
        return self.cur_level_state 
    

