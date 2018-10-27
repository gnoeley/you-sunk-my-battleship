# Ships
CARRIER = 5
BATTLESHIP = 4
CRUISER = 3
SUBMARINE = 3
DESTROYER = 2

# Orientation
VERTICAL = 0
HORIZONTAL = 1


def create_empty_board():
    return [['e' for i in range(10)] for i in range(10)]


def pretty_print_board(board):
    for row in board:
        for position in row:
            print(position, end=" ")
        print()


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


if __name__ == "__main__":
    game_board = create_empty_board()
    place_ship(game_board, CARRIER, VERTICAL, [0, 0])
    place_ship(game_board, DESTROYER, HORIZONTAL, [5, 3])
    pretty_print_board(game_board)
    take_fire(game_board, [0, 1])
    take_fire(game_board, [9, 9])
    print()
    pretty_print_board(game_board)
