from dataclasses import dataclass
from card_deck.card import Card
from card_deck.ranks import Ranks
from card_deck.suits import Suits

@dataclass
class Turn:
    current_player_turn_id: int
    current_card: Card

    def serialize(self):
        return f'{self.current_player_turn_id},{self.current_card.serialize()}'
    
    @classmethod
    def parse(self, data):
        data = data.split(',')

        if len(data) < 3 or not data[0].isnumeric():
            return None
        
        card = Card.parse(f'{data[1]},{data[2]}')

        return Turn(int(data[0]), card)
