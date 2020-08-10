from card_deck.deck import Deck
from card_deck.suits import Suits
from card_deck.ranks import Ranks
from card_deck.card import Card
from core.player import Player
from core.turn import Turn
from core.exceptions import *
from typing import List

"""
TODO: Defined and detect tied game
TODO: Take cards from game deck (max 3)
"""
class CrazyEights():

    def __init__(self, players: List[str]):
        self.deck = Deck.make_french_deck()
        self.waiting_for_suit_change = False
        self.deck.shuffle()
        self.winner = None
        self.players = [Player(players[i], i) for i in range(len(players)) ]
    
    def deal_cards(self, qty: int = 5):
        for player in self.players:
            cards = [self.deck.take_last() for _ in range(qty)]
            player.player_deck = Deck(cards)
    
    def get_playerid_from_username(self, username: str):
        for player in self.players:
            if player.name == username:
                return player.turn_id
                
        else:
            return None
    
    def start_game(self):
        
        if not len(self.players):
            raise NoPlayersException()

        while (last_card := self.deck.take_last()).rank == Ranks.EIGHT:
            self.deck.place_at_bottom(last_card)

        self.turn_state  = Turn(0, last_card)
        return self.turn_state

    def _is_valid_move(self, card: Card):
        return card.suit == self.turn_state.current_card.suit or card.rank == self.turn_state.current_card.rank or self._is_wildcard(card)

    def _is_wildcard(self, card: Card):
        return card.rank == Ranks.EIGHT

    def make_move(self, player_id: int, card: Card):

        if self.is_game_finished():
            raise GameAlreadyFinishedException()

        if self.waiting_for_suit_change:
            raise WaitingForSuitChangeException()
        
        if self.turn_state.current_player_turn_id != player_id:
            raise NotYourTurnException()

        if not self._is_valid_move(card):
            raise InvalidMoveException()

        if card not in self.players[player_id].player_deck.cards:
            raise CardNotOnDeckException()

        if self._is_wildcard(card):
            self.waiting_for_suit_change = True
        
        self.players[player_id].player_deck.remove(card)

        if self.players[player_id].player_deck.is_empty():
            self.winner = self.players[player_id]
        
        self.turn_state = Turn( (self.turn_state.current_player_turn_id + 1) % len(self.players), card )

        return self.turn_state
    
    def needs_suit_change(self):
        return self.waiting_for_suit_change

    def change_suit(self, new_suit: Suits):
        if not self.waiting_for_suit_change:
            raise NotWaitingForSuitChangeException()

        self.turn_state.current_card.suit = new_suit
        self.waiting_for_suit_change = False
    
    def is_game_finished(self):
        return self.winner != None
    
    def get_player(self, turn_id):
        if len(self.players) > turn_id:
            return self.players[turn_id]
    
    def take_from_deck(self, turn_id):
        if len(self.players) > turn_id:
            last = self.deck.take_last()
            self.players[turn_id].player_deck.cards.append(last)
            return last
