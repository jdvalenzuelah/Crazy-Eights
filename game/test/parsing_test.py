import context
from game_service.crazy_serializer.serialize import CrazySerializer
from core.player import Player
from core.turn import Turn
from card_deck.card import Card
from card_deck.ranks import Ranks
from card_deck.suits import Suits
from card_deck.deck import Deck
import unittest

class ParsingTest(unittest.TestCase):

    def setUp(self):
        self.serializer = CrazySerializer()
    
    def test_serialize_card(self):
        expected = Card(Ranks.ACE, Suits.DIAMONDS)
        card = 'A,diamonds'
        self.assertEqual(self.serializer.parse(card, Card), expected)
    
    def test_serialize_deck(self):
        expected = Deck([Card(Ranks.ACE, Suits.DIAMONDS), Card(Ranks.EIGHT, Suits.HEARTS)])
        deck = '[A,diamonds;8,hearts]'
        self.assertEqual(self.serializer.parse(deck, Deck), expected)
    
    def test_serilize_player(self):
        expected = Player('David', 1, Deck([Card(Ranks.ACE, Suits.DIAMONDS), Card(Ranks.EIGHT, Suits.HEARTS)]))
        player = 'David,1,[A,diamonds;8,hearts]'
        self.assertEqual(self.serializer.parse(player, Player), expected)
    
    def test_serialize_turn(self):
        expected = Turn(0, Card(Ranks.ACE, Suits.DIAMONDS))
        turn = '0,A,diamonds'
        self.assertEqual(self.serializer.parse(turn, Turn), expected)


if __name__ == "__main__":
    unittest.main()