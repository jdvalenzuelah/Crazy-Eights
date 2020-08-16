class GameException(Exception):
    code = '-1'

class NoPlayersException(GameException):
    code = '00'

class NotYourTurnException(GameException):
    code = '01'

class InvalidMoveException(GameException):
    code = '02'

class CardNotOnDeckException(GameException):
    code = '03'

class WaitingForSuitChangeException(GameException):
    code = '04'

class NotWaitingForSuitChangeException(GameException):
    code = '05'

class InvalidNumberOfPlayersException(GameException):
    code = '06' 

class UserNameAlreadyTakenException(GameException):
    code = '07'

class GameAlreadyFinishedException(GameException):
    code = '08'

class InvalidUserNameException(GameException):
    code = '09'

class RoomAlreadyFull(GameException):
    code = '10'

class NotEnoughPlayerException(GameException):
    code = '11'

class GameAlreadyOnCourseException(GameException):
    code = '12'

class RoomRoundsAlreadyCompletedException(GameException):
    code = '13'

class RoomRoundsNotCompleted(GameException):
    code = '14'