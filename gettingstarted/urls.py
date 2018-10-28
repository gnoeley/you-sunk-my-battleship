from django.urls import path

from django.contrib import admin

admin.autodiscover()

import hello.views
from receive import receiver

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("receive", receiver.receive, name='receive'),
    path("db/", hello.views.db, name="db"),
    path('board-print/', hello.views.board_print, name="board-print" ),
    path("admin/", admin.site.urls),
]
