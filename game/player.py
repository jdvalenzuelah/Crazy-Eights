from card_deck.deck import Deck
from dataclasses import dataclass
from typing import List

@dataclass
class Player:
    name: str
    turn_id: int
    current_score: int = 0
    player_deck: Deck = Deck()