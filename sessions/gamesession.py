from enum import Enum, auto

from hello.sms.stubSmsSender import sendMessage

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

    def __init__(self, player_1_num, player_2_num) -> None:
        self.player_1_num = player_1_num
        self.player_2_num = player_2_num
        self.session_state = SessionState.STARTING
        self.player_1_state = PlayerState.STARTING
        self.player_2_state = PlayerState.NOT_JOINED

    def invite_player_2(self):
        message = self.player_1_num + ' has invited you to a game of Battleships - text ACCEPT to join the game or REJECT to refuse'
        sendMessage(to=self.player_2_num, text=message)

        self.player_2_state = PlayerState.INVITED


    def player_2_accepted_invite(self):
        message = self.player_2_num + ' has accepted your invite.'
        sendMessage(to=self.player_1_num, text=message)

        self.player_1_state = PlayerState.IN_GAME
        self.player_2_state = PlayerState.IN_GAME
        self.session_state = SessionState.IN_GAME

    def player_2_rejected_invite(self):
        message = self.player_2_num + ' has rejected your invite :/'
        sendMessage(to=self.player_1_num, text=message)

        self.player_2_state = PlayerState.REJECTED
        self.session_state = SessionState.ENDED

    def player_1_quit(self):
        message = self.player_1_num + ' has quit the game :)'
        sendMessage(to=self.player_2_num, text=message)

        self.player_1_state = PlayerState.QUIT
        self.session_state = SessionState.ENDED

    def player_2_quit(self):
        message = self.player_2_num + ' has quit the game :)'
        sendMessage(to=self.player_1_num, text=message)

        self.player_2_state = PlayerState.QUIT
        self.session_state = SessionState.ENDED

    def __str__(self) -> str:
        return \
            "Message: {" + "session state:" + self.session_state + ", " + "player 1 number:" + self.player_1_num + ", " + "player 2 number:" + self.player_2_num + ", " + "player 1 state:" + self.player_1_state + ", player 2 state:" + self.player_2_state + "}"


