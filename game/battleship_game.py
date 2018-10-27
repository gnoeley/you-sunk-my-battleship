from enum import Enum

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
        place_ship(self.player_one_board, CARRIER, VERTICAL, [0, 0])
        place_ship(self.player_two_board, DESTROYER, HORIZONTAL, [5, 3])

    def player_turn(self, player, position):
        if self.winning_player is not None:
            return self.make_player_won_message()

        board = self.player_one_board if player is Players.PLAYER_ONE else self.player_two_board
        take_fire(board, position)
        if check_is_winning_board(board):
            self.winning_player = self.current_player

        self.current_player = Players.PLAYER_TWO if self.current_player is Players.PLAYER_ONE else Players.PLAYER_ONE

        return {
            Players.PLAYER_ONE: pretty_print_board(self.player_one_board),
            Players.PLAYER_TWO: pretty_print_board(self.player_two_board)
        }

    def make_player_won_message(self):
        return {
            Players.PLAYER_ONE: 'You won!' if self.winning_player is Players.PLAYER_ONE else 'You lose!',
            Players.PLAYER_TWO: 'You won!' if self.winning_player is Players.PLAYER_TWO else 'You lose!'
        }


def create_empty_board():
    return [['e' for i in range(10)] for i in range(10)]


def pretty_print_board(board):
    result = ''
    for row in board:
        for position in row:
            result += position + ' '
        result += '\n'
    return result


def place_ship(board, ship, orientation, position):
    initial_x, initial_y = position

    for i in range(ship):
        x = initial_x + i if orientation is HORIZONTAL else initial_x
        y = initial_y + i if orientation is VERTICAL else initial_y
        board[y][x] = 's'


def take_fire(board, position):
    x, y = position

    if board[y][x] is 's':
        board[y][x] = 'h'
    elif board[y][x] is 'e':
        board[y][x] = 'm'


def check_is_winning_board(board):
    for row in board:
        for position in row:
            if position is 's': return False
    return True


if __name__ == "__main__":
    game = Game()
    game.place_some_ships()

    game.player_turn(Players.PLAYER_TWO, [5, 3])
    game.player_turn(Players.PLAYER_TWO, [6, 3])
    final_state = game.player_turn(Players.PLAYER_TWO, [9, 9])

    game.player_turn(Players.PLAYER_ONE, [0, 1])
    game.player_turn(Players.PLAYER_ONE, [0, 0])
    game.player_turn(Players.PLAYER_ONE, [0, 2])
    game.player_turn(Players.PLAYER_ONE, [0, 3])
    game.player_turn(Players.PLAYER_ONE, [0, 4])

    print('Player ONE: ', final_state[Players.PLAYER_ONE])
    print()
    print('Player TWO: ', final_state[Players.PLAYER_TWO])
