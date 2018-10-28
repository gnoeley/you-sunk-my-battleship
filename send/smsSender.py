from clockwork import clockwork
import os

import requests

from send.boardSender import encode_board

api = clockwork.API(os.environ.get('CLOCKWORK_API_KEY'))


def send_message(to, text):
    if os.environ.get('SEND_SMS') != 'True':
        print('Would have sent "' + text + '" to ' + to)
    else:
        from_name = os.environ.get('FROM_SMS')
        print('Sending "' + text + '" to ' + to + " from " + from_name)
        message = clockwork.SMS(to=to, message=text, from_name=from_name)

        response = api.send(message)

        if response.success:
            print(response.id)
        else:
            print(response.error_code)
            print(response.error_message)


def send_message_with_board(to, text, board):
    xml = build_xml(text, to)
    headers = {'Content-Type': 'text/xml'} # set what your server accepts
    print(requests.post('https://api.clockworksms.com/xml/send.aspx', data=xml.encode('utf-8'), headers=headers).text)

    encoded_board = encode_board(board)
    xml = build_xml(encoded_board, to)
    print(len(encoded_board))
    headers = {'Content-Type': 'text/xml'} # set what your server accepts
    print(requests.post('https://api.clockworksms.com/xml/send.aspx', data=xml.encode('utf-8'), headers=headers).text)
    return xml


def build_xml(content, phone_number='447528830422'):
    return '<?xml version="1.0" encoding="UTF-8"?>' + \
           '<Message>' + \
           '<Key>' + os.environ.get('CLOCKWORK_API_KEY') + '</Key>' + \
           '<SMS>' + \
           '<To>' + phone_number + '</To><MsgType>UCS2</MsgType>' + \
           '<Content>' + content + '</Content>' + \
           '<Concat>3</Concat>' + \
           '</SMS>' + \
           '</Message>'
