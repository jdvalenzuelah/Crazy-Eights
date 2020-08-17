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
<<<<<<< HEAD
"""
send data to js
"""
"""
login
"""
@eel.expose
def login(username):
	global cw
	logging.debug(f'Username was passed {username}')
	cw.client.register_user(username)

"""
created user
"""
def on_user_created(**kwargs):
	logging.info(f'User created {kwargs["username"]}')
	eel.handle_login(kwargs["username"])

"""
fist deck
"""



"""
player deck
"""
def deck(**kwargs):
	logging.debug((f'\nCurrent card: {card_str_h(kwargs["current_card"])}'))
	kwargs["deck"]
	eel.deck(kwargs["deck"])

"""
current card
"""
def current_card(**kwargs):
	
	logging.debug((f'\nCurrent card: {card_str_h(kwargs["current_card"])}'))
	eel.current_card(kwargs["current_card"])

"""
stack card 
"""
def stack_card(**kwargs):
	logging.debug((f'current card {card_str_h(kwargs["new_card"])}'))
	eel.stack_card(kwargs["new_card"])


def card_str_h(card):
    return f'{card.rank.value} {card.suit.value}'


"""
room id
"""
def room_id (**kwargs):
	logging.debug((f'id room {kwargs["room_id"]}'))

	
"""
turn id
"""
def on_turn(**kwargs):
	pass


if __name__ == "__main__":
	import sys
	_, ip, port = sys.argv
	
	with Client(ip, int(port)) as client:
		client.on('user_created', on_user_created)

		client.game_started("")

=======

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

def on_user_created(**kwargs):
	logging.debug(f'User created {kwargs}')
	eel.handle_login(kwargs['username'])

def on_room_created(**kwargs):
	logging.debug(f'Room created {kwargs}')
	eel.go_to_room()

def on_room_joined(**kwargs):
	logging.debug(f'Joined new room {kwargs}')
	eel.go_to_room()

if __name__ == "__main__":
	import sys
	_, ip, port = sys.argv
	
	with Client(ip, int(port)) as client:
		client.on('user_created', on_user_created)
		client.on('room_created', on_room_created)
		client.on('room_joined', on_room_joined)
		
>>>>>>> bc2a468d76751dfc58b53f5446b00a5201f11f62
		client.connect()
		
		cw.set_client(client)

		eel.init('gui/Interface')
		eel.start('index.html')