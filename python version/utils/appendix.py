from random import choice
from .Board import Board
from .NameMatch import name_player_index
import matplotlib.pyplot as plt

board_numbers = 6

def split(total_awards: int, nominal_value: list = [10000, 30000, 50000, 70000, 100000]) -> list:
    total = total_awards
    awards_list = list()
    while total > 0:
        for value in nominal_value:
            awards_list.append(value)
            total -= value
    return awards_list


def distribute(total_awards: int, nominal_value: list = [10000, 30000, 50000, 70000, 100000]) -> list:
    awards_list = split(total_awards, nominal_value)
    distributions = list()
    nominal_value.sort()
    target_values = [nominal_value[-1], nominal_value[-2]]
    while len(awards_list) > 0:
        distribution = []
        for i in range(3):
            p = choice(awards_list)
            distribution.append(p)
            awards_list.remove(p)
            if p in target_values:
                break
        distributions.append(distribution)
    while len(awards_list) % board_numbers != 0:
        distributions.append([0])
    return distributions

def check(name_players: dict):
    for player in name_players.values():
        if player.dices > 0:
            return True
    return False

def display_board_info(name_boards : dict):
    for name in name_boards.keys():
        board = name_boards[name]
        print(f"Board {name} {board.award_list}:")
        for k,v in zip(board.dices_info.keys(), board.dices_info.values()):
            print(f"{name_player_index[k]} has {v} dices on {name} board")

def show_all_rewards(name_players : dict):
    awards = [name_players[name].total_award for name in name_players.keys()]
    names = list(name_players.keys())
    plt.title('Currrent Awards Distributions')
    plt.bar(range(len(names)), awards, tick_label = names)
    plt.savefig('./img/current_result.jpg')