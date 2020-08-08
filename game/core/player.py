from card_deck.deck import Deck
from dataclasses import dataclass
from typing import List
from game_service.crazy_serializer.crazy_class import CrazyClass

@dataclass
class Player(CrazyClass):
    name: str
    turn_id: int
    player_deck: Deck = Deck()

    def serialize(self):
        return f'{self.name},{self.turn_id},{self.player_deck.serialize()}'
    
    @classmethod
    def parse(self, data):
        deck = data[data.find('['):data.find(']')+1]
        deck = Deck.parse(deck)

        if not deck:
            return deck

        data = data.split(',')
        if len(data) < 2 or not data[1].isnumeric():
            return None
        
        return Player(data[0], int(data[1]), deck)
