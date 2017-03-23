import os
import time
player1_points = 0
player2_points = 0


class textformats:
    DEFAULT = '\033[0m'
    UNDER = '\033[4m'
    BOLD = '\033[1m'
    CYAN = '\033[0;36m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'


def game_info():
    os.system("clear")
    print("""
  ____        _   _   _           _     _       
 | __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __  
 |  _ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
 | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
 |____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                         |_|    """)
    print("\nThis is a hot-seat multiplayer Battleship game. Each player has five ships,")
    print("which they position in ascending order. After placing the ships the battle ")
    print("begins. If someone loses all their ships, the round ends.\n")
    print("The game will last until one of the players reach 5 points.\n")
    print("Board symbols: ")
    print("'~' : the vast ocean\n'#' : ship\n'o' : shot that didn't hit anything\n'x' : shot that hit a ship")
    print("\nHave fun!")
    time.sleep(10)


def game_menu():
    os.system('clear')
    print("""
  ____        _   _   _           _     _       
 | __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __  
 |  _ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
 | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
 |____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                         |_|    """)
    print("\n" + textformats.UNDER + "Game menu\n\n" + textformats.DEFAULT)
    print(textformats.BOLD + "[P]" + textformats.DEFAULT + "lay game\n")
    print(textformats.BOLD + "[E]" + textformats.DEFAULT + "xit\n")
    print_points(player1_points, player2_points)


def init_board():
    board = []
    for i in range(10):
        board.append(["~"]*10)
    return board


def single_ship_position(player_board, length):
    ship_position = [0, 0]
    ship_direction = ""
    ending_x = 0
    ending_y = 0
    init_x = 0
    init_y = 0
    allowed_directions = ["h", "H", "v", "V"]
    input_valid = False
    position_valid = False
    no_ship_overlap = True

    # Validating section - parse, position, overlap
    while not (input_valid and position_valid and no_ship_overlap):
        ship_position = input("Ship's starting position (row,col)? ").split(',')
        # Checking whether input is an integer and set ship starting coords
        input_valid = validate_input(ship_position)
        if not input_valid:
            print("Invalid input")
            continue
        init_y = int(ship_position[0])
        init_x = int(ship_position[1])
        # Checking whether starting coords are inside board
        position_valid = validate_position(init_y, init_x)
        if not position_valid:
            print("Position is not on the board")
            continue
        if length > 1:
            while ship_direction not in allowed_directions:
                ship_direction = input("Ship's direction ([h]orizontal/[v]ertical) ")
            if ship_direction in ["h", "H"]:
                ending_x = init_x + length - 1
                ending_y = init_y
            elif ship_direction in ["v", "V"]:
                ending_y = init_y + length - 1
                ending_x = init_x
            # Checking whether whole ship is inside board
            position_valid = validate_position(ending_y, ending_x)
            if not position_valid:
                print("Ship is out of board")
                ship_direction = ""
                continue
            # Checking whether new ship overlaps existing one(s)
            no_ship_overlap = check_overlap(player_board, init_y, init_x, ending_y, ending_x)
            if no_ship_overlap is False:
                print("Oops, there is another ship")
                ship_direction = ""
                continue

    # If everything is fine, writing hashmarks to player_board's relating position(s)
    for i in range(length):
        if ship_direction in ["h", "H"]:
            player_board[init_y-1][init_x-1+i] = "#"
        else:
            player_board[init_y-1+i][init_x-1] = "#"
    return player_board


def validate_input(position_to_check):
    try:
        pos_y = int(position_to_check[0])
        pos_x = int(position_to_check[1])
    except(ValueError, IndexError):
        return False
    else:
        return True


def validate_position(pos_y, pos_x):
    if pos_y <= 0 or pos_x <= 0 or pos_y > 10 or pos_x > 10:
        return False
    else:
        return True


def check_overlap(board_to_check, start_y, start_x, end_y, end_x):
    for i in range(start_y-1, end_y):
        for j in range(start_x-1, end_x):
            if board_to_check[i][j] == "#":
                return False
    return True


def draw_board(player_board, hide):
    header = textformats.BOLD + "1 2 3 4 5 6 7 8 9 10" + textformats.DEFAULT
    symbol_colours = {'~': textformats.CYAN, '#': textformats.BOLD, 'o': textformats.GREEN, 'X': textformats.RED}

    print(header.rjust(2))
    for i in range(10):
        for j in range(10):
            if player_board[i][j] == '#' and hide:
                print(textformats.CYAN + '~' + textformats.DEFAULT, end=" ")
            else:
                colour = symbol_colours[player_board[i][j]]
                print(colour + player_board[i][j] + textformats.DEFAULT, end=" ")
        print(textformats.BOLD + str(i+1).rjust(2) + textformats.DEFAULT, end=" ")
        print()


