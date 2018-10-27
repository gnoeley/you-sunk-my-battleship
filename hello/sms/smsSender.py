from clockwork import clockwork
import os
api = clockwork.API(os.environ.get('CLOCKWORK_API_KEY'))


def sendMessage(to, text):
    message = clockwork.SMS(to=to, message=text)

    response = api.send(message)

    if response.success:
        print (response.id)
    else:
        print (response.error_code)
        print (response.error_message)


