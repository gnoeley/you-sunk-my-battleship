from enum import Enum, auto

from hello.models import Dbsession
from hello.sms.smsSender import sendMessage
from receive.keywords import Keyword


class SessionState(Enum):
    STARTING = auto()
    IN_GAME = auto()
    ENDED = auto()


class PlayerState(Enum):
    STARTING = auto()
    NOT_JOINED = auto()
    INVITED = auto()
    REJECTED = auto()
    IN_GAME = auto()
    QUIT = auto()


class Session:

    def __init__(self, player_1_num='a', player_2_num='b', dbSession: Dbsession = None) -> object:
        if dbSession is None:
            self.player_1_num = player_1_num
            self.player_2_num = player_2_num
            self.session_state = SessionState.STARTING
            self.player_1_state = PlayerState.STARTING
            self.player_2_state = PlayerState.NOT_JOINED
        else:
            self.player_1_num = dbSession.player1
            self.player_2_num = dbSession.player2
            self.session_state = SessionState[dbSession.session_state]
            self.player_1_state = PlayerState[dbSession.player_1_state]
            self.player_2_state = PlayerState[dbSession.player_2_state]
            self.save()

    def save(self):
        print("SAVING")
        dbSession = Dbsession()
        dbSession.player1=self.player_1_num
        dbSession.player2=self.player_2_num
        dbSession.session_state=self.session_state.name
        dbSession.player_1_state=self.player_1_state.name
        dbSession.player_2_state=self.player_2_state.name

        dbSession.save()
        print("Saved dbSession")
        print("new sessions: " + str(len(Dbsession.objects.all())) + " ---- " + str(Dbsession.objects.all()))

    def restart(self, player_restarting):

        if player_restarting == self.player_2_num:
            self.player_2_num = self.player_1_num
            self.player_1_num = player_restarting

        self.session_state = SessionState.STARTING
        self.player_1_state = PlayerState.STARTING
        self.player_2_state = PlayerState.STARTING
        self.invite_player_2()

    def invite_player_2(self):
        print("INVITING " + str(self.player_2_num))

        self.session_state = SessionState.STARTING
        self.player_1_state = PlayerState.STARTING

        p1Message = self.player_2_num + ' has been invited'
        p2Message = self.player_1_num + ' has invited you to a game of Battleships - text ' + Keyword.ACCEPT.value + ' to join the game or ' + Keyword.QUIT.value + ' to refuse'

        sendMessage(to=self.player_1_num, text=p1Message)
        sendMessage(to=self.player_2_num, text=p2Message)

        self.player_2_state = PlayerState.INVITED

        self.save()
        return {'p1': p1Message, 'p2': p2Message}


    def player_2_accepted_invite(self):

        p1Message = self.player_2_num + ' has accepted your invite.' + ' reply ' + Keyword.QUIT.value + ' to quit'
        p2Message = 'You are now in a game with: ' + self.player_1_num + ' reply ' + Keyword.QUIT.value + ' to quit'

        sendMessage(to=self.player_1_num, text=p1Message)
        sendMessage(to=self.player_2_num, text=p2Message)

        self.player_1_state = PlayerState.IN_GAME
        self.player_2_state = PlayerState.IN_GAME
        self.session_state = SessionState.IN_GAME

        self.save()
        return {'p1': p1Message, 'p2': p2Message}

    def player_2_rejected_invite(self):
        p1Message = self.player_2_num + ' has rejected your invite.' + ' reply ' + Keyword.INVITE.value + ' with a number to invite someone else'
        p2Message = 'Why so serious?'

        sendMessage(to=self.player_1_num, text=p1Message)
        sendMessage(to=self.player_2_num, text=p2Message)

        self.player_2_state = PlayerState.REJECTED
        self.session_state = SessionState.ENDED

        self.save()
        return {'p1': p1Message, 'p2': p2Message}

    def player_1_quit(self):
        p1Message = 'Bye'
        p2Message = 'Player 1 left'

        sendMessage(to=self.player_1_num, text=p1Message)
        sendMessage(to=self.player_2_num, text=p2Message)

        self.player_1_state = PlayerState.QUIT
        self.session_state = SessionState.ENDED

        self.save()
        return {'p1': p1Message, 'p2': p2Message}

    def player_2_quit(self):
        p1Message = 'Player 2 left'
        p2Message = 'Bye'

        sendMessage(to=self.player_1_num, text=p1Message)
        sendMessage(to=self.player_2_num, text=p2Message)

        self.player_2_state = PlayerState.QUIT
        self.session_state = SessionState.ENDED

        self.save()
        return {'p1': p1Message, 'p2': p2Message}

    def __str__(self) -> str:
        return \
            "Session: {" + \
            "session state:" + self.session_state.name + \
            ", player 1 number:" + self.player_1_num + \
            ", player 2 number:" + self.player_2_num + \
            ", player 1 state:" + self.player_1_state.name + \
            ", player 2 state:" + self.player_2_state.name + \
            "}"

    def process_game_action(self, sent_by, first_word, remainder):
        #  TODO: implement this
        return 'processing game action ' + first_word + ' from ' + sent_by + ' [' + remainder + ']'

    @staticmethod
    def findSession(p):

        print('Finding session for: ' + p + Session.sessions_str())

        theSession = Session.findSessionForPlayer1(p)
        if theSession is None:
            theSession = Session.findSessionForPlayer2(p)
        return theSession

    @staticmethod
    def findSessionForPlayer1(p):
        theSession = None
        for sess in Dbsession.objects.all():
            if sess.player1 == p:
                theSession = sess

        print(' Found ' + str(theSession or 'no session') + ' for p1: ' + p)
        return theSession

    @staticmethod
    def findSessionForPlayer2(p):

        theSession = None
        for sess in Dbsession.objects.all():
            print('iterating over sessions to find player2: "' + p + '" +  session.player2="' + sess.player2 + '", p2 equal? ' + str(sess.player2 == p))
            if sess.player2 == p:
                theSession = sess

        print(' Found ' + str(theSession or 'no session') + ' for p2: ' + p)
        return theSession

    @staticmethod
    def sessions_str() -> str:
        s = ''
        for sess in Dbsession.objects.all():
            s = s + '\n\t\t' + str(sess)
        return ' Sessions: ' + str(len(Dbsession.objects.all())) + " ---- " + s
