import context
from game_service.crazy_serializer.serialize import CrazySerializer
from core.player import Player
from core.turn import Turn
from card_deck.card import Card
from card_deck.ranks import Ranks
from card_deck.suits import Suits
from card_deck.deck import Deck
import unittest

class SerializeTest(unittest.TestCase):

    def setUp(self):
        self.serializer = CrazySerializer()
    
    def test_serialize_card(self):
        card = Card(Ranks.ACE, Suits.DIAMONDS)
        expected = 'A,diamonds'
        self.assertEqual(self.serializer.serialize(card), expected)
    
    def test_serialize_deck(self):
        deck = Deck([Card(Ranks.ACE, Suits.DIAMONDS), Card(Ranks.EIGHT, Suits.HEARTS)])
        expected = '[A,diamonds;8,hearts]'
        self.assertEqual(self.serializer.serialize(deck), expected)
    
    def test_serilize_player(self):
        player = Player('David', 1, Deck([Card(Ranks.ACE, Suits.DIAMONDS), Card(Ranks.EIGHT, Suits.HEARTS)]))
        expected = 'David,1,[A,diamonds;8,hearts]'
        self.assertEqual(self.serializer.serialize(player), expected)
    
    def test_serialize_turn(self):
        turn = Turn(0, Card(Ranks.ACE, Suits.DIAMONDS))
        expected = '0,A,diamonds'
        self.assertEqual(self.serializer.serialize(turn), expected)


if __name__ == "__main__":
    unittest.main()