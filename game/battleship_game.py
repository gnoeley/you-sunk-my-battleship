def createEmptyBoard():
    return [['e' for i in range(10)] for i in range(10)]

def prettyPrintBoard(board):
    for row in board:
        for position in row:
            print(position, end=" ")
        print()