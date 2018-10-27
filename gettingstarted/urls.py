from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views
import hello.ping.ping
import hello.receive.receiver
from receive import choose

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("ping", hello.ping.ping.pong, name="pong"),
    path("receive", hello.receive.receiver.receive, name='receive'),
    path("choose", choose.game, name="choose"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
]
