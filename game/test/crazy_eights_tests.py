import context
from core.crazy_eights import CrazyEights
from core.exceptions import *
from core.turn import Turn
from card_deck.card import Card
from card_deck.ranks import Ranks
from card_deck.suits import Suits
from card_deck.deck import Deck
import unittest

class CrazyEightsTest(unittest.TestCase):

    def setUp(self):
        self.players = ['David', 'Marcos', 'Fernando']
        self.game = CrazyEights(self.players)

    def test_deal_cards(self):
        self.game.deal_cards(qty = 5)

        # should deal 5 cards
        for player in self.game.players:
            self.assertEqual( len(player.player_deck.cards), 5 )
    
    def test_start_game(self):
        start_state = self.game.start_game()
        # should start with player id 0
        self.assertEqual(start_state.current_player_turn_id, 0)
        # should not start with wildcard
        self.assertNotEqual(start_state.current_card, Ranks.EIGHT)
    
    def test_make_move(self):
        self.game.turn_state = Turn(0, Card(Ranks.FOUR, Suits.CLUBS))

        # Should raise exception on card not on player deck
        self.assertRaises(CardNotOnDeckException, self.game.make_move, 0, Card(Ranks.FOUR, Suits.HEARTS))

        self.game.players[0].player_deck = Deck([Card(Ranks.FIVE, Suits.HEARTS), Card(Ranks.FOUR, Suits.DIAMONDS), Card(Ranks.EIGHT, Suits.HEARTS)])

        # Should raise exception on invalid suit
        self.assertRaises(InvalidMoveException, self.game.make_move, 0, Card(Ranks.FIVE, Suits.HEARTS))

        # Should raise exception on invalid turn
        self.assertRaises(NotYourTurnException, self.game.make_move, 1, Card(Ranks.FIVE, Suits.HEARTS))

        # Should allow to place wildcard and update state
        self.assertEqual(Turn(1, Card(Ranks.EIGHT, Suits.HEARTS) ), self.game.make_move(0,  Card(Ranks.EIGHT, Suits.HEARTS)))

        # Should remove card after player move
        self.assertEqual( len(self.game.players[0].player_deck.cards), 2 )

        # Should force suit change after wildcard played
        self.assertRaises(WaitingForSuitChangeException, self.game.make_move, 1, Card(Ranks.FIVE, Suits.HEARTS))

        # Should allow suit change
        self.game.change_suit(Suits.DIAMONDS)
        self.assertFalse(self.game.waiting_for_suit_change)

        # Should raise exception if not waiting for suit change
        self.assertRaises(NotWaitingForSuitChangeException, self.game.change_suit, Suits.DIAMONDS)

if __name__ == '__main__':
    unittest.main()
