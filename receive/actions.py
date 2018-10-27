from sessions import sessions, gamesession

def invite(message, sent_by, to_num):
    response = ('You\'re inviting ' + message)

    print(response)

    sessions.Sessions.add_session(sent_by, to_num)

    return response


def accept(message, session: gamesession.Session):
    response = ('You\'ve accepted an invitation')

    print(response, message, session)

    session.player_2_accepted_invite()

    return response
