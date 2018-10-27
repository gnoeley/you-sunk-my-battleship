from enum import Enum, auto

from hello.sms.stubSmsSender import sendMessage
from receive.content_processor import Keyword


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
        sendMessage(to=self.player_1_num, text=self.player_2_num + ' has been invited')
        sendMessage(to=self.player_2_num,
                    text=self.player_1_num + ' has invited you to a game of Battleships - text ' + Keyword.ACCEPT.value + ' to join the game or ' + Keyword.QUIT.value + ' to refuse')

        self.player_2_state = PlayerState.INVITED

    def player_2_accepted_invite(self):
        sendMessage(to=self.player_1_num,
                    text=self.player_2_num + ' has accepted your invite.' + ' reply ' + Keyword.QUIT.value + ' to quit')
        sendMessage(to=self.player_2_num,
                    text='You are now in a game with: ' + self.player_1_num + ' reply ' + Keyword.QUIT.value + ' to quit')

        self.player_1_state = PlayerState.IN_GAME
        self.player_2_state = PlayerState.IN_GAME
        self.session_state = SessionState.IN_GAME

    def player_2_rejected_invite(self):
        sendMessage(to=self.player_1_num,
                    text=self.player_2_num + ' has rejected your invite.' + ' reply ' + Keyword.INVITE.value + ' with a number to invite someone else')
        sendMessage(to=self.player_2_num,
                    text='Why so serious?')

        self.player_2_state = PlayerState.REJECTED
        self.session_state = SessionState.ENDED

    def player_1_quit(self):
        sendMessage(to=self.player_1_num,
                    text='Bye')
        sendMessage(to=self.player_2_num,
                    text='Player 1 left')

        self.player_1_state = PlayerState.QUIT
        self.session_state = SessionState.ENDED

    def player_2_quit(self):
        sendMessage(to=self.player_1_num,
                    text='Player 2 left')
        sendMessage(to=self.player_2_num,
                    text='Bye')
        self.player_2_state = PlayerState.QUIT
        self.session_state = SessionState.ENDED

    def __str__(self) -> str:
        return \
            "Session: {" + \
            "session state:" + self.session_state.name + \
            ", player 1 number:" + self.player_1_num + \
            ", player 2 number:" + self.player_2_num + \
            ", player 1 state:" + self.player_1_state.name + \
            ", player 2 state:" + self.player_2_state.name + \
            "}"


