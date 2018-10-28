from enum import Enum

from game.battleship_game import Game
from game.game_entities import Players


class GameAction(Enum):
    FIRE = "FIRE"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


def process_fire(game: Game, player: Players, message: str):
    coords = parse_coordinate(message)
    print('Player ' + str(player) + ' is firing at ' + str(coords))
    return game.player_turn(player=player,position=coords)


GAME_ACTIONS = {
    GameAction.FIRE: process_fire
}

ROW_CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


def parse_coordinate(s: str) -> (int, int):
    row_char = s[0].capitalize()
    col_chars = s[1:]

    row_num = ROW_CHARS.index(row_char)
    col_num = int(col_chars)-1

    return col_num, row_num


def process_action(game: Game, action_keyword: str, player: Players, message: str):
    if GameAction.has_value(action_keyword):

        gameAction = GameAction[action_keyword]

        action_method = GAME_ACTIONS.get(gameAction)

        return action_method(game, player, message)