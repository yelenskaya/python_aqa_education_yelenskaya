"""
Custom exceptions for console game
"""


class InvalidActionError(Exception):
    """
    Validation error for main menu error handling
    """

    def __init__(self, message="No such action is supported. Please try again."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class MoveNotValidError(InvalidActionError):
    """
    Validation error for game submenu error handling
    """

    def __init__(self, message="This move is not valid. Please try again"):
        self.message = message
        super().__init__(message)


class StopProgram(Exception):
    """
    Exception to exit the main menu
    """


class StopGame(StopProgram):
    """
    Exception to exit the game menu
    """
