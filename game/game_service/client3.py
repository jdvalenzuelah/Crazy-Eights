import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9090        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'00,kkk')
    data = s.recv(1024)
    s.sendall(b'01,kkk')
    time.sleep(2)
    s.sendall(b'02,kkk')
    time.sleep(2)
    s.sendall(b'04,kkk,6e490084-d')
    data = s.recv(1024)
    print('Received', repr(data))
    time.sleep(2)
    print('sending 5')
    s.sendall(b'05,kkk,6e490084-d')
    data = s.recv(1024)
    print('Received', repr(data))
    data = s.recv(1024)
    print('Received', repr(data))