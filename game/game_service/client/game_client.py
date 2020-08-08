import logging

logging.basicConfig(level=logging.INFO)

class GameClient:

    def __init__(self, server_ip: str, server_port: int):
        self.server_info = (server_ip, server_port)
    
    def start()
