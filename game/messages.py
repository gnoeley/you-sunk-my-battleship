import random

from game.game_entities import Ships, Players, available_ships

message_to_player_when_missing_opponent = [
    'Try again loser',
    'Small children have better aim',
    'You hit one! If hit one is slang for not even close',
    'Missed, maybe try your hand at world peace instead of war'
]

message_to_player_when_hitting_opponent = [
    'BOOM! You got one',
    'Spot on!',
    'Bang! That sound of people screaming is because you did a good job',
    'All those years in the simulator have finally paid off. Direct hit.',
    'Achievement unlocked - widow maker! How does it feel?',
    'Well done.'
]

message_to_player_when_other_player_missed = [
    'All your ships are still safe',
    'No damage this time',
    'Your ships are hanging on'
]

message_to_player_when_own_ship_hit = {
    Ships.CARRIER.name: [
        'Your carrier is hit! Minimal damage sustained',
        'Your carrier is hit again! Distress signal launched!',
        'A third hit on your carrier, start preparing life boats',
        'Fourth hit on carrier! Start sending messages to loved ones',
        'Your carrier is sunk, 16 of your finest men have died'
    ],
    Ships.BATTLESHIP.name: [
        'Battleship hit! One of your caliber guns is out',
        'A second attack on your battleship, two more caliber guns are hit, you have one remaining',
        'A third hit on your battleship, it is no longer fit for battle.',
        'Your battleship is down, a memorial for lost souls is scheduled next week'
    ],
    Ships.CRUISER.name: [
        'Cruiser hit, still cruising, but less smoothly',
        'Another hit on the cruiser! It\'s starting to sink',
        'Cruiser down, the seas are cruise free once again'
    ],
    Ships.SUBMARINE.name: [
        'Submarine down! Though it\'s not exactly sinking because it/s already underwater',
        'Another hit on submarine! Shipmates are breaking out into an emotional rendition of yellow submarine',
        'Submarine destroyed! Luckily it\'s pretty airtight, so people will die when the air runs out instead of drowning'
    ],
    Ships.DESTROYER.name: [
        'Destroyer hit! Cue titanic theme song',
        'Destroyer is down, those poor souls never had a chance'
    ]
}

class MessageMaker:

    def __init__(self, hits_take=None):
        self.hits_taken = {
            Players.PLAYER_ONE.name: {
                Ships.CARRIER.name: 0,
                Ships.BATTLESHIP.name: 0,
                Ships.CRUISER.name: 0,
                Ships.SUBMARINE.name: 0,
                Ships.DESTROYER.name: 0
            },
            Players.PLAYER_TWO.name: {
                Ships.CARRIER.name: 0,
                Ships.BATTLESHIP.name: 0,
                Ships.CRUISER.name: 0,
                Ships.SUBMARINE.name: 0,
                Ships.DESTROYER.name: 0
            }
        } if hits_take is None else hits_take

    def is_ship_sunk(self, player: Players, ship: Ships):
        return self.hits_taken[player.name][ship.name] >= available_ships[ship].size

    @staticmethod
    def make_turn_status(player, current_player):
        if player == current_player:
            return '\nIt\'s your opponent\'s turn.'
        else:
            return '\nIt\'s your turn!'

    def make_message(self, player, current_player, winning_player, type_of_ship_hit):
        if winning_player is not None:
            return self.make_player_won_message(player, winning_player)

        current_player_turn = player is current_player
        if current_player_turn:
            if type_of_ship_hit:
                if self.is_ship_sunk(Players.other_player(current_player), type_of_ship_hit):
                    return 'You sunk their ' + type_of_ship_hit.name.lower() + "!"
                else:
                    return message_to_player_when_hitting_opponent[random.randint(0, 5)]
            else:
                return message_to_player_when_missing_opponent[random.randint(0, 2)]
        else:
            if type_of_ship_hit:
                type_of_ship_name = type_of_ship_hit.name
                message = message_to_player_when_own_ship_hit[type_of_ship_name][self.hits_taken[player.name][type_of_ship_name]]
                self.hits_taken[player.name][type_of_ship_name] += 1
                return message
            else:
                return message_to_player_when_other_player_missed[random.randint(0, 2)]

    @staticmethod
    def make_player_won_message(player, winning_player):
        return 'You won!' if winning_player is player else 'You lose!'

