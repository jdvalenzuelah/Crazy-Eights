from dataclasses import dataclass
from card_deck.suits import Suits
from card_deck.ranks import Ranks

@dataclass
class Card:
    rank: Ranks
    suit: Suits
