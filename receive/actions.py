from sessions import sessions, gamesession


def invite(message, sent_by, to_num):
    session = sessions.Sessions.add_session(sent_by, message)
    response = session.invite_player_2()

    print(response)

    return response


def accept(message, session: gamesession.Session, sent_by):
    response = session.player_2_accepted_invite()

    print(response, message, session)

    return response


def reject(message, session: gamesession.Session, sent_by):
    response = session.player_2_rejected_invite()

    print(response)

    return response


def quit(message, session: gamesession.Session, sent_by):
    response = ''

    if session.player_1_num == sent_by:
        response = 'Player 1 has quit ' + message
        session.player_1_quit()
    else:
        session.player_2_quit()
        response = 'Player 2 has quit ' + message

    print(response)

    return response
