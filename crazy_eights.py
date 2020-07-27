from card_deck.deck import Deck
from card_deck.suits import Suits
from card_deck.ranks import Ranks
from card_deck.card import Card
from game.player import Player
from game.turn import Turn
from game.exceptions import *
from typing import List

class CrazyEights():

    def __init__(self, players: List[str]):
        self.deck = Deck.make_french_deck()
        self.deck.shuffle()
        self.players = [Player(players[i], i) for i in range(len(players)) ]
    
    def deal_cards(self, qty: int = 5):
        for player in self.players:
            cards = [self.deck.take_last() for _ in range(qty)]
            player.player_deck = Deck(cards)
    
    def start_game(self):
        
        if not len(self.players):
            raise NoPlayersException()

        while (last_card := self.deck.take_last()).rank == Ranks.EIGHT:
            self.deck.place_at_bottom(last_card)

        self.turn_state  = Turn(0, last_card)
        return self.turn_state

    def _is_valid_move(self, card: Card):
        return card.suit == self.turn_state.current_card.suit or self._is_wildcard(card) # if same number can place card?

    def _is_wildcard(self, card: Card):
        return card.rank == Ranks.EIGHT

    def make_move(self, player_id: int, card: Card):

        if self.waiting_for_suit_change:
            raise WaitingForSuitChangeException()
        
        if self.turn_state.current_player_turn_id != player_id:
            raise NotYourTurnException()

        if not self._is_valid_move(card):
            raise InvalidMoveException()

        if card not in self.players[player_id].player_deck:
            raise CardNotOnDeckException()

        if self._is_wildcard(card):
            self.waiting_for_suit_change = True
        
        self.players[player_id].player_deck.remove(card)

        self.turn_state = Turn( (self.turn_state.current_player_turn_id + 1) % len(self.players), card )

        return self.turn_state
    
    def change_suit(self, new_suit: Suits):
        if not self.waiting_for_suit_change:
            raise NotWaitingForSuitChangeException()

        self.turn_state.current_card.suit = new_suit
        self.waiting_for_suit_change = False
