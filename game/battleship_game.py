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
    x = position[0]
    y = position[1]

    if orientaion is VERTICAL:
        for i in range(ship):
            board[y+i][x] = 's'
    else:
        for i in range(ship):
            board[y][x+i] = 's'
