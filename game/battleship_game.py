from enum import Enum

from game.game_entities import Players, available_ships, Ships
from game.messages import MessageMaker
from game.event_occurances import event_check
import random


class CellState(Enum):
    MISS = 'm'
    EMPTY = 'e'
    HIT = 'h'


# Orientation


VERTICAL = 0
HORIZONTAL = 1


def create_empty_board():
    return [[CellState.EMPTY.value for i in range(10)] for i in range(10)]


class Game:
    def __init__(self,
                 session_id=None,
                 current_player=Players.PLAYER_ONE,
                 player_one_board=None,
                 player_two_board=None,
                 winning_player=None,
                 hit_taken=None):
        self.session_id = session_id
        self.message_maker = MessageMaker(hit_taken)
        self.current_player = current_player
        self.player_one_board = player_one_board if player_one_board is not None else create_empty_board()
        self.player_two_board = player_two_board if player_two_board is not None else create_empty_board()
        self.winning_player = winning_player

    def place_some_ships(self):
        for player_board in [self.player_one_board, self.player_two_board]:
            while not place_ship(player_board, available_ships[Ships.CARRIER], random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, available_ships[Ships.BATTLESHIP], random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, available_ships[Ships.CRUISER], random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, available_ships[Ships.SUBMARINE], random_orientation(), random_board_position()):
                pass
            while not place_ship(player_board, available_ships[Ships.DESTROYER], random_orientation(), random_board_position()):
                pass

    def build_game_won_message(self):
        return {
            self.winning_player: 'You have already won! Send another INVITE to start a new game',
            Players.other_player(self.winning_player): 'You have already lost! Send another INVITE to restore your honour',
            'GAME_OVER': False,
            'PLAYER_1_BOARD': self.typed_player_board(self.player_one_board),
            'PLAYER_2_BOARD': self.typed_player_board(self.player_two_board),
        }

    def get_player_instructions(self):
        if self.winning_player is not None:
            return self.build_game_won_message()
        else:
            return {
                self.current_player: 'You\'re in a game it\'s your turn. Text \'FIRE\' followed by your coordinates to attack.',
                Players.other_player(self.current_player): 'You\'re in a game it\'s another players turn. Text \'FIRE\' followed by your coordinates to attack once the other player has been.',
                'GAME_OVER': False,
                'PLAYER_1_BOARD': self.typed_player_board(self.player_one_board),
                'PLAYER_2_BOARD': self.typed_player_board(self.player_two_board),
            }

    def player_turn(self, player: Players, position):
        if player != self.current_player:
            return {
                player: 'It is not your turn, patience!',
                self.current_player: 'The other player is getting restless, please hurry up',
                'GAME_OVER': False,
                'PLAYER_1_BOARD': self.typed_player_board(self.player_one_board),
                'PLAYER_2_BOARD': self.typed_player_board(self.player_two_board),
            }

        if self.winning_player is not None:
            return self.build_game_won_message()

        board = self.player_two_board if player is Players.PLAYER_ONE else self.player_one_board
        type_of_ship_hit: Ships = take_fire(board, position)
        if check_is_winning_board(board):
            self.winning_player = self.current_player
        elif self.winning_player == 'Draw':
            print('Everyone loses!')

        message = self.make_message(type_of_ship_hit)
        self.current_player = Players.other_player(self.current_player)

        print('PLAYER_ONE:')
        print(pretty_print_board(self.player_one_board))
        print()
        print('PLAYER_TWO:')
        print(pretty_print_board(self.player_two_board))

        return message

    def make_message(self, type_of_ship_hit):
        player_message = event_check()

        if game.winning_player == 'Draw':
            return {
                Players.PLAYER_ONE: player_message,
                Players.PLAYER_TWO: player_message,
                'GAME_OVER': 'Draw'
            }
        else:
            return {
                Players.PLAYER_ONE: self.message_maker.make_message(Players.PLAYER_ONE,
                                                                    self.current_player,
                                                                    self.winning_player,
                                                                    type_of_ship_hit),
                Players.PLAYER_TWO: self.message_maker.make_message(Players.PLAYER_TWO,
                                                                    self.current_player,
                                                                    self.winning_player,
                                                                    type_of_ship_hit),
                'GAME_OVER': self.winning_player is not None,
                'PLAYER_1_BOARD': self.typed_player_board(self.player_one_board),
                'PLAYER_2_BOARD': self.typed_player_board(self.player_two_board),
            }

    def position_to_cell_state(self, position):
        if position == CellState.EMPTY.value:
            return CellState.EMPTY
        if position == CellState.HIT.value:
            return CellState.HIT
        if position == CellState.MISS.value:
            return CellState.MISS

    def typed_player_board(self, board):
        rows = []
        for row in board:
            cells = []
            for position in row:
                cells.append(self.position_to_cell_state(position))
            rows.append(cells)
        return rows


