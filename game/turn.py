from dataclasses import dataclass
from card_deck.card import Card

@dataclass
class Turn:
    current_player_turn_id: int
    current_card: Card
