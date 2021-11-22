"""Util functions for a game"""
from tictactoe.game_exceptions import InvalidActionError


def sure_int(user_input):
    """Parse int and wrap the exception into custom one"""
    try:
        return int(user_input)
    except ValueError as error:
        raise InvalidActionError from error
