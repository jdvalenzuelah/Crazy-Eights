import random
from dataclasses import dataclass, field
from typing import List
from card_deck.suits import Suits
from card_deck.ranks import Ranks
from card_deck.card import Card
from game_service.crazy_serializer.crazy_class import CrazyClass

@dataclass
class Deck(CrazyClass):
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
    
    def is_empty(self):
        return len(self.cards) == 0
    
    def serialize(self):
        elements = ';'.join(value.serialize() for value in self.cards)
        return f'[{elements}]'
    
    @classmethod
    def parse(self, data):
        if not data.startswith('[') or not data.endswith(']'):
            return None
        data = data[1:-1].split(';')

        if None in (result := [Card.parse(card) for card in data]):
            return None
        return result
