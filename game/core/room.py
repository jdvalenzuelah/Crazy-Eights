from .crazy_eights import CrazyEights
from card_deck.card import Card
from card_deck.suits import Suits
from exceptions import *
import collections

"""
TODO: Add game loop
TODO: Keep track of scores and find room winner
"""
class Room():

    def __init__(self, rounds: int):
        self.clean_room(rounds)

    def clean_room(self, rounds: int):
        self.rounds = rounds
        self.played_rounds = 0
        self.players = collections.OrderedDict()
        self.game = None

    def add_new_player(self, username: str):
        if self.game:
            raise GameAlreadyOnCourseException()

        if len(self.players.keys()) == 7:
            raise RoomAlreadyFullException()

        if username in self.players.keys():
            raise UserNameAlreadyTakenException()

        if ',' in username or len(username) == 0:
            raise InvalidUserNameException()

        self.players[username.replace(' ', '_')] = 0



    def start_game(self):
        if len(self.players.keys()) < 2:
            raise NotEnoughPlayerException()

        if self.is_room_rounds_completed():
            raise RoomRoundsAlreadyCompletedException()

        if self.game:
            raise GameAlreadyOnCourseException()

        self.played_rounds += 1
        self.game = CrazyEights(list(self.players.keys()))
        self.game.deal_cards()
        self.game.start_game()
    
    def restart_room(self):
        self.played_rounds = 0
        for username in self.players:
            self.players[username] = 0
    
    def is_game_finished(self):
        return self.game.is_game_finished()
    
    def is_room_rounds_completed(self):
        self.played_rounds == self.rounds
    
    def move(self, username: str, move: Card):
        return self.game.make_move(self.game.get_playerid_from_username(username), move)
    
    def get_current_game_state(self):
        if self.game:
            return self.game.turn_state
    
    def take_from_deck(self, username):
        return self.game.take_from_deck( self.game.get_playerid_from_username(username) )
    
    def get_current_player(self):
        return self.game.get_player(self.get_current_game_state().current_player_turn_id)
    
    def change_game_suit(self, new_suit: Suits):
        self.game.change_suit(new_suit)
    
    def get_current_game_winner(self):    
        if (winner := self.game.winner):
            self.players[winner.name] += 1
        return winner
    
    def game_needs_suit_change(self):
        return self.game.needs_suit_change()

    def get_players_deck(self):
        players = {}
        for name in self.players.keys():
            players[name] = self.game.get_player(self.game.get_playerid_from_username(name)).player_deck
        return players





# --- test ----
def card_str_h(card):
    return f'{card.rank.value} {card.suit.value}'

def print_deck(deck):
    for i in range(len(deck.cards)):
        print(f'{i}. {card_str_h(deck.cards[i])}')

if __name__ == "__main__":
    room = Room(2)
    room.add_new_player('David')
    room.add_new_player('Marcos')
    room.add_new_player('Fernando')
    room.start_game()

    while not room.is_room_rounds_completed():
        print('  ---- Inicio de ronda ------ ')
        while not room.is_game_finished():
            current_state = room.get_current_game_state()
            current_player = room.get_current_player()

            print(f'Turno de {current_player.name} Carta en el maso {card_str_h(current_state.current_card)}')
            print('Cartas del jugador:')
            print_deck(current_player.player_deck)
            card_pos = int(input('Ingresa numero de carta a colocar o -1 para tomar del maso: '))
            if card_pos >  -1:
                room.move(current_player.name, current_player.player_deck.cards[card_pos])
                if room.game_needs_suit_change():
                    print('Cambio de carta necesario')
                    va_suits = [e for e in Suits]
                    for i in range(len(va_suits)):
                        print(f'{i}. {va_suits[i].value}')
                    change = int(input('Ingrese el numero de carta a cambiar: '))
                    room.change_game_suit(va_suits[change])
            else:
                room.take_from_deck(current_player.name)
        print(f'Ganador ronda: {room.get_current_game_winner()}')

