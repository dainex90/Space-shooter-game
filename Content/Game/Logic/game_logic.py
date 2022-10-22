import pygame

from Content.Game.Characters import player


class Score(pygame.sprite.Sprite):

    def __init__(self, _score=None, _increaseAmount=None, _decreaseAmount=None):

        super(Score, self).__init__()

        self.score = _score
        self.increaseAmount = _increaseAmount
        self.decreaseAmount = _decreaseAmount

    """
    @classmethod
    def set_score(amount):

        #todo -> functionality for setting a score bound to the specific player based on the enemy-type
        "what enemy-type?"

        player.score += amount 
        """


class Highscore(Score):
    def __init__(self):

        super(Highscore, self).__init__()

