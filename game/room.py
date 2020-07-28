from crazy_eights import CrazyEights
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
        if not self.game:
            raise GameAlreadyOnCourseException()

        if len(self.players.keys) == 7:
            raise RoomAlreadyFullException()

        if username in self.players.keys:
            raise UserNameAlreadyTakenException()

        if ',' in username or len(username) == 0:
            raise InvalidUserNameException()

        self.players[username.replace(' ', '_')] = 0
    
    def start_game(self):
        if len(self.players.keys) < 2:
            raise NotEnoughPlayerException()

        if self.rounds == self.played_rounds:
            raise RoomRoundsAlreadyCompletedException()

        if not self.game:
            raise GameAlreadyOnCourseException()

        self.played_rounds += 1
        self.game = CrazyEights(self.players)