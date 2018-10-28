from django.db import models
import json


# Create your models here.
from game.battleship_game import Game
from game.game_entities import Players


class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class Dbsession(models.Model):
    game_id = models.CharField(max_length=100, null=True)
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    session_state = models.CharField(max_length=100)
    player_1_state = models.CharField(max_length=100)
    player_2_state = models.CharField(max_length=100)

    def __str__(self) -> str:
        return \
            "Session: {" + \
            "session state:" + self.session_state + \
            ", game ID :" + (self.game_id or '') + \
            ", player 1 :" + self.player1 + \
            ", player 2 :" + self.player2 + \
            ", player 1 state:" + self.player_1_state + \
            ", player 2 state:" + self.player_2_state + \
            "}"


class GameModel(models.Model):
    player_one_board = models.CharField(max_length=10000)
    player_two_board = models.CharField(max_length=10000)
    current_player = models.CharField(max_length=100)
    winning_player = models.CharField(max_length=100, null=True)
    hits_taken = models.CharField(max_length=10000)

    def get_player_one_board(self):
        return json.load(self.player_one_board)

    def get_player_two_board(self):
        return json.load(self.player_two_board)


    def toGame(self):
        return Game(
            self.id,
            Players[self.current_player],
            json.loads(self.player_one_board),
            json.loads(self.player_two_board),
            None if self.winning_player is None else Players[self.winning_player]
        )

    def __str__(self) -> str:
        winning_player = '' if self.winning_player is None else self.winning_player.name
        return "Game: {" \
            "id:" + str(self.id) + \
            ", current_player: " + self.current_player + \
            ", player_one_board: " + self.player_one_board + \
            ", player_two_board: " + self.player_two_board + \
            ", winning_player: " + winning_player + \
            ", hits_taken: " + self.hits_taken + \
            "}"

    @staticmethod
    def toModel(game):
        model = GameModel()

        if game.session_id:
            model.id = game.session_id

        model.current_player = game.current_player.name
        model.player_one_board = json.dumps(game.player_one_board)
        model.player_two_board = json.dumps(game.player_two_board)
        model.winning_player = None if game.winning_player is None else game.winning_player.name
        model.hits_taken = json.dumps(game.message_maker.hits_taken)

        return model
