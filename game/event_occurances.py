import random
from game.battleship_game import game, other_player
from game.game_entities import Ships


def event_check():
    if random.random() < 0.01:
        game.winning_player = 'Draw'		# TODO Everyone loses
        return 'A Kraken rises out of the sea! There were no survivors'
    elif random.random() < 0.03:
        return{
            game.current_player: 'Pirates have come for your bounty! They plunder your '
                                 + Ships.name
                                 + 'and your shipmates are made to walk the plank',
            other_player(game.current_player): 'The enemy has been attacked by pirates! Their battleship is no longer standing'
        }
    elif random.random() < 0.05:
        return 'A Tsunami hit! Your Submarine has been washed away..'
    elif random.random() < 0.07:
        return 'The enemy has cracked your secret code! Maybe next time don\'t use A=1..'
    elif random.random() < 0.09:
        return 'Mutiny on board! Your second in command reveals your location to an enemy ship'
