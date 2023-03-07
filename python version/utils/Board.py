import numpy as np


class Board:
    '''
        params:
        {
            self.award_list : the awards in each board
            self.dices_info : record the dices of each players of each board 
            self.update(): update the dices on each board with each players' decisions and return a dict with
                            each players' dices on the board
            self.relate_num : the related number of each board in cases with 1,2,3,4,5,6

        }
    '''

    def __init__(self, award_list: list, relate_num: int):
        self.award_list = award_list
        self.dices_info = dict()
        self.relate_number = relate_num

    def update(self, player: int, num: int) -> dict:  # Update the number of dices on each board
        if player in self.dices_info.keys():
            self.dices_info[player] += num
        else:
            self.dices_info.update({player: num})
        return self.dices_info

    def get_reward_names(self) -> list:  # return the award list for certain player
        players, dices = np.array(list(self.dices_info.keys())), np.array(
            list(self.dices_info.values()))
        arr_index = dices.argsort()
        players, dices = players[arr_index][::-1], dices[arr_index][::-1]
        awards_num = len(self.award_list)
        award_player_num = []
        unique_dice = np.sort(np.unique(dices))[::-1]
        for u_dice in unique_dice:
            if dices.tolist().count(u_dice) == 1 and len(award_player_num) < awards_num:
                index = dices.tolist().index(u_dice)
                award_player_num.append(players[index])
        return award_player_num
