from enum import Enum

class ClientMsgType(Enum):
    EST_CONN = '00'
    ACK_CONN = '01'
    NEW_ROOM = '03'
    JOIN_ROOM = '04'
    START_GAME = '05'
    GAME_MOVE = '06'
    GET_CARD_STACK = '07'
    LEAVE_ROOM = '08'
    CLOSE_ROOM = '09'
    DISCONNECT = '10'
    SUIT_CHANGE = '26'

    @classmethod
    def from_string(self, name: str):
        for msg_type in ClientMsgType:
            if msg_type.value == name:
                return msg_type