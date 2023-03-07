import argparse

from utils.NameMatch import player_names, board_names, name_player_index
from utils.Board import Board
from utils.Player import Player
from utils.appendix import distribute, board_numbers, display_board_info, check, show_all_rewards


def parse_args():
    parser = argparse.ArgumentParser(
        description='Start a new LasVagas Board Game!')
    parser.add_argument('num_of_players', type=int, help='Number of players')
    parser.add_argument('num_of_boards', type=int, help='Number of boards')
    parser.add_argument('num_of_dices', type=int,
                        help='Number of dices of each player')
    parser.add_argument('total_awards', type=int, help='Number of players')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    name_players, name_boards = dict(), dict()
    distributions = distribute(args.total_awards)
    if args.num_of_players < len(player_names):
        # Initialize of players
        for i in range(args.num_of_players):
            player_name = player_names[i]
            name_players.update({player_name: Player(i, args.num_of_dices)})
        # Initialize of board_games
        print('Welcome to LasVagas Board Game!\n')
        print(
            f"We have {args.num_of_players} players in today's match! Let me introduce each player's name first! You are:\n")
        for p_name in name_players.keys():
            print(p_name, end=' ')
        print('Lets begin!!!!!!!!\n')
        print('-----------------------------------------------------------------------\n')
        round = 0
        # Each round of board_games
        while round * board_numbers < len(distributions):
            for j in range(len(board_names)):
                board_name = board_names[j]
                name_boards.update(
                    {board_name: Board(distributions[round * board_numbers + j], j + 1)})
            # Show award list of each board
            print(f'Round {round + 1}: The awards on each board are:\n')
            for b_name in name_boards.keys():
                current_board = name_boards[b_name]
                print(f'Board {b_name}: {current_board.award_list}')
            # Each player of selection:
            while check(name_players):
                for p_name in name_players.keys():
                    if name_players[p_name].dices == 0:
                        print(
                            f"{p_name}'s dices are already empty, next player!\n")
                        continue
                    print(f'\nTurn of player {p_name}:\n')
                    current_player = name_players[p_name]
                    result = current_player.shuffle()
                    for r in result:
                        print(r, end=' ')
                    num_of_choice = 0
                    while num_of_choice == 0:
                        choice = int(input(f"\n{p_name}'s choice is: "))
                        num_of_choice = result.tolist().count(choice)
                        if num_of_choice == 0:
                            print('Please select the number from the result!\n')
                    board_choice = 0
                    for board in name_boards.values():
                        if board.relate_number == choice:
                            board_choice = board
                            break
                    current_player.decide(board_choice, num_of_choice)
                    print('-------show current info ----------\n')
                    display_board_info(name_boards)
                    print('-------show current info ----------\n')
            # Get rewards
            for board in name_boards.values():
                award_name_indexs = board.get_reward_names()
                for award, award_name_index in zip(board.award_list, award_name_indexs):
                    player_name = name_player_index[award_name_index]
                    name_players[player_name].get_reward(award)
            show_all_rewards(name_players)
            round += 1
            print('----------------------next round---------------------------\n')
    else:
        print(
            f'Excessive players! Try to reduce player number to {len(player_names)}!\n')


if __name__ == '__main__':
    main()
