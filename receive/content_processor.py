from enum import Enum

from .actions import invite, accept
from sessions import sessions

class Keyword(Enum):
    INVITE = 'INVITE'
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'
    QUIT = 'QUIT'

actions = {
    Keyword.ACCEPT: accept
}


def process_content(message, sent_by, to_num):
    first_word = message.split(' ')[0]
    keyword = Keyword[first_word]

    remainder = remove_first_word(message, first_word)

    session = sessions.Sessions.get_session(sent_by)

    if session is None:
        return invite(remainder, sent_by, to_num)

    return actions[keyword](remainder, session)

def remove_first_word(message, first_word):
    remainder = message[len(first_word):]

    return remainder