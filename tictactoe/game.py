"""
Main game entry point and menu
"""

from collections import namedtuple

from tictactoe.game_exceptions import InvalidActionError, StopProgram
from tictactoe.log_manager import GameLogging
from tictactoe.tictactoe_interface import TicTacToeInterface
from tictactoe.utils import sure_int


class Menu:
    """
    Game menu
    """
    _PLAY = "play"
    _SHOW_LOG = "show log"
    _CLEAR_LOG = "clear log"
    _EXIT = "exit"

    def __init__(self, game_interface, game_logging):
        self._game_interface = game_interface
        self._game_logging = game_logging

        Action = namedtuple("Action", "name, instruction")
        self._actions = {1: Action(self._PLAY, self._game_interface.play_game),
                         2: Action(self._SHOW_LOG, self._game_logging.show_logs),
                         3: Action(self._CLEAR_LOG, self._game_logging.clear_logs),
                         4: Action(self._EXIT, None)}

    def _list_actions(self):
        """Return formatted string for all available actions"""
        return ", ".join([f"{action.name} - {index}" for index, action in self._actions.items()])

    def _validate_action(self, action_input):
        """Validate if action is supported"""
        if action_input not in self._actions:
            raise InvalidActionError

    def describe_actions(self):
        """Construct description of available actions"""
        return f"Please select an action: {self._list_actions()}\n"

    def evaluate_action(self, action_input):
        """Route program flow to submenus or close program"""
        action_input = sure_int(action_input)
        self._validate_action(action_input)

        if self._actions.get(action_input).name == self._EXIT:
            raise StopProgram

        return self._actions.get(action_input).instruction

    def welcome(self):
        """Generate welcome string for a specific game"""
        print(f"Welcome to {self._game_interface.game_name} game!\n")


def main():
    """
    Main game entry point. Responsible for supplying user input.

    User chooses the action from main menu and proceeds to submenu choices.
    If submenu returns the next prompt, the program remains in the submenu.
    If submenu does not return a prompt, the user is returned back to the main menu.
    """
    # Initialize
    game_logging = GameLogging()
    menu = Menu(TicTacToeInterface(game_logging.logger), game_logging)

    # Print welcome message
    menu.welcome()

    while True:
        # Main menu interaction
        try:
            # Try to get next instruction
            requested_action = input(menu.describe_actions())
            instruction = menu.evaluate_action(requested_action)

        # Validation
        except InvalidActionError as error:
            print(error)
            continue

        # Exit condition
        except StopProgram:
            break

        # If instruction exists and is valid, proceed to submenu interaction
        else:
            user_input = ""
            while True:
                try:
                    # In case user input is present - pass it to submenu
                    if user_input:
                        next_prompt = instruction(user_input=user_input)
                    else:
                        next_prompt = instruction()

                    # Retry instruction if case of not valid action
                except InvalidActionError as error:
                    print(error)
                    user_input = ""
                    continue
                except StopProgram:
                    break

                # If there is a next prompt, pass it to user
                if next_prompt:
                    user_input = input(next_prompt)

                # Otherwise exit submenu
                else:
                    break


if __name__ == "__main__":
    main()
