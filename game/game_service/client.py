
import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9090        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'00,David')
    data = s.recv(1024)
    print('Received', repr(data))
    s.sendall(b'01,David')
    time.sleep(2)
    s.sendall(b'02,David')
    time.sleep(2)
    s.sendall(b'03,4')
    data = s.recv(1024)
    print('Received', repr(data))
    time.sleep(2)
    data = s.recv(1024)
    print('Received', repr(data))
    data = s.recv(1024)
    print('Received', repr(data))
