
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import socket
import logging
from .client_msg_type import ClientMsgType
from .server_msg_type import ServerMsgType
from card_deck.deck import Deck
from card_deck.card import Card
from card_deck.suits import Suits

ENCONDING = 'utf-8'

class Client:

    def __init__(self, server: str, port: int):
        self.server_info = (server, port)
        self.username = ''
        self.room_id = ''
        self.deck = Deck()
        self.event_actions = {
            'user_created': None,
            'room_created': None,
            'room_joined': None,
            'game_started': None,
            'game_move': None,
            'your_turn': None,
            'stack_card': None,
            'game_finished': None,
            'suit_change': None,
            'needs_suit_change': None,
            'room_finished': None,
            'room_winner': None,
            'error': None
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    """
    connect server
    """
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.server_info)
    
    def get_res_type(self, res: str) -> ServerMsgType:
        res = res.split('.')
        return ServerMsgType.from_string(res[0])
    

    def register_user(self, userid: str):

        logging.info(f'Connection to server {self.server_info}')
        
        req = f'{ClientMsgType.EST_CONN.value}'
        self.socket.sendall(req.encode(ENCONDING))
        
        res = self.socket.recv(1024).decode(ENCONDING)
        req_type = self.get_res_type(res)
        
        if req_type != ServerMsgType.ACK_CONN:
            logging.error('Error stablishing connection to server')
            return self.close()
        
        logging.info(f'Registering user {userid}')
        req = f'{ClientMsgType.ACK_CONN.value}.{userid}'
        self.socket.sendall(req.encode(ENCONDING))

        res = self.socket.recv(1024).decode(ENCONDING)
        res_type = self.get_res_type(res)
        if res_type == ServerMsgType.USER_CREATED:
            self.username = userid
            logging.info(f'User registered {res}')
            self._call_event('user_created', username=self.username)
            
    
    def create_room(self, rounds: int):
        logging.info('Creating new room')
        req = f'{ClientMsgType.NEW_ROOM.value}.{rounds}'
        self.socket.sendall(req.encode(ENCONDING))

        res = self.socket.recv(1024).decode(ENCONDING)
        res_type = self.get_res_type(res)
        if res_type == ServerMsgType.ROOM_CREATED:
            self.room_id = res.split('.')[1]
            logging.info(f'Room created {res}')
            self._call_event('room_created', room_id=self.room_id)
    
    def join_room(self, room_id: str):
        logging.debug(f'Trying to join room {room_id} as {self.username}')    
        if not self.username or not room_id:
            logging.error(f'Incorrect params {self.username}')
            return None
        
        req = f'{ClientMsgType.JOIN_ROOM.value}.{self.username},{room_id}'
        self.socket.sendall(req.encode(ENCONDING))
        
        res = self.socket.recv(1024).decode(ENCONDING)
        res_type = self.get_res_type(res)
        if res_type == ServerMsgType.JOINED_ROOM:
            logging.info(f'Joined room {res}')
            self.room_id = res.split('.')[1]
            self._call_event('room_joined', room_id=self.room_id)
    
    def start_game(self):
        req = f'{ClientMsgType.START_GAME.value}.{self.username},{self.room_id}'
        self.socket.sendall(req.encode(ENCONDING))
        self.listen()
    
    def listen(self):
        while ( res := self.socket.recv(1024).decode(ENCONDING) ):
            res_type = self.get_res_type(res)
            if res_type == ServerMsgType.GAME_STARTED:
                self.game_started(res)
            elif res_type == ServerMsgType.YOUR_TURN:
                self.game_turn(res)
            elif res_type == ServerMsgType.STACK_CARD:
                self.receive_stack_card(res)
            elif res_type == ServerMsgType.SUIT_NEEDS_CHANGE:
                self.on_needs_suit_change(res)
            elif res_type == ServerMsgType.SUIT_CHANGE:
                self.on_suit_change(res)
    
    def game_started(self, data):
        

        deck = Deck.parse(data[data.find('['):data.find(']')+1])
        current_card = Card.parse(f"{data.split(',')[-2]},{data.split(',')[-1]}")
        self.deck = deck
        self.current_card = current_card
        self._call_event('game_started', deck=self.deck, current_card=self.current_card)

    
    def game_turn(self, data):
        print(data)
        card = Card.parse(data.split('.')[1])
        self.current_card = card
        self._call_event('your_turn', current_card=card)
    
    def make_move(self, card: Card):
        if card in self.deck.cards:
            self.last_played_card = card
            self.deck.remove(card)
            card = card.serialize()
            req = f'{ClientMsgType.GAME_MOVE.value}.{self.room_id},{card}'
            self.socket.sendall(req.encode(ENCONDING))
    
    def take_from_stack(self):
        req = f'{ClientMsgType.GET_CARD_STACK.value}.{self.room_id}'
        self.socket.sendall(req.encode(ENCONDING))
    
    def receive_stack_card(self, data):
        data = data.split('.')
        card =Card.parse(data[1])
        self.deck.cards.append(card)
        self._call_event('stack_card', new_card=card, current_card=self.current_card)
    
    def on_needs_suit_change(self, data):
        self._call_event('needs_suit_change')
    
    def on_suit_change(self, data):
        data = data.split('.')
        suit = Suits.from_string(data[1])
        self._call_event('suit_change', new_suit=suit)
    
    def change_suit(self, suit: Suits):
        req = f'{ClientMsgType.SUIT_CHANGE.value}.{self.room_id},{suit.value}'
        self.socket.sendall(req.encode(ENCONDING))
    
    def on_game_move(self, data):
        print(data)
        self._call_event('game_move')
    
    def on_room_finished(self, data):
        self._call_event('room_finished')
    
    def on_room_winner(self, data):
        self._call_event('room_winner')
    
    def on_error(self, data):
        self._call_event('error')
    
    def on(self, event: str, action: callable):
        self.event_actions[event] = action

    def _default_callback(self, *args, **kwargs):
        logging.info(f'Incomming res: {args} {kwargs}')
    
    def _call_event(self, event: str, **kwargs):
        if not event in self.event_actions.keys():
            return

        if (action := self.event_actions[event]):
                action(**kwargs, context=self)
    
    def close(self):
        logging.debug('closing connection')
        self.socket.close()
