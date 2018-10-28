import random
from game.battleship_game import game
from game.battleship_game import other_player


def event_check():
    if random.random() < 0.01:
        game.winning_player = 'Draw'		# Everyone loses
        return 'A Kraken rises out of the sea! There were no survivors'
    elif random.random() < 0.03:
        return{
            game.winning_player: 'Pirates have come for your bounty! They plunder your battleship and your shipmates are made to walk the plank'
            # other_player(): ''
        }
    elif random.random() < 0.05:
        return 'A Tsunami hit! Your Submarine has been washed away..'
    elif random.random() < 0.07:
        return 'The enemy has cracked your secret code! Maybe next time don\'t use A=1..'
    elif random.random() < 0.09:
        return 'Mutany on board! Your second in command reveals your location to an enemy ship'
