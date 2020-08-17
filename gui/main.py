import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_service.client import Client
from game.game_service.threaded import threaded
from game.card_deck.card import Card
from card_deck.ranks import Ranks
from card_deck.suits import Suits
import logging
import eel

logging.basicConfig(level=logging.DEBUG)

ranks_js = {
    '1': 'A',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
    '11': 'J',
    '12': 'Q',
    '13': 'K'
}

suits_js = {
    'c': 'clubs',
    'd': 'diamonds',
    'h': 'hearts',
    's': 'spades'
}

class wrapper:
	def __init__(self):
		self.client = None
	
	def set_client(self, client):
		self.client = client

cw = wrapper()

@eel.expose
def login(username):
	global cw
	logging.debug(f'Username was passed {username}')
	cw.client.register_user(username)

@eel.expose
def create_new_room(rounds):
	global cw
	logging.debug(f'Creating new room {rounds}')
	cw.client.create_room(int(rounds))

@eel.expose
def join_room(roomid):
	global cw
	logging.debug(f'Joining new room {roomid}')
	cw.client.join_room(roomid)

@eel.expose
def make_move(suit, rank):
	global cw
	suit = Suits.from_string(suits_js[suit])
	rank = Ranks.from_string(ranks_js[rank])
	card_server = Card(rank, suit)
	logging.debug(f'Card in turn: {card_server}')
	logging.debug(f'Received move from ui: {suit} {rank}')
	cw.client.make_move(card_server)


@eel.expose
def take_from_stack():
	global cw
	logging.info('Tacking card from stack')
	cw.client.take_from_stack()

@eel.expose
def change_suit(suit):
	global cw
	logging.info(f'Changing suit {suit}')
	suit = Suits.from_string(suit)
	cw.client.change_suit(suit)

@eel.expose
def start_game():
	global cw
	logging.debug('Starting game')
	eel.spawn(start)

def on_user_created(**kwargs):
	logging.debug(f'User created {kwargs}')
	eel.handle_login(kwargs['username'])

def on_room_created(**kwargs):
	logging.debug(f'Room created {kwargs}')
	eel.after_created(kwargs['room_id'])

def on_room_joined(**kwargs):
	logging.debug(f'Joined new room {kwargs}')
	eel.after_joined(kwargs['room_id'])
	logging.info("Waiting for adming to start game...")
	kwargs['context'].start()

def on_game_started(**kwargs):
	logging.debug(f'Game started {kwargs}')
	deck = kwargs['deck'].serialize()
	card = kwargs['current_card'].serialize()
	eel.on_game_started(deck, card)

def on_turn(**kwargs):
	logging.debug(f'New game move {kwargs}')
	card = kwargs['current_card'].serialize()
	eel.receive_card(card)

def on_your_turn(**kwargs):
	logging.debug(f'Your turn {kwargs}')
	eel.alert_turn(card)

def on_stack_card(**kwargs):
	logging.debug(f'Stack card received {kwargs}')
	card = kwargs['new_card'].serialize()
	eel.on_stack_card(card)

def on_suit_change(**kwargs):
	logging.info('Suit change required!')
	eel.on_suit_change()

def on_game_finished(**kwargs):
	eel.alert_winner(kwargs['winner'])

def on_room_winner(**kwargs):
	eel.alert_winner(kwargs['winner'])

def on_error(**kwargs):
	eel.handle_error(kwargs['code'])

@threaded
def start():
	global cw
	cw.client.start_game()

if __name__ == "__main__":
	import sys
	_, ip, port = sys.argv
	
	with Client(ip, int(port)) as client:
		client.on('user_created', on_user_created)
		client.on('room_created', on_room_created)
		client.on('room_joined', on_room_joined)
		client.on('game_started', on_game_started)
		client.on('your_turn', on_turn)
		client.on('game_move', on_turn)
		client.on('stack_card', on_stack_card)
		client.on('needs_suit_change', on_suit_change)
		client.on('game_finished', on_game_finished)
		client.on('room_winner', on_room_winner)
		client.on('error', on_error)
		
		client.connect()
		
		cw.set_client(client)

		eel.init('gui/Interface')
		eel.start('index.html', block=False)
		while True:
			#print("I'm a main loop")
			eel.sleep(1.0)