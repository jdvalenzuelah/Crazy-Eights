from dataclasses import dataclass
from card_deck.suits import Suits
from card_deck.ranks import Ranks
from game_service.crazy_serializer.crazy_class import CrazyClass

@dataclass
class Card(CrazyClass):
    rank: Ranks
    suit: Suits

    @classmethod
    def parse(self, data):
        list_vals = data.split(',')

        if len(list_vals) < 2:
            return None
        
        rank = Ranks.from_string(list_vals[0])
        suit = Suits.from_string(list_vals[1])

        if not rank or not suit:
            return None
        
        return Card(rank, suit)
    
    def serialize(self):
        return f'{self.rank.value},{self.suit.value}'
