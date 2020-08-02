from crazy_eights import CrazyEights
from card_deck.card import Card
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

        if self.rounds == self.played_rounds:
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
    
    def move(self, username: str, move: Card):
        return self.game.make_move(self.game.get_playerid_from_username(username), card)

if __name__ == "__main__":
    room = Room(2)
    room.add_new_player('David')
    room.add_new_player('Marcos')
    room.add_new_player('Fernando')
    room.start_game()
    print(room.game)