from sessions import sessions, gamesession


def invite(message, sent_by, to_num):
    response = 'You\'re inviting ' + message

    print(response)

    sessions.Sessions.add_session(sent_by, to_num)

    return response


def accept(message, session: gamesession.Session, sent_by):
    response = 'You\'ve accepted an invitation'

    print(response, message, session)

    session.player_2_accepted_invite()

    return response


def reject(message, session: gamesession.Session, sent_by):
    response = 'Player 2 rejected the invite ' + message

    session.player_2_rejected_invite()

    return response


def quit(message, session: gamesession.Session, sent_by):
    response = ''

    if session.player_1_num == sent_by:
        response = 'Player 1 has quit ' + message
        session.player_1_quit()
    else:
        session.player_2_quit()
        response = 'Player 2 has quit ' + message

    return response
