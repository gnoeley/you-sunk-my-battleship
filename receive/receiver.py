from django.http import HttpResponse

from hello.message import Message
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

    response = process_content(message.content)

    return HttpResponse(response)
