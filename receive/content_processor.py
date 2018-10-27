from hello.models import Dbsession
from sessions.gamesession import Session
from .actions import invite, accept, reject, quit
from sessions import gamesession
from .keywords import Keyword


actions = {
    Keyword.ACCEPT: accept,
    Keyword.REJECT: reject,
    Keyword.QUIT: quit
}


def process_content(message, sent_by):
    first_word = message.split(' ')[0]
    remainder = remove_first_word(message, first_word)

    dbSession = Session.findSession(sent_by)
    
    if first_word == Keyword.INVITE.value:
        if dbSession is None:
            return invite(remainder, sent_by)
        else:
            session = gamesession.Session(dbSession=dbSession)
            if session.session_state == gamesession.SessionState.ENDED:
                return session.restart(player_restarting=sent_by)
            else:
                return 'invite already in a session'  # TODO: stuff and things

    if dbSession is None:
        return 'no session found' + Session.sessions_str()

    session = gamesession.Session(dbSession=dbSession)

    if Keyword.has_value(first_word):

        keyword = Keyword[first_word]

        action_method = actions.get(keyword)

        return action_method(remainder, session, sent_by)

    else:
        session.process_game_action(sent_by, first_word, remainder)


def remove_first_word(message, first_word):
    remainder = message[len(first_word) + 1:]

    return remainder
