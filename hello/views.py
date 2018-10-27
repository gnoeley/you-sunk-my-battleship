from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import os

# Create your views here.
def index(request):
    configVal = os.environ.get('A_CONFIG_VAR')

    return HttpResponse('Hello from Python! =>' + configVal)
    # return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
