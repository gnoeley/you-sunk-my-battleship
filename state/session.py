from enum import Enum, auto

from game.battleship_game import Game, Players
from hello.models import Dbsession, GameModel
from send.smsSender import send_message, send_message_with_board
from receive.keywords import Keyword
from game.game_actions import process_action

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

    def __init__(self, player_1_num='a', player_2_num='b', dbSession: Dbsession = None):
        if dbSession is None:
            self.id = None
            self.game_id = None
            self.player_1_num = player_1_num
            self.player_2_num = player_2_num
            self.session_state = SessionState.STARTING
            self.player_1_state = PlayerState.STARTING
            self.player_2_state = PlayerState.NOT_JOINED
        else:
            self.id = dbSession.id
            self.game_id = dbSession.game_id
            self.player_1_num = dbSession.player1
            self.player_2_num = dbSession.player2
            self.session_state = SessionState[dbSession.session_state]
            self.player_1_state = PlayerState[dbSession.player_1_state]
            self.player_2_state = PlayerState[dbSession.player_2_state]
            self.save()

    def save(self):
        print("SAVING")

        dbSession = None
        theId = self.id

        if theId is None:
            dbSession = Dbsession()
        else:
            dbSession = Dbsession.objects.get(id=theId)

        dbSession.game_id=self.game_id
        dbSession.player1=self.player_1_num
        dbSession.player2=self.player_2_num
        dbSession.session_state=self.session_state.name
        dbSession.player_1_state=self.player_1_state.name
        dbSession.player_2_state=self.player_2_state.name

        dbSession.save()


        self.id = dbSession.id  # Not sure if this works ... shrugs

        print("Saved dbSession")
        print("new sessions: " + str(len(Dbsession.objects.all())) + " ---- " + str(Dbsession.objects.all()))

    def restart(self, player_restarting, other_player):



        if player_restarting == self.player_2_num:
            self.player_1_num = player_restarting
            self.player_2_num = other_player
        else:
            self.player_1_num = other_player
            self.player_2_num = player_restarting

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

        send_message(to=self.player_1_num, text=p1Message)
        send_message(to=self.player_2_num, text=p2Message)

        self.player_2_state = PlayerState.INVITED

        self.save()
        return {'p1': p1Message, 'p2': p2Message}


    def player_2_accepted_invite(self):

        p1Message = self.player_2_num + ' has accepted your invite.' + ' reply ' + Keyword.QUIT.value + ' to quit'
        p2Message = 'You are now in a game with: ' + self.player_1_num + ' reply ' + Keyword.QUIT.value + ' to quit'

        send_message(to=self.player_1_num, text=p1Message)
        send_message(to=self.player_2_num, text=p2Message)

        self.player_1_state = PlayerState.IN_GAME
        self.player_2_state = PlayerState.IN_GAME
        self.session_state = SessionState.IN_GAME

        self.save()
        return {'p1': p1Message, 'p2': p2Message}

    def player_2_rejected_invite(self):
        p1Message = self.player_2_num + ' has rejected your invite.' + ' reply ' + Keyword.INVITE.value + ' with a number to invite someone else'
        p2Message = 'Why so serious?'

        send_message(to=self.player_1_num, text=p1Message)
        send_message(to=self.player_2_num, text=p2Message)

        self.player_2_state = PlayerState.REJECTED
        self.session_state = SessionState.ENDED

        self.save()
        return {'p1': p1Message, 'p2': p2Message}

    def player_1_quit(self):
        p1Message = 'Bye'
        p2Message = 'Player 1 left'

        send_message(to=self.player_1_num, text=p1Message)
        send_message(to=self.player_2_num, text=p2Message)

        self.player_1_state = PlayerState.QUIT
        self.session_state = SessionState.ENDED

        self.save()
        return {'p1': p1Message, 'p2': p2Message}

    def player_2_quit(self):
        p1Message = 'Player 2 left'
        p2Message = 'Bye'

        send_message(to=self.player_1_num, text=p1Message)
        send_message(to=self.player_2_num, text=p2Message)

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
        game = self.find_game_for_session()

        # Do player turn
        playing_player = self.get_player(sent_by)
        game_response = process_action(game, first_word, playing_player, remainder)

        p1Message = game_response[Players.PLAYER_ONE]
        p2Message = game_response[Players.PLAYER_TWO]

        game_finished = game_response['GAME_OVER']

        if game.current_player == Players.PLAYER_ONE:
            send_message_with_board(to=self.player_1_num, text=p1Message, board=game_response['PLAYER_2_BOARD'])
            send_message(to=self.player_2_num, text=p2Message)
        else:
            send_message(to=self.player_1_num, text=p1Message)
            send_message_with_board(to=self.player_2_num, text=p2Message, board=game_response['PLAYER_1_BOARD'])

        # Persist GameModel
        game_model = GameModel.toModel(game)
        game_model.save()

        return game_finished

    def find_game_for_session(self):
        try:
            game = GameModel.objects.get(id=self.game_id).toGame()
        except GameModel.DoesNotExist:
            game = None
        # Make new GameModel and persist
        if game is None:
            game = Game()
            game.place_some_ships()
            game_model = GameModel.toModel(game)
            print('CREATING NEW GAME')
            game_model.save()
            print('Created new game_model', game_model.id)
            print(game_model)
            self.game_id = game.session_id = game_model.id
            self.save()
        else:
            print('GAME FOUND')
            print(game)
        return game

    def get_player(self, phone_num: str):
        if phone_num == self.player_1_num:
            return Players.PLAYER_ONE
        else:
            return Players.PLAYER_TWO

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
