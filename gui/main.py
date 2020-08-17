import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_service.client import Client
import logging
import eel

logging.basicConfig(level=logging.DEBUG)

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
def start_game():
	global cw
	logging.debug('Starting game')
	cw.client.start_game()

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
	eel.make_move(deck, card)

def print_deck(deck):
	for i in range(len(deck.cards)):
		print(f'{i}. {card_str_h(deck.cards[i])}')

def card_str_h(card):
	return f'{card.rank.value} {card.suit.value}'

def on_turn(**kwargs):
	logging.debug(f'Your turn {kwargs}')

if __name__ == "__main__":
	import sys
	_, ip, port = sys.argv
	
	with Client(ip, int(port)) as client:
		client.on('user_created', on_user_created)
		client.on('room_created', on_room_created)
		client.on('room_joined', on_room_joined)
		client.on('game_started', on_game_started)
		client.on('your_turn', on_turn)
		
		client.connect()
		
		cw.set_client(client)

		eel.init('gui/Interface')
		eel.start('index.html')