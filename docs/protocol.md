# Crazy Eights Protocol

Message is defined in two parts:
1. Header: Contains Message type 
2. Body: Contains message data according to the message type

## Format
```
<message type>.<message data>
```

## Received by Server (send by client)

| type           | description                        | value | message body                      |
|----------------|------------------------------------|-------|-----------------------------------|
| EST_CONN       | Establish connection               | 00    |                                   |
| ACK_CONN       | Acknowledge connection             | 01    |                                   |
| NEW_USER       | Create new user                    | 02    | <userid>                          |
| NEW_ROOM       | Create new room                    | 03    | <rounds_n>                        |
| JOIN_ROOM      | Join a room                        | 04    | <userid>,<room_id>                |
| START_GAME     | Start a new game (must be on room) | 05    | <userdi>,<room_id>                |
| GAME_MOVE      | New game move                      | 06    | <room_id>,<card_rank>,<card_suit> |
| GET_CARD_STACK | Get card from the game stack       | 07    | <card_rank>,<card_suit>           |
| CLOSE_ROOM     | Close a room                       | 09    | <userid>,<room_id>                |
| DISCONNECT     | Disconnect from server             | 10    | <userid>                          |

## Received by Client (send by server)

| type          | description                   | value | message body                     |
|---------------|-------------------------------|-------|----------------------------------|
| ACK_CONN      | Acknowledge client connection | 11    |                                  |
| USER_CREATED  | User created                  | 12    | <userid>                         |
| ROOM_CREATED  | Room created                  | 13    | <roomid>                         |
| JOINED_ROOM   | Joined new room               | 14    | <roomid>                         |
| GAME_STARTED  | Started a new game            | 15    | <roomid>,<game_deck>,<stack_card>|
| YOUR_TURN     | New game turn                 | 16    | <card_rank>,<card_suit>          |
| NEW_GAME_MOVE | New game move                 | 17    | <card_rank>,<card_suit>          |
| STACK_CARD    | New card from stack           | 18    | <card_rank>,<card_suit>          |
| GAME_FINISHED | Game finished                 | 20    | <winner_userid>                  |
| ROOM_CLOSED   | Room closed                   | 21    |                                  |
| ROOM_WINNER   | Room Winner                   | 22    | <winner_userid>                  |
| ERROR         | Error                         | 23    | <error_code>,<error_description> |