from enum import Enum


class Keyword(Enum):
    INVITE = 'INVITE'
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'
    QUIT = 'QUIT'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
