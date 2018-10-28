from game.battleship_game import CellState
from unicode.symbols import letter_symbols, number_symbols, cell_symbols


def get_cell_symbol(cell_state):
    if cell_state == CellState.EMPTY:
        return cell_symbols.get('BLANK')
    elif cell_state == CellState.HIT:
        return cell_symbols.get('HIT')
    else:
        return cell_symbols.get('MISS')


def encode_row(cell_states):
    return ''.join(map(get_cell_symbol, cell_states))


column_labels = ''.join([
    '   ',
    number_symbols['0'],
    number_symbols['1'],
    number_symbols['2'],
    number_symbols['3'],
    number_symbols['4'],
    number_symbols['5'],
    number_symbols['6'],
    number_symbols['7'],
    number_symbols['8'],
    number_symbols['9']])


def encode_board(board):
    result = column_labels + '\n'
    for i, row in enumerate(board):
        result += letter_symbols[i] + encode_row(row) + '\n'
    return result
