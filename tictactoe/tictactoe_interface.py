"""
Tic tac toe game submenu and user interface
"""
from collections import deque
from enum import Enum

from texttable import Texttable

from tictactoe import utils
from tictactoe.game_exceptions import MoveNotValidError, StopGame
from tictactoe.game_timer import timer
from tictactoe.tictactoe_logic import TicTacToe


class TicTacToeStage(Enum):
    """
    Tic tac toe game states with regards to the user input
    """
    SELECT_PLAYERS = 1
    ASK_FOR_MOVE = 2
    ASK_FOR_REMATCH = 3


class TicTacToeInterface:
    """
    Tic tac toe game submenu
    """
    _PLAYER_FIGURES = {1: "X", 2: "O"}

    def __init__(self, logger):
        self.game_name = "Tic Tac Toe"
        self._logger = logger
        self._tictactoe = TicTacToe()

        self._stage = TicTacToeStage.SELECT_PLAYERS

        self._players = deque(maxlen=2)

        self._current_player = None
        self._retry_move = False
        self._game_over = False
        self._rematch = True

    def _process_matrix_for_printing(self):
        """
        Renders Tic tac toe table
        """
        table = Texttable()
        table.set_chars(['-', '|', '+', '-'])
        table.set_cols_align(["c"] * len(self._tictactoe.matrix[0]))
        table.set_cols_valign(["m"] * len(self._tictactoe.matrix[0]))
        table.add_rows(self._tictactoe.matrix)
        print(table.draw())

    def _log_victory(self, current_player):
        """Logs victory"""
        self._logger.info(f"{current_player.name} has won")

    def _log_draw(self):
        """Logs draw"""
        self._logger.info("Draw. The game is over")

    def _get_new_player_number(self):
        """Determine the player's ordinal number"""
        return len(self._players) + 1

    def _ask_for_player(self):
        """Return prompt to ask for the player's username"""
        player_number = self._get_new_player_number()
        return f"Name {player_number} player " \
               f"- to play with {self._PLAYER_FIGURES.get(player_number)}\n"

    def _players_ready(self):
        """Check if there is a required number of registered players"""
        return len(self._players) == 2

    def _register_player(self, user_input):
        """Store the player's username and an assigned game figure for further use in the game"""
        player_number = self._get_new_player_number()
        self._players.append(Player(user_input, self._PLAYER_FIGURES.get(player_number)))

    def _get_other_player(self, player_to_exclude):
        """Get another player to enable playing by turns"""
        return next(player for player in self._players if player.name != player_to_exclude.name)

    def _reset_players(self):
        """Clear players' storage"""
        self._players.clear()

    def _handle_rematch_input(self, user_input):
        """Handles response to y/n question"""
        self._rematch = user_input == "y"

    @staticmethod
    def _ask_for_rematch():
        """Generate a prompt for a rematch"""
        return "Wanna rematch? y/n\n"

    def _ask_for_move(self):
        """Generate a prompt for a next move"""
        return f"{self._current_player.name}, please make a move, i.e. A1\n"

    def _handle_move_input(self, move):
        """Validate move user input"""
        try:
            x_axis, y_axis = move
            y_axis = utils.sure_int(y_axis)
            self._tictactoe.validate_move_to_cell(x_axis, y_axis)

            # Reset retry if was present, as the value is now valid
            self._retry_move = False
        except ValueError as error:
            self._retry_move = True
            raise MoveNotValidError from error
        except MoveNotValidError as error:
            self._retry_move = True
            raise MoveNotValidError from error
        return x_axis, y_axis

    def _make_a_move(self, move):
        """Sets user move to tic tac toe table, renders the table, ascertains and logs the result"""
        x_axis, y_axis = move

        self._tictactoe.set_cell_value(x_axis, y_axis, self._current_player.figure)
        self._process_matrix_for_printing()
        game_over = self._tictactoe.check_matrix_for_win()

        if game_over:
            self._log_victory(self._current_player)
        else:
            game_over = self._tictactoe.is_matrix_filled()
            if game_over:
                self._log_draw()

        return game_over

    @timer(logger_attribute_name="_logger")
    def _continue_game(self, current_move):
        """
        Manages the move

        Validates the move, determines whether this is a retry of invalid move,
        switches players, resets resources
        """
        # If there is a new input
        if current_move:
            # Validate move
            current_move = self._handle_move_input(current_move)
            # Make a move and ascertain if anyone has won
            self._game_over = self._make_a_move(current_move)

        # If there is no new input and it is not a retry
        elif not self._retry_move:
            # First print
            self._process_matrix_for_printing()

        # If this is not a retry, determine next player
        if not self._retry_move:
            # If somebody had already made a move, take the other player
            if self._current_player:
                self._current_player = self._get_other_player(self._current_player)
            # Otherwise take first player
            else:
                self._current_player = self._players[0]

        # Clear the table if the game is done
        if self._game_over:
            self._tictactoe.reset_matrix()

            # Clear players if there is surely not going to be a rematch
            if not self._rematch:
                self._reset_players()

        return self._game_over

    def play_game(self, **kwargs):
        """
        Handles Tic Tac Toe submenu, stores the information between the stages,
        routes the flow depending on the user input
        """
        user_input = kwargs.get("user_input")

        # Add players
        if self._stage == TicTacToeStage.SELECT_PLAYERS:
            # Add new player with a name if there are some user input
            if user_input:
                self._register_player(user_input)

            # If there are already 2 players - go to next stage
            if self._players_ready():
                user_input = ""
                self._stage = TicTacToeStage.ASK_FOR_MOVE

            # Otherwise ask for a player name
            else:
                return self._ask_for_player()

        # Play game
        if self._stage == TicTacToeStage.ASK_FOR_MOVE:
            # Determine current player, perform move and acknowledge the result
            self._continue_game(user_input)

            # If game is done  - go to next stage
            if self._game_over:
                user_input = ""
                self._stage = TicTacToeStage.ASK_FOR_REMATCH

            # If not - ask for another move
            else:
                return self._ask_for_move()

        # Stage to ask for a rematch
        if self._stage == TicTacToeStage.ASK_FOR_REMATCH:
            # Ask for a rematch
            if not user_input:
                return self._ask_for_rematch()

            # If there is already input for this stage,
            # validate and store result to instance variable
            self._handle_rematch_input(user_input)

            # If rematch is not cancelled, switch to asking for move
            if self._rematch:
                user_input = ""
                self._stage = TicTacToeStage.ASK_FOR_MOVE
                # Reset state
                self._rematch = True
                self._game_over = False
                # Initiate game
                self._continue_game(user_input)
                return self._ask_for_move()

            # If a user decided for no rematch - return to main menu
            # Reset state
            self._game_over = False
            raise StopGame


class Player:
    """Tic tac toe player model"""
    def __init__(self, name, figure):
        self.name = name
        self.figure = figure

    def __str__(self):
        return f"{self.name}, plays {self.figure}"
