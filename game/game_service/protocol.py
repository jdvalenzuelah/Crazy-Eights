from server_msg_type import ServerMsgType
from client_msg_type import ClientMsgType

def get_message_type(data: str):
    data = data.split(',')

    if (result := ServerMsgType.from_string(data[0])):
        return result
    elif (result := ClientMsgType.from_string(data[0])):
        return result
    else:
        return None