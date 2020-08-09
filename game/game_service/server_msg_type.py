from enum import Enum

class ServerMsgType(Enum):
    ACK_CONN = '11'
    USER_CREATED = '12'
    ROOM_CREATED = '13'
    JOINED_ROOM = '14'
    GAME_STARTED = '15'
    YOUR_TURN = '16'
    NEW_GAME_MOVE = '17'
    STACK_CARD = '18'
    OUT_OF_GAME = '19'
    GAME_FINISHED = '20'
    ROOM_CLOSED = '21'
    ROOM_WINNER = '23'
    ERROR = '23'

    @classmethod
    def from_string(self, name: str):
        for msg_type in ServerMsgType:
            if msg_type.value == name:
                return msg_type