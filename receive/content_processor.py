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

    dbSession = findSession(sent_by)
    
    if first_word == Keyword.INVITE.value:
        if dbSession is None:
            return invite(remainder, sent_by, "")
        else:
            return 'invite already in a session'  # TODO: stuff and things

    if dbSession is None:
        return 'no session found' + sessions_str()

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


def findSession(player):

    print('Finding session for: ' + player + sessions_str())

    theSession = findSessionForPlayer1(player)
    if theSession is None:
        theSession = findSessionForPlayer2(player)
    return theSession

def findSessionForPlayer1(player1):
    theSession = None
    for sess in Dbsession.objects.all():
        if sess.player1 == player1:
            theSession = sess

    print(' Found ' + str(theSession or 'no session') + ' for p1: ' + player1)
    return theSession


def findSessionForPlayer2(player2):

    theSession = None
    for sess in Dbsession.objects.all():
        print('iterating over sessions to find player2: "' + player2 + '" +  session.player2="' + sess.player2 + '", p2 equal? ' + str(sess.player2 == player2))
        if sess.player2 == player2:
            theSession = sess

    print(' Found ' + str(theSession or 'no session') + ' for p2: ' + player2)
    return theSession


def sessions_str() -> str:
    s = ''
    for sess in Dbsession.objects.all():
        s = s + '\n\t\t' + str(sess)
    return ' Sessions: ' + str(len(Dbsession.objects.all())) + " ---- " + s
