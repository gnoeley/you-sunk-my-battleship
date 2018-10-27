from django.http import HttpResponse

def game(request):
    # TODO instantiate game and send message
    return HttpResponse('Game selected: ' + request.GET.get('game'))