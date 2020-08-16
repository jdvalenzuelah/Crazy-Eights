
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import socket
import logging
from threading import Thread, Lock
from threaded import threaded
from client_msg_type import ClientMsgType
from server_msg_type import ServerMsgType
from card_deck.deck import Deck
from card_deck.card import Card
from card_deck.suits import Suits
import protocol
from message import Message

#logging.basicConfig(level=logging.DEBUG)

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
        self._res_queue = []
        self.queue_mutex = Lock()
    
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
            
    def add_response_to_queue(self, res: iter):
        self.queue_mutex.acquire()
        self._res_queue.extend(res)
        self.queue_mutex.release()
    
    def get_latest_res(self) -> Message:
        self.queue_mutex.acquire()
        res =  self._res_queue.pop(0) if len(self._res_queue) > 0 else None
        self.queue_mutex.release()
        return res
    
    def parse_response(self, res: bytes):
        logging.info(f'Parsing incomming res: {res}')
        res = res.decode(ENCONDING)
        res = protocol.parse_message(res)
        if res:
            self.add_response_to_queue(res)

    def format_request(self, req: Message) -> bytes:
        return protocol.serialize(req).encode(ENCONDING)
    

    def register_user(self, userid: str):

        logging.info(f'Connection to server {self.server_info}')
        
        req = self.format_request(Message(ClientMsgType.EST_CONN, {'empty': True}))
        self.socket.sendall(req)
        
        res = self.socket.recv(1024)
        self.parse_response(res)
        res = self.get_latest_res()
        
        if res.type != ServerMsgType.ACK_CONN:
            logging.error('Error stablishing connection to server')
            return self.close()
        
        logging.info(f'Registering user {userid}')
        req = self.format_request(Message(ClientMsgType.ACK_CONN, {'userid': userid}))
        self.socket.sendall(req)

        res = self.socket.recv(1024)
        self.parse_response(res)
        res = self.get_latest_res()

        if res.type == ServerMsgType.USER_CREATED:
            self.username = userid
            logging.info(f'User registered {res}')
            self._call_event('user_created', username=self.username)
            
    
    def create_room(self, rounds: int):
        logging.info('Creating new room')
        req = self.format_request(Message(ClientMsgType.NEW_ROOM, {'rounds': rounds}))
        self.socket.sendall(req)

        res = self.socket.recv(1024)
        self.parse_response(res)
        res = self.get_latest_res()
        if res.type == ServerMsgType.ROOM_CREATED:
            self.room_id = res.data['roomid']
            logging.info(f'Room created {res}')
            self._call_event('room_created', room_id=self.room_id)
    
    def join_room(self, room_id: str):
        logging.debug(f'Trying to join room {room_id} as {self.username}')    
        if not self.username or not room_id:
            logging.error(f'Incorrect params {self.username}')
            return None
        
        req = self.format_request(Message(ClientMsgType.JOIN_ROOM, {'userid': self.username, 'roomid':room_id}))
        self.socket.sendall(req)
        
        res = self.socket.recv(1024)
        self.parse_response(res)
        res = self.get_latest_res()
        if res.type == ServerMsgType.JOINED_ROOM:
            logging.info(f'Joined room {res}')
            self.room_id = res.data['roomid']
            self._call_event('room_joined', room_id=self.room_id)
    
    def start_game(self):
        req = self.format_request(Message(ClientMsgType.START_GAME, {'userid': self.username, 'roomid': self.room_id}))
        self.socket.sendall(req)
        self.start()
    
    def start(self):
        logging.info('Initialing response processor')
        self.process_responses()
        logging.info('Listening for messages')
        self.listen()

    
    def listen(self):
        logging.info('Listening for message from server')
        while ( res := self.socket.recv(1024) ):
            if not res:
                break
            else:
                self.parse_response(res)
        
        logging.info('Connection was terminated by server')
        self.close()

    @threaded        
    def process_responses(self):
        logging.info('Processing responses')
        while True:
            if ( res := self.get_latest_res()):
                if res.type == ServerMsgType.GAME_STARTED:
                    self.game_started(**res.data)
                elif res.type  == ServerMsgType.YOUR_TURN:
                    self.game_turn(**res.data)
                elif res.type  == ServerMsgType.STACK_CARD:
                    self.receive_stack_card(**res.data)
                elif res.type  == ServerMsgType.SUIT_NEEDS_CHANGE:
                    self.on_needs_suit_change(**res.data)
                elif res.type  == ServerMsgType.SUIT_CHANGE:
                    self.on_suit_change(**res.data)
                elif res.type  == ServerMsgType.GAME_FINISHED:
                    self.on_game_finished(**res.data)
                elif res.type == ServerMsgType.ROOM_WINNER:
                    self.on_room_winner(**res.data)
                elif res.type  == ServerMsgType.ERROR:
                    self.on_error(**res.data)
    
    def game_started(self, **kwargs):
        self.deck = kwargs['deck']
        self.current_card = kwargs['current_card']
        self._call_event('game_started', deck=self.deck, current_card=self.current_card)

    
    def game_turn(self, **kwargs):
        self.current_card = kwargs['card']
        self._call_event('your_turn', current_card=self.current_card)
    
    def make_move(self, card: Card):
        if card in self.deck.cards:
            self.last_played_card = card
            self.deck.remove(card)
            req = self.format_request(Message(ClientMsgType.GAME_MOVE, {'card': card, 'roomid': self.room_id}))
            self.socket.sendall(req)
    
    def take_from_stack(self):
        req = self.format_request(Message(ClientMsgType.GET_CARD_STACK, {'roomid':self.room_id}))
        self.socket.sendall(req)
    
    def receive_stack_card(self, **kwargs):
        card = kwargs['card']
        self.deck.cards.append(card)
        self._call_event('stack_card', new_card=card, current_card=self.current_card)
    
    def on_needs_suit_change(self, **kwargs):
        self._call_event('needs_suit_change')
    
    def on_suit_change(self, **kwargs):
        suit = kwargs['suit']
        self.current_card.suit = suit
        self._call_event('suit_change', new_suit=suit)
    
    def change_suit(self, suit: Suits):
        req = self.format_request(Message(ClientMsgType.SUIT_CHANGE, {'roomid': self.room_id, 'suit': suit}))
        self.socket.sendall(req)
    
    def on_game_move(self, **kwargs):
        self._call_event('game_move', **kwargs)
    
    def on_room_finished(self, **kwargs):
        self._call_event('room_finished', **kwargs)
    
    def on_room_winner(self, **kwargs):
        self._call_event('room_winner', **kwargs)
    
    def on_game_finished(self, **kwargs):
        self._call_event('game_finished', **kwargs)
    
    def on_error(self, **kwargs):
        self._call_event('error', **kwargs)
    
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
