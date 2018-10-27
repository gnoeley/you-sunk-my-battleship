from .actions import invite, accept, reject, quit
from sessions import sessions
from .keywords import Keyword




actions = {
    Keyword.ACCEPT: accept,
    Keyword.REJECT: reject,
    Keyword.QUIT: quit
}


def process_content(message, sent_by, to_num):
    first_word = message.split(' ')[0]
    keyword = Keyword[first_word]

    remainder = remove_first_word(message, first_word)

    session = sessions.Sessions.get_session(sent_by)

    if session is None:
        return invite(remainder, sent_by, to_num)

    return actions[keyword](remainder, session, sent_by)


def remove_first_word(message, first_word):
    remainder = message[len(first_word):]

    return remainder
