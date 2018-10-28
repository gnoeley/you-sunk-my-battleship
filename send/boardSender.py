
import requests
import os
from unicode.symbols import letter_symbols, number_symbols, cell_symbols


def get_cell_symbol(isHit):
    if isHit is None:
        return cell_symbols.get('BLANK')
    elif isHit:
        return cell_symbols.get('HIT')
    else:
        return cell_symbols.get('MISS')


def encode_row(hits):
    return ''.join(map(get_cell_symbol, hits))


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


unicodeBoard = \
    column_labels + ' \n' + \
    letter_symbols.get('A') + encode_row([None, None, None, None,None,None,None,None,None, None]) + '\n' + \
    letter_symbols.get('B') + encode_row([True, True, True, True,True,True,True,True,True, True]) + '\n' + \
    letter_symbols.get('C') + encode_row([False, False, False, False,False,False,False,False,False, False]) + '\n' + \
    letter_symbols.get('D') + '◽◽◽◽◽◽◽◽\n' + \
    letter_symbols.get('E') + '◽◽◽◽◽◽◽◽\n' + \
    letter_symbols.get('F') + '◽◽◽◽◽◽◽◽\n' + \
    letter_symbols.get('G') + '◽◽◽◽◽◽◽◽\n' + \
    letter_symbols.get('H') + '◽◽◽◽◽◽◽◽\n' + \
    letter_symbols.get('I') + '◽◽◽◽◽◽◽◽\n' + \
    letter_symbols.get('J') + '◽◽◽◽◽◽◽◽\n'

def build_board_xml(aBoard):
    board = unicodeBoard
    return '<?xml version="1.0" encoding="UTF-8"?>' + \
           '<Message>' + \
           '<Key>' + os.environ.get('CLOCKWORK_API_KEY') + '</Key>' + \
           '<SMS>' + \
           '<To>447528830422</To><MsgType>UCS2</MsgType>' + \
           '<Content>' + board + '</Content>' + \
           '</SMS>' + \
           '</Message>'


def send_board_xml(board):
    xml = build_board_xml(board)
    headers = {'Content-Type': 'text/xml'} # set what your server accepts
    print(requests.post('https://api.clockworksms.com/xml/send.aspx', data=xml.encode('utf-8'), headers=headers).text)
    return xml
