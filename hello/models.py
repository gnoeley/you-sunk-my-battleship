from django.db import models



# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class Dbsession(models.Model):
    player1=models.CharField(max_length=100)
    player2=models.CharField(max_length=100)
    session_state = models.CharField(max_length=100)
    player_1_state = models.CharField(max_length=100)
    player_2_state = models.CharField(max_length=100)

    def __str__(self) -> str:
        return \
            "Session: {" + \
            "session state:" + self.session_state + \
            ", player 1 :" + self.player1 + \
            ", player 2 :" + self.player2 + \
            ", player 1 state:" + self.player_1_state + \
            ", player 2 state:" + self.player_2_state + \
            "}"


