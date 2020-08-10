from client import Client
import logging


#logging.basicConfig(level=logging.DEBUG)

def print_deck(deck):
    for i in range(len(deck.cards)):
        print(f'{i}. {card_str_h(deck.cards[i])}')

def card_str_h(card):
    return f'{card.rank.value} {card.suit.value}'

def on_user_created(**kwargs):
    print(f'User name created: {kwargs["username"]}')

def on_room_created(**kwargs):
    print(f'Room created id: {kwargs["room_id"]}')

def on_room_joined(**kwargs):
    print(f'Joined room {kwargs["room_id"]}')

def on_game_started(**kwargs):
    print('Game started, your deck:')
    print_deck(kwargs["deck"])
    print(f'\nCurrent card: {card_str_h(kwargs["current_card"])}')

def on_stack_card(**kwargs):
    print(f'New car from stack: {card_str_h(kwargs["new_card"])}')
    on_turn(**kwargs)

def on_turn(**kwargs):
    print(f'Your turn. Current card: {card_str_h(kwargs["current_card"])}')
    print(f'Your deck:')
    current_deck = kwargs["context"].deck
    print_deck(current_deck)
    card_index = int(input('Enter card to place (or -1 to take from stack): '))
    if card_index >= 0:
        kwargs["context"].make_move(current_deck.cards[card_index])
    else:
        kwargs["context"].take_from_stack()

if __name__ == "__main__":
    import sys
    _, ip, port, user = sys.argv
    with Client(ip, int(port)) as client:
        client.on('user_created', on_user_created)
        client.on('room_created', on_room_created)
        client.on('room_joined', on_room_joined)
        client.on('game_started', on_game_started)
        client.on('your_turn', on_turn)
        client.on('stack_card', on_stack_card)

        client.connect()
        client.register_user(user)

        print("Create or join room?")
        while ( res := input("1. Join Room\n2.Create new room\n") ) not in ["1", "2"]:
            res = '0'
        
        if res == "1":
            room = input("Enter room id: ")
            client.join_room(room)
            print("Waiting for adming to start game...")
            client.listen()
        else:
            rounds = int(input("Enter the number of rounds to play; "))
            client.create_room(rounds)
        
        while ( res := input("Start Game? y/n \n") ) not in ["y"]:
            res = 'x'
        
        client.start_game()
