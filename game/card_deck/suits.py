from enum import Enum

class Suits(Enum):
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'
    HEARTS = 'hearts'
    SPADES = 'spades'

    @classmethod
    def from_string(self, name: str):
        for suit in Suits:
            if suit.value == name:
                return suit