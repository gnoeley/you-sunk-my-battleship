from hello.models import Dbsession
from .actions import invite, accept, reject, quit
from sessions import sessions, gamesession
from .keywords import Keyword


actions = {
    Keyword.ACCEPT: accept,
    Keyword.REJECT: reject,
    Keyword.QUIT: quit
}


def process_content(message, sent_by):
    first_word = message.split(' ')[0]
    remainder = remove_first_word(message, first_word)

    dbSession = findSession(sent_by, sent_by)
    
    if first_word == Keyword.INVITE.value:
        if dbSession is None:
            return invite(remainder, sent_by, "")
        else:
            return 'invite already in a session'  # TODO: stuff and things

    if dbSession is None:
        return 'no session found' +  str(len(Dbsession.objects.all())) + " ---- " + str(Dbsession.objects.all())

    session = gamesession.Session(dbSession=dbSession)

    if Keyword.has_value(first_word):

        keyword = Keyword[first_word]

        action_method = actions.get(keyword)

        return action_method(remainder, session, sent_by)

    else:
        session.process_game_action(sent_by, first_word, remainder)


def remove_first_word(message, first_word):
    remainder = message[len(first_word):]

    return remainder


def findSession(player1, player2):
    theSession = findSessionForPlayer1(player1)
    if theSession is None:
        theSession = findSessionForPlayer2(player2)
    return theSession

def findSessionForPlayer1(player1):
    try:
        return Dbsession.objects.get(player1=player1)
    except Dbsession.DoesNotExist:
        return None

def findSessionForPlayer2(player2):
    try:
        return Dbsession.objects.get(player2=player2)
    except Dbsession.DoesNotExist:
        return None