# Ships
CARRIER = 5
BATTLESHIP = 4
CRUISER = 3
SUBMARINE = 3
DESTROYER = 2

# Orientation
VERTICAL = 0
HORIZONTAL = 1

def createEmptyBoard():
    return [['e' for i in range(10)] for i in range(10)]

def prettyPrintBoard(board):
    for row in board:
        for position in row:
            print(position, end=" ")
        print()

def placeShip(board, ship, orientaion, position):
    initial_x = position[0]
    initial_y = position[1]

    for i in range(ship):
        x = initial_x + i if orientaion is HORIZONTAL else initial_x
        y = initial_y + i if orientaion is VERTICAL else initial_y
        board[y][x] = 's'

def takeFire(board, position):
    x = position[0]
    y = position[1]

    if board[y][x] is 's':
        board[y][x] = 'h'
    elif board[y][x] is 'e':
        board[y][x] = 'm'

if __name__ == "__main__":
    board = createEmptyBoard()
    placeShip(board, CARRIER, VERTICAL, [0, 0])
    placeShip(board, DESTROYER, HORIZONTAL, [5, 3])
    prettyPrintBoard(board)
    takeFire(board, [0, 1])
    takeFire(board, [9, 9])
    print()
    prettyPrintBoard(board)
