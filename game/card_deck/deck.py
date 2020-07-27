import random
from dataclasses import dataclass, field
from typing import List
from card_deck.suits import Suits
from card_deck.ranks import Ranks
from card_deck.card import Card

@dataclass
class Deck:
    cards: List[Card] = field(default_factory=lambda: [])

    @staticmethod
    def make_french_deck():
        cards = [Card(rank, suit) for suit in Suits for rank in Ranks]
        return Deck(cards)

    def shuffle(self):
        random.shuffle(self.cards)
    
    def take_last(self):
        return self.cards.pop(0)
    
    def place_at_bottom(self, card: Card):
        if card not in self.cards:
            self.cards.append(card)
    
    def remove(self, card: Card):
        self.cards.remove(card)

