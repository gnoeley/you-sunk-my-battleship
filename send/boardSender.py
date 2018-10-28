
import requests
import os
from unicode.symbols import letter_symbols

column_labels = u'\u00a0'.join([
    letter_symbols.get('A'),
    letter_symbols.get('B'),
    letter_symbols.get('C'),
    letter_symbols.get('D'),
    letter_symbols.get('E'),
    letter_symbols.get('F'),
    letter_symbols.get('G'),
    letter_symbols.get('H'),
    letter_symbols.get('I'),
    letter_symbols.get('J')])

unicodeBoard = \
    column_labels + ' \n' + \
    '1◽◽◽◽◽◽◽◽\n' + \
    '2◽◽◽◽◽◽◽◽\n' + \
    '3◽◽◽◽◽◽◽◽\n' + \
    '4◽◽◽◽◽◽◽◽\n' + \
    '5◽◽◽◽◽◽◽◽\n'


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
