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