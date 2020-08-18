import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_service.server import Server

if __name__ == "__main__":
    import sys
    _, port = sys.argv
    with Server(int(port)) as server:
        server.start()