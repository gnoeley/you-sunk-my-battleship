from enum import Enum

from .actions import invite

class Keyword(Enum):
    INVITE = 'INVITE'
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'
    QUIT = 'QUIT'

actions = {
    Keyword.INVITE: invite
}


def process_content(message):
    first_word = message.split(' ')[0]
    keyword = Keyword[first_word]

    remainder = remove_first_word(message, first_word)

    return actions[keyword](remainder)

def remove_first_word(message, first_word):
    remainder = message[len(first_word):]

    return remainder