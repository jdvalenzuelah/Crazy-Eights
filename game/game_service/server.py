import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import socket
import logging
from threading import Thread, Lock
from .threaded import threaded
import queue
import uuid
from .client_msg_type import ClientMsgType
from .server_msg_type import ServerMsgType
from core.room import Room
from card_deck.card import Card
from card_deck.suits import Suits
from .protocol import *
from .message import Message
from .room_server import RoomServer
from core.exceptions import *

logging.basicConfig(level=logging.DEBUG)

ENCONDING = 'utf-8'

class Server:

    def __init__(self, port: int):
        host = socket.gethostname()
        self.server_info = (host, int(port))

        self.conn_queue = queue.Queue()
        self.queue_mutex = Lock()

        self.room_pool = {}
        self.rooms_mutex = Lock()

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def start(self):
        logging.debug(f'starting server on port {self.server_info}')
        self.set_up_socket()
        while True:
            logging.info('Listening for connections...')
            conn, addr = self.socket.accept()
            logging.info(f'Incomming connection from {addr}')
            self.push_new_connection(conn)
            logging.debug('Processing incoming request on new thread')
            self.handle_request()
    
    def set_up_socket(self):
        self.socket = socket.socket()
        self.socket.bind( self.server_info )
        self.socket.listen()                     
    
    def push_new_connection(self, conn):
        self.queue_mutex.acquire()
        self.conn_queue.put(conn)
        self.queue_mutex.release()
    
    def get_conn(self):
        self.queue_mutex.acquire()
        conn = self.conn_queue.get()
        self.queue_mutex.release()
        return conn
    
    def parse_request(self, req: bytes) -> Message:
        req = req.decode(ENCONDING)
        return parse_message(req)
    
    def format_response(self, message: Message) -> bytes:
        res = serialize_server_msg(message.type, **message.data)
        return res.encode(ENCONDING)

    @threaded
    def handle_request(self):
        conn = self.get_conn()
        req = conn.recv(1024)
        req = self.parse_request(req)[0]
        logging.debug(f'Incomming request {req}')

        if req.type == ClientMsgType.EST_CONN:
            res = self.format_response(Message(ServerMsgType.ACK_CONN, {'empty': True}))
            conn.sendall(res)
            req = conn.recv(1024)
            req = self.parse_request(req)[0]
            if req.type != ClientMsgType.ACK_CONN:
                logging.error('Error on handshake, closing connection')
                conn.close()
            else:
                logging.info(f'Accepted connection {conn}')
                logging.info(f'Creating new user {req.data}')
                userid = req.data['userid']
                res = self.format_response(Message(ServerMsgType.USER_CREATED, {'userid': userid}))
                conn.sendall(res)
                self._listen_user(conn, userid)
                
    
    def _listen_user(self, conn, userid):
        while ( req := conn.recv(1024) ):
            logging.debug(f'Incomming request {req}')
            req = self.parse_request(req)
            for r in req:
                if r.type == ClientMsgType.DISCONNECT:
                    break
                else:
                    try:
                        self._process_all(r, conn, userid)
                    except Exception as e:
                        logging.error(e)
                        self._send_error(e, conn)
    
    def _send_error(self, e: Exception, conn):
        if isinstance(e, GameException):
            res = Message(ServerMsgType.ERROR, {'code': e.code, 'description': str(e)})
        else:
            res = Message(ServerMsgType.ERROR, {'code': '-1', 'description': f'unknown error {e}'})
        conn.sendall(self.format_response(res))
    
    def _process_all(self, req, conn, userid):
        res = self.process_request(req, userid, conn)
        if res:
            res = self.format_response(res)
            conn.sendall(res)
    
    def process_request(self, req: Message, userid: str, conn) -> Message:
        if req.type == ClientMsgType.NEW_ROOM:
            rounds = req.data['rounds']
            room = Room(int(rounds))
            room.add_new_player(userid)
            room_id =  self.new_room(room, userid, conn)
            return Message(ServerMsgType.ROOM_CREATED, {'roomid':room_id})
        elif req.type == ClientMsgType.JOIN_ROOM:
            self.join_room(req.data['roomid'], req.data['userid'], conn)
            return Message(ServerMsgType.JOINED_ROOM, req.data)
        elif req.type == ClientMsgType.START_GAME:
            self.start_game_and_send_decks(req.data['roomid'])
            self.send_turn(req.data['roomid'])
        elif req.type == ClientMsgType.GAME_MOVE:
            self.new_move(req.data['roomid'], userid, req.data['card'])
        elif req.type == ClientMsgType.SUIT_CHANGE:
            self.change_suit(req.data['roomid'], req.data['suit'])
        elif req.type == ClientMsgType.GET_CARD_STACK:
            card = self.take_from_deck(req.data['roomid'], userid)
            return Message(ServerMsgType.STACK_CARD, {'card': card})
    
    def new_room(self, room: Room, userid, conn):
        logging.info('Creating new room')
        self.rooms_mutex.acquire()
        room_id = str(uuid.uuid1())[:10]
        self.room_pool[room_id] = RoomServer(room, {userid: conn})
        self.rooms_mutex.release()
        return room_id
    
    def join_room(self, room_id: str, userid: str, conn):
        logging.info(f'{userid}: joining room {room_id}')
        self.rooms_mutex.acquire()
        self.room_pool[room_id].room.add_new_player(userid)
        self.room_pool[room_id].connection_pool[userid] = conn
        self.rooms_mutex.release()
    
    def get_players_deck(self, room_id: str, start: bool = False):
        self.rooms_mutex.acquire()
        if start:
            self.room_pool[room_id].room.start_game()
        decks = self.room_pool[room_id].room.get_players_deck()
        conn_pool = self.room_pool[room_id].connection_pool
        current_state = self.room_pool[room_id].room.get_current_game_state()
        self.rooms_mutex.release()
        return (decks, conn_pool, current_state)
    
    def start_game_and_send_decks(self, room_id):
        decks, conns, current_state = self.get_players_deck(room_id, start=True)
        current_card = current_state.current_card
        for id in decks.keys():
            logging.debug(f'sending deck to {id}')
            ser_deck = decks[id].serialize()
            res = self.format_response(Message(ServerMsgType.GAME_STARTED, {'roomid': room_id, 'deck': decks[id], 'current_card': current_card }))
            conns[id].sendall(res)
    
    def send_turn(self, room_id):
        logging.info(f'Sending turn from room {room_id}')
        current_state, _, current_player_conn = self.get_current_state(room_id)
        res = self.format_response(Message(ServerMsgType.YOUR_TURN, {'card': current_state.current_card}))
        current_player_conn.sendall(res)
    
    def get_current_state(self, room_id):
        self.rooms_mutex.acquire()
        current_state = self.room_pool[room_id].room.get_current_game_state()
        current_player = self.room_pool[room_id].room.get_current_player()
        current_player_conn = self.room_pool[room_id].connection_pool[current_player.name]
        self.rooms_mutex.release()
        return (current_state, current_player, current_player_conn)
    
    def new_move(self, room_id: str, userid: str, card: Card):
        self.rooms_mutex.acquire()
        current_player = self.room_pool[room_id].room.get_current_player()
        current_player_conn = self.room_pool[room_id].connection_pool[current_player.name]
        self.room_pool[room_id].room.move(userid, card)
        needs_suit_change = self.room_pool[room_id].room.game_needs_suit_change()
        is_game_finished = self.room_pool[room_id].room.is_game_finished()
        self.rooms_mutex.release()

        if  needs_suit_change:
            logging.info(f'Sending suit change to {current_player.name} at {current_player_conn}')
            res = self.format_response(Message(ServerMsgType.SUIT_NEEDS_CHANGE, {'empty': True}))
            current_player_conn.sendall(res)
        elif is_game_finished:
            self.send_game_winner(room_id)
        else:
            self.send_turn(room_id)
        
        self.send_move(room_id, userid)


    def send_move(self, room_id: str, userid: str):
        _, conns, current_state = self.get_players_deck(room_id)
        current_card = current_state.current_card
        for id in conns.keys():
            if id == userid:
                logging.debug(f'Skipping move maker {userid}')
                continue
            logging.debug(f'sending move to {id}')
            res = self.format_response(Message(ServerMsgType.NEW_GAME_MOVE, {'card': current_card}))
            conns[id].sendall(res)
        
    def change_suit(self, room_id, suit: Suits):
        self.rooms_mutex.acquire()
        self.room_pool[room_id].room.change_game_suit(suit)
        self.rooms_mutex.release()
        self.send_suit_change(room_id, suit)

    def send_suit_change(self, room_id: str, new_suit: Suits):
        _, conns, current_state = self.get_players_deck(room_id)
        current_card = current_state.current_card.serialize()
        for id in conns.keys():
            logging.debug(f'sending suit change to {id}')
            res = self.format_response(Message(ServerMsgType.SUIT_CHANGE, {'suit': new_suit}))
            conns[id].sendall(res)
            
        self.send_turn(room_id)

    def take_from_deck(self, room_id: str, userid: str):
        self.rooms_mutex.acquire()
        card = self.room_pool[room_id].room.take_from_deck(userid)
        self.rooms_mutex.release()
        return card

    def send_game_winner(self, room_id: str):
        _, conns, _ = self.get_players_deck(room_id)
        self.rooms_mutex.acquire()
        winner = self.room_pool[room_id].room.get_current_game_winner()
        room_winner = self.room_pool[room_id].room.get_room_winner() if self.room_pool[room_id].room.is_room_rounds_completed() else None
        self.rooms_mutex.release()
        for id in conns.keys():
            if winner:
                res = self.format_response(Message(ServerMsgType.GAME_FINISHED, {'winner': winner}))
                conns[id].sendall(res)

            if room_winner:
                res = Message(ServerMsgType.ROOM_WINNER, {'winner': room_winner})
                conns[id].sendall(res)
        
    def close(self):
        logging.debug('closing connection')
        self.socket.close()