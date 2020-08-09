import socket
import logging
from threading import Thread, Lock
from threaded import threaded
import queue
from client_msg_type import ClientMsgType
from server_msg_type import ServerMsgType
from crazy_serializer.serialize import CrazySerializer
from protocol import get_message_type


logging.basicConfig(level=logging.DEBUG)

ENCONDING = 'utf-8'

class Server:

    def __init__(self, host: str, port: int):
        self.server_info = (host, int(port))

        self.conn_queue = queue.Queue()
        self.queue_mutex = Lock()

        self.parser = CrazySerializer()
        self.parser_mutex = Lock()

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
                    req_type = get_message_type(req)
                    if req_type == ClientMsgType.DISCONNECT:
                        break
                    elif req_type == ClientMsgType.NEW_USER:
                        logging.info(f'Creating new user {req}')
                        userid = req.split(',')[1]
        
    def close(self):
        logging.debug(f'closing connection')
        self.socket.close()

if __name__ == "__main__":
    with Server('127.0.0.1', 8080) as server:
        server.start()