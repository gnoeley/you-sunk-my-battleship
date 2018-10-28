from clockwork import clockwork
import os
api = clockwork.API(os.environ.get('CLOCKWORK_API_KEY'))


def sendMessage(to, text):
    if os.environ.get('SEND_SMS') != 'True':
        print('Would have sent "' + text + '" to ' + to)
    else:
        from_name = os.environ.get('FROM_SMS')
        print('Sending "' + text + '" to ' + to + " from " + from_name)
        message = clockwork.SMS(to=to, message=text, from_name=from_name)

        response = api.send(message)

        if response.success:
            print(response.id)
        else:
            print(response.error_code)
            print(response.error_message)


