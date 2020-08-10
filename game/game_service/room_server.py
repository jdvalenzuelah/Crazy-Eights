from dataclasses import dataclass
from core.room import Room
from typing import Dict

@dataclass
class RoomServer:
    room: Room
    connection_pool: Dict