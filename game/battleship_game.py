from game import messages
from enum import Enum
import random

# Ships
CARRIER = 5
BATTLESHIP = 4
CRUISER = 3
SUBMARINE = 3
DESTROYER = 2

# Orientation
VERTICAL = 0
HORIZONTAL = 1


class Players(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2


class Game:

    def __init__(self):
        self.current_player = Players.PLAYER_ONE
        self.player_one_board = create_empty_board()
        self.player_two_board = create_empty_board()
        self.winning_player = None

    def place_some_ships(self):
        for player_board in [self.player_one_board, self.player_two_board]:
            while not place_ship(player_board, CARRIER, random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, BATTLESHIP, random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, CRUISER, random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, SUBMARINE, random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, DESTROYER, random_orientation(), random_board_position()):
                pass

    def player_turn(self, player, position):
        if self.winning_player is not None:
            return self.make_message()

        board = self.player_one_board if player is Players.PLAYER_ONE else self.player_two_board
        take_fire(board, position)
        if check_is_winning_board(board):
            self.winning_player = self.current_player

        message = self.make_message()
        self.current_player = Players.PLAYER_TWO if self.current_player is Players.PLAYER_ONE else Players.PLAYER_ONE

        return message

    def make_message(self):
        return {
            Players.PLAYER_ONE: messages.make_message(Players.PLAYER_ONE, self.current_player, self.winning_player, True),
            Players.PLAYER_TWO: messages.make_message(Players.PLAYER_TWO, self.current_player, self.winning_player, True),
            'GAME_OVER': self.winning_player is not None
        }


def create_empty_board():
    return [['e' for i in range(10)] for i in range(10)]


def random_orientation():
    return random.randint(0, 1)


def random_board_position():
    return [random.randint(0, 9), random.randint(0, 9)]


def place_ship(board, ship, orientation, position):
    if not is_valid_placement(board, ship, orientation, position):
        return False

    initial_x, initial_y = position

    for i in range(ship):
        x = initial_x + i if orientation is HORIZONTAL else initial_x
        y = initial_y + i if orientation is VERTICAL else initial_y
        board[y][x] = 's'

    return True


def is_valid_placement(board, ship, orientation, position):
    def is_out_of_bounds(value):
        return not -1 < value < 10

    initial_x, initial_y = position
    max_x = initial_x + ship - 1 if orientation is HORIZONTAL else initial_x
    max_y = initial_y + ship - 1 if orientation is VERTICAL else initial_y

    if is_out_of_bounds(initial_x) or is_out_of_bounds(initial_y) or is_out_of_bounds(max_x) or is_out_of_bounds(max_y):
        return False

    for i in range(ship):
        x = initial_x + i if orientation is HORIZONTAL else initial_x
        y = initial_y + i if orientation is VERTICAL else initial_y
        if board[y][x] is 's':
            return False

    return True


def take_fire(board, position):
    x, y = position

    if board[y][x] is 's':
        board[y][x] = 'h'
    elif board[y][x] is 'e':
        board[y][x] = 'm'


def check_is_winning_board(board):
    for row in board:
        for position in row:
            if position is 's':
                return False
    return True


def pretty_print_board(board):
    result = ''
    for row in board:
        for position in row:
            result += position + ' '
        result += '\n'
    return result


if __name__ == "__main__":
    game = Game()
    game.place_some_ships()
    print(pretty_print_board(game.player_one_board))
    print(pretty_print_board(game.player_two_board))

    game.player_turn(Players.PLAYER_TWO, [5, 3])
    game.player_turn(Players.PLAYER_TWO, [6, 3])
    final_state = game.player_turn(Players.PLAYER_TWO, [9, 9])

    print('Player ONE: ', final_state[Players.PLAYER_ONE])
    print('Player TWO: ', final_state[Players.PLAYER_TWO])
    print("Game Over?", final_state['GAME_OVER'])
