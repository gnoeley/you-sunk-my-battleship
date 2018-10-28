from enum import Enum


class Players(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2


class Ship:
    def __init__(self, size, character):
        self.size = size
        self.character = character


class Ships(Enum):
    CARRIER = 1,
    BATTLESHIP = 2,
    CRUISER = 3,
    SUBMARINE = 4,
    DESTROYER = 5


available_ships = {
    Ships.CARRIER: Ship(5, 'CA'),
    Ships.BATTLESHIP: Ship(4, 'B'),
    Ships.CRUISER: Ship(3, 'CR'),
    Ships.SUBMARINE: Ship(3, 'S'),
    Ships.DESTROYER: Ship(2, 'D')
}
