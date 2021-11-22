"""
Timer decorator
"""
import time

START_TIME = None


def timer(logger_attribute_name):
    """
    Decorator for measuring the total time between the first fun of the function
    until the function returns True, signalizing that the game is over
    :param logger_attribute_name: name of class instance variable where a logger is stored
    """
    def record_time(func):
        def inner(*args):

            global START_TIME
            if not START_TIME:
                START_TIME = time.time()

            game_over = func(*args)

            if game_over:
                end_time = time.time()

                logger = getattr(args[0], logger_attribute_name)
                if logger:
                    logger.info(f"Game took {end_time - START_TIME:.2f} seconds")

                # Reset
                START_TIME = None

        return inner

    return record_time
