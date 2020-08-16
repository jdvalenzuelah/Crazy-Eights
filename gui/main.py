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

def on_user_created(**kwargs):
	logging.info(f'User created {kwargs["username"]}')
	eel.handle_login(kwargs["username"])


if __name__ == "__main__":
	import sys
	_, ip, port = sys.argv
	
	with Client(ip, int(port)) as client:
		client.on('user_created', on_user_created)

		client.connect()
		
		cw.set_client(client)

		eel.init('gui/Interface')
		eel.start('index.html')