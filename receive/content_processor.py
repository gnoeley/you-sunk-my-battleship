from state.session import Session, SessionState
from .actions import invite, accept, reject, quit
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
        return process_invite(dbSession, remainder, sent_by)

    if dbSession is None:
        return 'no session found' + Session.sessions_str()  # TODO: need an SMS

    session = Session(dbSession=dbSession)

    if Keyword.has_value(first_word):

        keyword = Keyword[first_word]

        action_method = actions.get(keyword)

        return action_method(remainder, session, sent_by)

    else:
        session.process_game_action(sent_by, first_word, remainder)


def process_invite(dbSession, remainder, sent_by):
    other_player_num = remainder
    if dbSession is None:
        if is_player_in_other_active_session(player_phone_num=other_player_num):
            return other_player_num + 'is already in a game session -> still have no SMS message sent for this'  # TODO: send SMSs
        return invite(remainder, sent_by)
    else:
        session = Session(dbSession=dbSession)
        if session.session_state == SessionState.ENDED:
            return maybe_restart_session(dbSession, other_player_num, sent_by, session)
        else:
            return 'current game session is still active, cannot INVITE again -> still have no SMS message sent for this'  # TODO: send SMSs


def is_player_in_other_active_session(player_phone_num, db_session_to_ignore=None):
    other_db_session = Session.findSession(player_phone_num)
    if other_db_session is None:
        return False

    if (db_session_to_ignore is None) or (other_db_session.id != db_session_to_ignore.id):
        if other_db_session.session_state == SessionState.ENDED.name:
            other_db_session.delete()
        else:
            return True
    return False


def maybe_restart_session(dbSession, other_player_number, sent_by, session):
    if is_player_in_other_active_session(player_phone_num=other_player_number, db_session_to_ignore=dbSession):
        return 'other player in a game -> still have no SMS message sent for this'  # TODO: send SMSs
    else:
        return session.restart(player_restarting=sent_by, other_player=other_player_number)


def remove_first_word(message, first_word):
    remainder = message[len(first_word) + 1:]

    return remainder
