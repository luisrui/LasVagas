from .Board import Board
import numpy as np

class Player:
    '''
        params:
        {
            self.index : the number of each player
            self.dices : the number of dices of each players in each round
            self.total_award : the number of total awards of each player
        }
    '''

    def __init__(self, index: int, ini_dices: int):
        self.index = index
        self.dices = ini_dices
        self.total_award = 0

    def shuffle(self) -> np.ndarray:
        result = np.sort(np.random.randint(1, 7, size = self.dices))
        return result

    def decide(self, board: Board, num: int):
        info = board.update(self.index, num)
        self.dices -= num
    
    def get_reward(self, reward:int):
        self.total_award += reward

        