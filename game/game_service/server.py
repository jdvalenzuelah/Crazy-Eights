import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import socket
import logging
from threading import Thread, Lock
from threaded import threaded
import queue
import uuid
from client_msg_type import ClientMsgType
from server_msg_type import ServerMsgType
from core.room import Room
from protocol import get_message_type
from room_server import RoomServer

logging.basicConfig(level=logging.DEBUG)

ENCONDING = 'utf-8'

class Server:

    def __init__(self, host: str, port: int):
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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    @threaded
    def handle_request(self):
        conn = self.get_conn()
        req = conn.recv(1024).decode(ENCONDING)
        req_type = get_message_type(req)

        if req_type == ClientMsgType.EST_CONN:
            res = f'{ServerMsgType.ACK_CONN.value}'
            conn.sendall(res.encode(ENCONDING))
            req = conn.recv(1024).decode(ENCONDING)
            req_type = get_message_type(req)
            if req_type != ClientMsgType.ACK_CONN:
                logging.error('Error on handshke, closing connection')
                conn.close()
            else:
                logging.info(f'Accepted connection {conn}')
                userid = ''
                while ( req := conn.recv(1024).decode(ENCONDING) ):
                    logging.debug(f'Incomming request {req}')
                    req_type = get_message_type(req)
                    if req_type == ClientMsgType.DISCONNECT:
                        break
                    elif req_type == ClientMsgType.NEW_USER:
                        logging.info(f'Creating new user {req}')
                        userid = req.split(',')[1]
                    else:
                        res = self.process_request(req_type, req, userid, conn)
                        logging.debug(res)
                        if res:
                            res = res.encode(ENCONDING)
                            conn.sendall(res)
    
    def process_request(self, req_type: ClientMsgType, req: str, userid: str, conn):
        if req_type == ClientMsgType.NEW_ROOM:
            rounds = req.split(',')[1]
            room = Room(int(rounds))
            room.add_new_player(userid)
            room_id =  self.new_room(room, userid, conn)
            return self.get_response(ServerMsgType.ROOM_CREATED, room_id=room_id)
        elif req_type == ClientMsgType.JOIN_ROOM:
            data = req.split(',')
            self.join_room(data[2], data[1], conn)
            return self.get_response(ServerMsgType.JOINED_ROOM, room_id=data[2])
        elif req_type == ClientMsgType.START_GAME:
            self.start_game_and_send_decks(req.split(',')[2])
    
    def get_response(self, type: ServerMsgType, **kwargs) -> str:
        if type == ServerMsgType.ROOM_CREATED:
            return f'{type.value},{kwargs["room_id"]}'
        elif type == ServerMsgType.JOINED_ROOM:
            return f'{type.value},{kwargs["room_id"]}'
    
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
    
    def get_players_deck(self, room_id: str):
        self.rooms_mutex.acquire()
        self.room_pool[room_id].room.start_game()
        decks = self.room_pool[room_id].room.get_players_deck()
        conn_pool = self.room_pool[room_id].connection_pool
        self.rooms_mutex.release()
        return (decks, conn_pool)
    
    def start_game_and_send_decks(self, room_id):
        decks, conns = self.get_players_deck(room_id)
        for id in decks.keys():
            logging.debug(f'sending deck to {id}')
            ser_deck = decks[id].serialize()
            res = f'{ServerMsgType.GAME_STARTED.value},{room_id},{ser_deck}'
            conns[id].sendall(res.encode(ENCONDING))
        
    def close(self):
        logging.debug(f'closing connection')
        self.socket.close()

if __name__ == "__main__":
    with Server('127.0.0.1', 9090) as server:
        server.start()