def info_board():
    os.system('clear')
    draw_board(init_board(), False)


def shot_display(player):
    os.system('clear')
    if player == 1:
        print("Enemy's board:")
        draw_board(player_two_board, True)
        print("\nYour board:")
        draw_board(player_one_board, False)
    if player == 2:
        print("Enemy's board:")
        draw_board(player_one_board, True)
        print("\nYour board:")
        draw_board(player_two_board, False)


# Shooting mechanism:
def shot(player):
    shot_display(player)
    input_valid = False
    position_valid = False
    while not (input_valid and position_valid):
        shot_position = input("\nPlayer {}: Where to shoot(row,col)? ".format(player)).split(',')
        input_valid = validate_input(shot_position)
        if not input_valid:
            print("Invalid input")
            continue
        shot_y = int(shot_position[0])
        shot_x = int(shot_position[1])
        position_valid = validate_position(shot_y, shot_x)
        if not position_valid:
            print("Target is out of range")
            continue
        else:
            if player == 1:
                if player_two_board[shot_y-1][shot_x-1] == "#":
                    player_two_board[shot_y-1][shot_x-1] = 'X'
                    shot_display(player)
                    print("Hit!")
                    time.sleep(3)
                    break
                elif player_two_board[shot_y-1][shot_x-1] == "~":
                    player_two_board[shot_y-1][shot_x-1] = 'o'
                    shot_display(player)
                    print("Miss!")
                    time.sleep(3)
                    break
                elif player_two_board[shot_y-1][shot_x-1] == "X" or player_two_board[shot_y-1][shot_x-1] == "o":
                    shot_display(player)
                    print("You've already taken a shot there!")
                    time.sleep(3)
                    break
            if player == 2:
                if player_one_board[shot_y-1][shot_x-1] == "#":
                    player_one_board[shot_y-1][shot_x-1] = 'X'
                    shot_display(player)
                    print("Hit!")
                    time.sleep(3)
                    break
                elif player_one_board[shot_y-1][shot_x-1] == "~":
                    player_one_board[shot_y-1][shot_x-1] = 'o'
                    shot_display(player)
                    print("Miss!")
                    time.sleep(3)
                    break
                elif player_one_board[shot_y-1][shot_x-1] == "X" or player_one_board[shot_y-1][shot_x-1] == "o":
                    shot_display(player)
                    print("You've already taken a shot there!")
                    time.sleep(3)
                    break


# Ship placement procedure
def place_ships(player):
    position_names = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth'}
    player_board = init_board()
    for ship_number in range(1, 6):
        print("\nPlayer {}: Place your {} ship".format(player, position_names[ship_number]))
        player_board = single_ship_position(player_board, ship_number)
        time.sleep(1)
        os.system('clear')
        draw_board(player_board, False)
    return player_board


def game_win_mech():
    global player1_points
    global player2_points
    global menu_choice
    round_finish = True
    while round_finish:
        shot(1)
        if not any("#" in a for a in player_two_board):
            print("Player 1 won the round!")
            time.sleep(3)
            player1_points += 1
            round_finish = False
            if player1_points == 5:
                os.system('clear')
                print("Player 1 won the game!")
                time.sleep(3)
                menu_choice = 'e'
                break
            continue

        shot(2)
        if not any("#" in b for b in player_one_board):
            print("Player 2 won the round!")
            time.sleep(3)
            player2_points += 1
            round_finish = False
            if player2_points == 5:
                os.system('clear')
                print("Player 2 won the game!")
                time.sleep(3)
                menu_choice = 'e'
                break
            continue
    return


def print_points(p1_point, p2_point):
    if p1_point > p2_point:
        p1_point = textformats.GREEN + str(p1_point)
    elif p1_point < p2_point:
        p2_point = textformats.GREEN + str(p2_point)
    print(textformats.UNDER + textformats.BOLD + "Score\n" + textformats.DEFAULT)
    print("Player 1: {}".format(p1_point) + textformats.DEFAULT)
    print("Player 2: {}".format(p2_point) + textformats.DEFAULT)
    time.sleep(3)


def main():
    global menu_choice
    menu_choice = ''
    global player_one_board
    global player_two_board
    player_one_board = init_board()
    player_two_board = init_board()
    game_info()
    while menu_choice != 'e':
        while menu_choice not in ('e', 'p'):
            game_menu()
            menu_choice = input('')
        if menu_choice == 'e':
            break
        elif menu_choice == 'p':
            menu_choice = ''
            # Player one positions ships
            info_board()
            player_one_board = place_ships(1)
            time.sleep(5)

            # Player 2 positions ships
            info_board()
            player_two_board = place_ships(2)
            time.sleep(5)

            # Shooting phase until someone wins
            game_win_mech()


main()