
from sessions.gamesession import Session


class Sessions:

    sessionsDict = dict()

    @staticmethod
    def add_session(player_1_num, player_2_num):
        session = Session(player_1_num, player_2_num)

        Sessions.sessionsDict[player_1_num] = session
        Sessions.sessionsDict[player_2_num] = session

        return session

    @staticmethod
    def get_session(player_num):
        return Sessions.sessionsDict[player_num]