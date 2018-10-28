from django.http import HttpResponse

from hello.message import Message
from hello.models import Dbsession
from .content_processor import process_content


def receive(request):
    message = Message(
        msg_id=request.GET.get('id'),
        from_num=request.GET.get('from'),
        to_num=request.GET.get('to'),
        keyword=request.GET.get('keyword'),
        content=request.GET.get('content'))

    print('received message: ')
    print(message)

    s = ''
    for sess in Dbsession.objects.all():
        print('looping over session: ' + str(sess))
        s = s + '\n\t\t' + str(sess)

    print('sessions: ' + s)

    response = process_content(message.content.upper, message.fromNum)

    return HttpResponse(response)
