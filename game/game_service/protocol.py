import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server_msg_type import ServerMsgType
from client_msg_type import ClientMsgType
from core.room import Room
from card_deck.card import Card
from card_deck.suits import Suits
from card_deck.deck import Deck
from message import Message
from typing import List

def get_type_and_data(data: str):
    data = data.split('.')
    body = data[1] if len(data) > 1 else ""
    
    if (result := ServerMsgType.from_string(data[0])):
        return (result, body)
    elif (result := ClientMsgType.from_string(data[0])):
        return (result, body)
    else:
        return (None, None)

def parse_server_msg(type: ServerMsgType, data: str) -> Message:
    if type == ServerMsgType.ACK_CONN:
        return Message(type, {"empty": True})
    elif type == ServerMsgType.USER_CREATED:
        return Message(type, {"userid": data})
    elif type == ServerMsgType.ROOM_CREATED or type == ServerMsgType.JOINED_ROOM:
        return Message(type, {"roomid": data})
    elif type == ServerMsgType.GAME_STARTED:
        deck = Deck.parse(data[data.find('['):data.find(']')+1])
        data = data.split(',')
        roomid = data[0]
        current_card = Card.parse(f"{data[-2]},{data[-1]}")
        return Message(type, {"deck": deck, "current_card": current_card, "roomid": roomid})
    elif type == ServerMsgType.YOUR_TURN or type == ServerMsgType.NEW_GAME_MOVE or type == ServerMsgType.STACK_CARD:
        card = Card.parse(data)
        return Message(type, {"card": card})
    elif type == ServerMsgType.GAME_FINISHED:
        return Message(type, {"winner": winner})
    elif type == ServerMsgType.ROOM_CLOSED:
        pass
    elif type == ServerMsgType.ROOM_WINNER:
        pass
    elif type == ServerMsgType.ERROR:
        data = data.split(',')
        return Message(type, {'code': data[0], 'description': data[1]})
    elif type == ServerMsgType.SUIT_CHANGE:
        suit = Suits.from_string(data)
        return Message(type, {"suit": suit})
    elif type == ServerMsgType.SUIT_NEEDS_CHANGE:
        return Message(type, {"empty": True})

def parse_client_msg(type: ClientMsgType, data: str) -> Message:
    if type == ClientMsgType.EST_CONN:
        return Message(type, {"empty": True})
    elif type == ClientMsgType.ACK_CONN:
        return Message(type, {"userid": data})
    elif type == ClientMsgType.NEW_ROOM:
        return Message(type, {"rounds": data})
    elif type == ClientMsgType.JOIN_ROOM or type == ClientMsgType.START_GAME or type == ClientMsgType.CLOSE_ROOM:
        user, room = data.split(',')
        return Message(type, {"userid": user, "roomid": room})
    elif type == ClientMsgType.GAME_MOVE:
        data = data.split(',')
        roomid = data[0]
        card = Card.parse(f'{data[1]},{data[2]}')
        return Message(type, {"roomid": roomid, "card": card})
    elif type == ClientMsgType.GET_CARD_STACK:
        return Message(type, {"roomid": data})
    elif type == ClientMsgType.DISCONNECT:
        return Message(type, {"userid": data})
    elif type == ClientMsgType.SUIT_CHANGE:
        roomid, suit = data.split(',')
        suit = Suits.from_string(suit)
        return Message(type, {"suit": suit, "roomid":roomid})

def serialize_message(type: str, data: str) -> str:
    return f'{type}.{data}$'

def serialize_client_msg(type: ClientMsgType, **kwargs) -> str:
    if type == ClientMsgType.EST_CONN:
        return serialize_message(type.value, '')
    elif type == ClientMsgType.ACK_CONN:
        return serialize_message(type.value, kwargs['userid'])
    elif type == ClientMsgType.NEW_ROOM:
        return serialize_message(type.value, kwargs['rounds'])
    elif type == ClientMsgType.JOIN_ROOM or type == ClientMsgType.START_GAME or type == ClientMsgType.CLOSE_ROOM:
        data = f'{kwargs["userid"]},{kwargs["roomid"]}'
        return serialize_message(type.value, data)
    elif type == ClientMsgType.GAME_MOVE:
        card = kwargs["card"].serialize()
        data = f'{kwargs["roomid"]},{card}'
        return serialize_message(type.value, data)
    elif type == ClientMsgType.GET_CARD_STACK:
        return serialize_message(type.value, kwargs["roomid"])
    elif type == ClientMsgType.DISCONNECT:
        return serialize_message(type.value, kwargs["userid"])
    elif type == ClientMsgType.SUIT_CHANGE:
        data = f'{kwargs["roomid"]},{kwargs["suit"].value}'
        return serialize_message(type.value, data)

def serialize_server_msg(type: ServerMsgType, **kwargs) -> str:
    if type == ServerMsgType.ACK_CONN:
        return serialize_message(type.value, '')
    elif type == ServerMsgType.USER_CREATED:
        return serialize_message(type.value, kwargs['userid'])
    elif type == ServerMsgType.ROOM_CREATED or type == ServerMsgType.JOINED_ROOM:
        return serialize_message(type.value, kwargs['roomid'])
    elif type == ServerMsgType.GAME_STARTED:
        deck = kwargs['deck'].serialize()
        card = kwargs['current_card'].serialize()
        data = f'{kwargs["roomid"]},{deck},{card}'
        return serialize_message(type.value, data)
    elif type == ServerMsgType.YOUR_TURN or type == ServerMsgType.NEW_GAME_MOVE or type == ServerMsgType.STACK_CARD:
        card = kwargs['card'].serialize()
        return serialize_message(type.value, card)
    elif type == ServerMsgType.GAME_FINISHED or type == ServerMsgType.ROOM_WINNER:
        return serialize_message(type.value, kwargs['winner'])
    elif type == ServerMsgType.ROOM_CLOSED:
        pass
    elif type == ServerMsgType.ERROR:
        data = f"{kwargs['code']},{kwargs['description']}"
        return serialize_message(type.value, data)
    elif type == ServerMsgType.SUIT_CHANGE:
        return serialize_message(type.value, kwargs['suit'].value)
    elif type == ServerMsgType.SUIT_NEEDS_CHANGE:
        return serialize_message(type.value, '')

def get_raw(data: str) -> List[str]:
    data = data.split('$')
    data.remove('')
    return data

def parse_individual(message: str):
    msg_type, msg_data = get_type_and_data(message)
    if isinstance(msg_type, ServerMsgType):
        return parse_server_msg(msg_type, msg_data)
    elif isinstance(msg_type, ClientMsgType):
        return parse_client_msg(msg_type, msg_data)

def parse_message(data: str):
    return [ parse_individual(message) for message in get_raw(data) ]

def serialize(message: Message):
    if isinstance(message.type, ServerMsgType):
        return serialize_server_msg(message.type, **message.data)
    elif isinstance(message.type, ClientMsgType):
        return serialize_client_msg(message.type, **message.data)
