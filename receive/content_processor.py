from .actions import invite, accept, reject, quit
from sessions import sessions, gamesession
from .keywords import Keyword


actions = {
    Keyword.ACCEPT: accept,
    Keyword.REJECT: reject,
    Keyword.QUIT: quit
}


def process_content(message, sent_by, to_num):
    first_word = message.split(' ')[0]
    remainder = remove_first_word(message, first_word)

    session: gamesession.Session = sessions.Sessions.get_session(sent_by)

    if first_word == Keyword.INVITE.value:
        if session is None:
            return invite(remainder, sent_by, to_num)
        else:
            return 'invite already in a session'  # TODO: stuff and things

    if session is None:
        return 'no session found' + sessions.Sessions.sessionsDict.str()  # TODO: stuff and things

    if Keyword.has_value(first_word):

        keyword = Keyword[first_word]

        action_method = actions.get(keyword)

        return action_method(remainder, session, sent_by)

    else:
        session.process_game_action(sent_by, first_word, remainder)


def remove_first_word(message, first_word):
    remainder = message[len(first_word):]

    return remainder
