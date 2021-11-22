"""
Log manager for a game
"""

import logging
import sys


class GameLogging:
    """
    Stores a preconfigured logger, can access and manage log records
    """

    def __init__(self, file_name="game.log"):
        self._file_name = file_name

        game_logger = logging.getLogger()
        game_logger.setLevel(logging.INFO)

        log_format = logging.Formatter(fmt="%(asctime)s - %(message)s",
                                       datefmt="%d.%m.%Y %H:%M")

        file_handler = logging.FileHandler(self._file_name)
        file_handler.setFormatter(log_format)
        game_logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        game_logger.addHandler(console_handler)

        self.logger = game_logger

    def show_logs(self):
        """
        Print all logs from the file
        """
        with open(self._file_name) as log:
            print(log.read())

    def clear_logs(self):
        """
        Clear logs from the file
        """
        with open(self._file_name, "w"):
            print("Log file is cleared")