def random_orientation():
    return random.randint(0, 1)


def random_board_position():
    return [random.randint(0, 9), random.randint(0, 9)]


def place_ship(board, ship, orientation, position):
    if not is_valid_placement(board, ship, orientation, position):
        return False

    initial_x, initial_y = position

    for i in range(ship.size):
        x = initial_x + i if orientation is HORIZONTAL else initial_x
        y = initial_y + i if orientation is VERTICAL else initial_y
        board[y][x] = ship.character

    return True


def is_valid_placement(board, ship, orientation, position):
    def is_out_of_bounds(value):
        return not -1 < value < 10

    initial_x, initial_y = position
    max_x = initial_x + ship.size - 1 if orientation is HORIZONTAL else initial_x
    max_y = initial_y + ship.size - 1 if orientation is VERTICAL else initial_y

    if is_out_of_bounds(initial_x) or is_out_of_bounds(initial_y) or is_out_of_bounds(max_x) or is_out_of_bounds(max_y):
        return False

    for i in range(ship.size):
        x = initial_x + i if orientation is HORIZONTAL else initial_x
        y = initial_y + i if orientation is VERTICAL else initial_y
        if is_ship_position(board[y][x]):
            return False

    return True


def is_ship_position(position):
    for type_of_ship, ship in available_ships.items():
        if position == ship.character:
            return type_of_ship
    return None


def take_fire(board, position):
    x, y = position

    type_of_ship_hit = is_ship_position(board[y][x])
    if type_of_ship_hit:
        board[y][x] = CellState.HIT.value
    elif board[y][x] is CellState.EMPTY.value:
        board[y][x] = CellState.MISS.value

    return type_of_ship_hit


def check_is_winning_board(board):
    if game.winning_player == 'Draw':
        return True

    for row in board:
        for position in row:
            if is_ship_position(position):
                return False
    return True


def pretty_print_board(board):
    result = ''
    for row in board:
        for position in row:
            result += ('s' if is_ship_position(position) else position) + ' '
        result += '\n'
    return result


def find_current_board():
    if game.current_player == Players.PLAYER_ONE:
        return game.player_one_board
    else:
        return game.player_two_board


def sink_random_ship():
    randomIdx = random.randint(0, 4)
    keys = [key for key in available_ships.keys()]
    randomKey = keys[randomIdx]

    target = available_ships[randomKey]
    print(randomKey)
    board = find_current_board()
    for row in board:
        for [x, y] in row:
            if board[x][y] == randomKey:
                board[x][y] = 'h'


if __name__ == "__main__":
    game = Game()
    game.place_some_ships()
    print(pretty_print_board(game.player_one_board))
    print(pretty_print_board(game.player_two_board))

    sink_random_ship()

    game_state = game.player_turn(Players.PLAYER_ONE, [5, 3])
    print('Player ONE: ', game_state[Players.PLAYER_ONE])
    print('Player TWO: ', game_state[Players.PLAYER_TWO])
    print("Game Over?", game_state['GAME_OVER'])

    game_state = game.player_turn(Players.PLAYER_TWO, [6, 3])
    print('Player ONE: ', game_state[Players.PLAYER_ONE])
    print('Player TWO: ', game_state[Players.PLAYER_TWO])
    print("Game Over?", game_state['GAME_OVER'])

    game_state = game.player_turn(Players.PLAYER_ONE, [9, 9])
    print('Player ONE: ', game_state[Players.PLAYER_ONE])
    print('Player TWO: ', game_state[Players.PLAYER_TWO])
    print("Game Over?", game_state['GAME_OVER'])

