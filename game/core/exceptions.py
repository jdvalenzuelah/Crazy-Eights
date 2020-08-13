class NoPlayersException(Exception):
    pass

class NotYourTurnException(Exception):
    pass

class InvalidMoveException(Exception):
    pass

class CardNotOnDeckException(Exception):
    pass

class WaitingForSuitChangeException(Exception):
    pass

class NotWaitingForSuitChangeException(Exception):
    pass

class InvalidNumberOfPlayersException(Exception):
    pass

class UserNameAlreadyTakenException(Exception):
    pass

class GameAlreadyFinishedException(Exception):
    pass

class InvalidUserNameException(Exception):
    pass

class RoomAlreadyFull(Exception):
    pass

class NotEnoughPlayerException(Exception):
    pass

class GameAlreadyOnCourseException(Exception):
    pass

class RoomRoundsAlreadyCompletedException(Exception):
    pass