"""
Banking system module

Contains bank interface and business logic
"""
import datetime
from enum import Enum, auto, IntEnum
from random import randint

from bank_system.card import BankingCard
from bank_system.card_storage import CardStorage
from bank_system.utils import get_list_of_digits, sum_digits


class LoginStates(Enum):
    """
    Stages of bank authorization
    """
    INITIAL = auto()
    FILLING_CARD = auto()
    FILLING_PIN = auto()


class AddIncomeStates(Enum):
    """
    Stages of topping up the card
    """
    INITIAL = auto()
    FILLING_INCOME = auto()


class TransferMoneyStates(Enum):
    """
    Stages of transferring money
    """
    INITIAL = auto()
    FILLING_CARD = auto()
    FILLING_SUM = auto()


class MenuStates(Enum):
    """
    Console menu states
    """
    MAIN_MENU = auto()
    CARD_MENU = auto()
    LOGGING_IN = auto()
    ADDING_INCOME = auto()
    TRANSFERRING_MONEY = auto()


class MainMenuOptions(IntEnum):
    """
    Main menu options
    """
    CREATE_ACCOUNT = 1
    LOG_IN = 2
    EXIT = 0


class CardMenuOptions(IntEnum):
    """
    Authorized user's menu options
    """
    BALANCE = 1
    ADD_INCOME = 2
    DO_TRANSFER = 3
    CLOSE_ACCOUNT = 4
    LOGOUT = 5
    EXIT = 0


class BankingSystemInterface:
    """
    Console interface for banking system
    """
    _MAIN_MENU_TEXT = """1. Create an account
2. Log into account
0. Exit
"""
    _CARD_MENU_TEXT = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""
    _WRONG_INPUT = "Input is incorrect. Please try again.\n"
    _EXIT_MESSAGE = "Bye!\n"

    def __init__(self):
        self._bank = Bank(CardStorage())

        self.state = "on"
        self._menu = MenuStates.MAIN_MENU
        self._authorization_stage = LoginStates.INITIAL
        self._add_income_stage = AddIncomeStates.INITIAL
        self._transfer_money_stage = TransferMoneyStates.INITIAL

        self._pending_transfer_to_card_number = None

    def start(self):
        """Print main menu"""
        return self._MAIN_MENU_TEXT

    def take_action(self, action):
        """Initial input validation and evaluation"""
        if self._check_user_input(action):
            return self._evaluate_action(action)
        return self._WRONG_INPUT

    def _check_user_input(self, action):
        """Validate input for the specific menu"""
        if self._menu == MenuStates.MAIN_MENU:
            return action.isdigit() and int(action) in range(0, 3)
        if self._menu == MenuStates.CARD_MENU:
            return action.isdigit() and int(action) in range(0, 6)
        if self._menu == MenuStates.LOGGING_IN or self._menu == MenuStates.ADDING_INCOME:
            return action.isdigit()
        return True

    def _evaluate_action(self, action):
        """Route user input to menu handlers"""
        if self._menu == MenuStates.MAIN_MENU:
            return self._handle_main_menu(int(action))
        if self._menu == MenuStates.LOGGING_IN:
            return self._handle_main_menu(action)
        if self._menu == MenuStates.CARD_MENU \
                or self._menu == MenuStates.ADDING_INCOME \
                or self._menu == MenuStates.TRANSFERRING_MONEY:
            return self._handle_card_menu(int(action))

    def _handle_main_menu(self, action):
        """Main menu handler"""
        if action == MainMenuOptions.CREATE_ACCOUNT:
            self._create_account()
            return self._MAIN_MENU_TEXT
        if action == MainMenuOptions.LOG_IN or self._authorization_stage != LoginStates.INITIAL:
            self._menu = MenuStates.LOGGING_IN
            return self._log_into_account(action)
        if action == MainMenuOptions.EXIT:
            return self._exit()

    def _exit(self):
        """Free resources and set state to 'off'"""
        self._bank.exit()
        self.state = "off"
        print(self._EXIT_MESSAGE)

    def _switch_to_main_menu(self, before_menu=""):
        """Reset state and return to main menu"""
        self._authorization_stage = LoginStates.INITIAL
        self._menu = MenuStates.MAIN_MENU
        return "\n".join([before_menu, self._MAIN_MENU_TEXT])

    def _switch_to_card_menu(self, before_menu=""):
        """Return to authorized user's menu"""
        self._menu = MenuStates.CARD_MENU
        return "\n".join([before_menu, self._CARD_MENU_TEXT])

    def _handle_card_menu(self, action):
        """Authorized user's menu handler"""
        if action == CardMenuOptions.BALANCE:
            return self._switch_to_card_menu(self._print_balance())
        if action == CardMenuOptions.ADD_INCOME or self._menu == MenuStates.ADDING_INCOME:
            self._menu = MenuStates.ADDING_INCOME
            return self._add_income(action)
        if action == CardMenuOptions.DO_TRANSFER or self._menu == MenuStates.TRANSFERRING_MONEY:
            self._menu = MenuStates.TRANSFERRING_MONEY
            return self._do_transfer(action)
        if action == CardMenuOptions.CLOSE_ACCOUNT:
            self._close_account()
            return self._switch_to_main_menu()
        if action == CardMenuOptions.LOGOUT:
            self._logout()
            return self._switch_to_main_menu()
        if action == CardMenuOptions.EXIT:
            return self._exit()

    def _create_account(self):
        """Initiate creating an account, print result"""
        bank_card = self._bank.issue_new_card()
        print(f"""Your card has been created
Your card number:
{bank_card.card_number}
Your card PIN:
{bank_card.pin}\n""")

    def _log_into_account(self, user_input):
        """Authorization process"""
        # If user has not started login process, ask for card number
        if self._authorization_stage == LoginStates.INITIAL:
            self._authorization_stage = LoginStates.FILLING_CARD
            return self._ask_for_card_number()

        # After asking for card, save card number and ask for pin
        if self._authorization_stage == LoginStates.FILLING_CARD:
            return self._handle_card_number(user_input)

        # Attempt authorization
        if self._authorization_stage == LoginStates.FILLING_PIN:
            # Reset authorization process in any case
            self._authorization_stage = LoginStates.INITIAL

            authorized = self._bank.authorize_access(user_input)
            return self._handle_authorization_result(authorized)

    def _handle_card_number(self, card_number):
        """Validate card for authorization"""
        # Check if card is registered, if yes, validate login attempts
        if self._bank.does_card_exist(card_number):
            # If there are not many failed login attempts, ask for pin
            if self._bank.validate_login_attempts_on_card(card_number):
                self._authorization_stage = LoginStates.FILLING_PIN
                self._bank.current_user_card_number = card_number
                return self._ask_for_pin()
            # If there were too many failed login attempts, return to main menu
            return self._switch_to_main_menu(self._print_too_many_login_attempts())

        # If no such card, return to main menu
        return self._switch_to_main_menu(self._print_non_existing_card())

    def _handle_authorization_result(self, success):
        """Route a user after authorization attempt"""
        # If login ok - proceed to card menu
        if success:
            # Get and save card
            return self._switch_to_card_menu(self._print_login_success())

        # If not - return back to main menu
        return self._switch_to_main_menu(self._print_login_failure())

    def _print_balance(self):
        """Return current user card balance"""
        return f"Balance: {self._bank.get_current_card_balance()}\n"

    def _add_income(self, user_input):
        """Top up a card"""
        # Ask for income first
        if self._add_income_stage == AddIncomeStates.INITIAL:
            self._add_income_stage = AddIncomeStates.FILLING_INCOME
            return self._ask_for_income_sum()

        # Save income and print success
        if self._add_income_stage == AddIncomeStates.FILLING_INCOME:
            self._bank.add_money_to_current_card(int(user_input))

            # Reset state
            self._add_income_stage = AddIncomeStates.INITIAL
            return self._switch_to_card_menu(self._print_add_income_success())

    def _do_transfer(self, user_input):
        """Transfer money from a card"""
        # Ask for target card first
        if self._transfer_money_stage == TransferMoneyStates.INITIAL:
            self._print_start_of_transfer()
            self._transfer_money_stage = TransferMoneyStates.FILLING_CARD
            return self._ask_for_target_card_number()

        # Validate and save the card, ask for sum
        if self._transfer_money_stage == TransferMoneyStates.FILLING_CARD:
            return self._handle_target_card(user_input)

        # Validate the sum and perform transfer
        if self._transfer_money_stage == TransferMoneyStates.FILLING_SUM:
            return self._handle_transfer_sum(user_input)

    def _handle_target_card(self, target_card_number):
        """Validate target card and ask for transfer sum"""
        target_card_number = str(target_card_number)

        # If card number if valid, proceed
        if self._bank.validate_card_number_luhn(target_card_number):
            # If card number is not a current card number, proceed
            if self._bank.current_user_card_number != target_card_number:

                # If card exists, ask for sum
                if self._bank.does_card_exist(target_card_number):
                    self._transfer_money_stage = TransferMoneyStates.FILLING_SUM
                    self._pending_transfer_to_card_number = target_card_number
                    return self._ask_for_transfer_sum()

                # If card does not exist, print failure
                self._print_card_does_not_exist()
            else:
                # If target card number is same as current, print failure
                self._print_same_account_transfer_error()
        else:
            # If card number is invalid, print failure
            self._print_invalid_card_number()

        # Reset state in case card is invalid
        self._transfer_money_stage = TransferMoneyStates.INITIAL
        return self._switch_to_card_menu()

    def _handle_transfer_sum(self, transfer_sum):
        """Validate transfer sum and perform transfer"""
        # If there is enough money, transfer money, reset state
        if self._bank.get_current_card_balance() >= transfer_sum:
            self._bank.transfer_money_from_current_card_to_target(
                self._pending_transfer_to_card_number, transfer_sum)
            result_message = self._print_success()
        # If there is not enough money, print failure
        else:
            result_message = self._print_not_enough_money()

        # Reset state
        self._pending_transfer_to_card_number = None
        self._transfer_money_stage = TransferMoneyStates.INITIAL
        return self._switch_to_card_menu(result_message)

    def _close_account(self):
        """Delete card from the system"""
        self._bank.close_current_account()
        self._print_account_is_closed()
        return self._switch_to_main_menu()

    def _logout(self):
        """Logout by a current user"""
        self._bank.current_user_card_number = None
        print("You have successfully logged out!\n")

    @staticmethod
    def _ask_for_card_number():
        """Ask for a card to authorize"""
        return "Enter your card number:\n"

    @staticmethod
    def _ask_for_pin():
        """Ask for a pin to authorize"""
        return "Enter your PIN:\n"

    @staticmethod
    def _print_login_success():
        """Authorization success"""
        return "You have successfully logged in!\n"

    @staticmethod
    def _print_non_existing_card():
        """Card does not exist error"""
        return "Wrong card number!\n"

    @staticmethod
    def _print_too_many_login_attempts():
        """Bruteforce defence"""
        return "There were too many failed login attempts. Card is blocked for one hour\n"

    @staticmethod
    def _print_login_failure():
        """Pin is incorrect error"""
        return "Wrong PIN!\n"

    @staticmethod
    def _ask_for_income_sum():
        """Ask for a sum to add to the card"""
        return "Enter income:\n"

    @staticmethod
    def _print_add_income_success():
        """Top up success"""
        return "Income was added!\n"

    @staticmethod
    def _print_start_of_transfer():
        """Start of transfer"""
        print("Transfer")

    @staticmethod
    def _ask_for_target_card_number():
        """Ask for a target card"""
        return "Enter card number:\n"

    @staticmethod
    def _ask_for_transfer_sum():
        """Ask for a transfer sum"""
        return "Enter how much money you want to transfer:\n"

    @staticmethod
    def _print_success():
        """Report success"""
        return "Success!\n"

    @staticmethod
    def _print_invalid_card_number():
        """Card validation error by Luhn's algorithm"""
        print("Probably you made a mistake in the card number. Please try again!\n")

    @staticmethod
    def _print_card_does_not_exist():
        """Card validation error - non existent card"""
        print("Such a card does not exist.\n")

    @staticmethod
    def _print_same_account_transfer_error():
        """Card validation error - same card"""
        print("You can't transfer money to the same account!\n")

    @staticmethod
    def _print_not_enough_money():
        """Transfer sum validation error"""
        return "Not enough money!\n"

    @staticmethod
    def _print_account_is_closed():
        """Report success for closing account"""
        print("The account has been closed!\n")


class Bank:
    """Bank business logic"""
    _BANK_IIN = "400000"

    def __init__(self, card_storage):
        self._card_storage = card_storage

        self.current_user_card_number = None

    def issue_new_card(self):
        """Issue a card"""
        account_number = self._generate_account_identifier()
        card_number = self._generate_card_number(self._BANK_IIN, account_number)
        pin = self._generate_pin()

        bank_card = BankingCard(card_number, pin)

        self._card_storage.register_card(bank_card)
        return bank_card

    def _generate_account_identifier(self):
        """Generate a unique account number"""
        is_not_unique = True
        while is_not_unique:
            account_number = str(self._card_storage.get_last_id() +
                                 1 + randint(0, 9999999)).zfill(9)
            is_not_unique = self._card_storage.does_account_number_exist(
                self._BANK_IIN + account_number)
        return account_number

    @staticmethod
    def _generate_pin():
        """Generate a pin"""
        return str(randint(1000, 9999))

    @classmethod
    def _generate_card_number(cls, iin, account_number):
        """Generate a checksum using Luhn's algorithm, construct a card number"""
        # Construct a card number with random checksum
        initial_card_number = iin + account_number + str(randint(0, 9))

        # Get list of digits
        card_number_as_list = get_list_of_digits(initial_card_number)

        # Replace random checksum with correct one using Luhn's algorithm
        card_number_as_list[-1] = cls._calculate_checksum_luhn(card_number_as_list)

        return "".join(str(num) for num in card_number_as_list)

    @staticmethod
    def _calculate_checksum_luhn(card_number_as_list):
        """Calculate a checksum using Luhn's algorithm"""
        # Luhn's algorithm
        # Get every other number from left to right
        reversed_every_other_number = card_number_as_list[-2::-2]

        # Double extracted numbers, store the doubled number if it is less than 10,
        # sum the digits of the retrieved number otherwise
        doubled_numbers_sum = sum(
            [num * 2 if num * 2 < 10 else sum_digits(num * 2)
             for num in reversed_every_other_number])

        # Sum other numbers except the fake last checksum
        other_numbers_sum = sum(card_number_as_list[-3::-2])

        # Get total sum
        total_sum = doubled_numbers_sum + other_numbers_sum

        # Get such x so that (total_sum + x) % 10 == 0
        return (total_sum * 9) % 10

    @classmethod
    def validate_card_number_luhn(cls, card_number):
        """Validate a checksum using Luhn's algorithm"""
        # Get list of digits
        card_number_as_list = get_list_of_digits(card_number)
        # Validate checksum against correct Luhn's checksum
        return card_number_as_list[-1] == cls._calculate_checksum_luhn(card_number_as_list)

    def validate_login_attempts_on_card(self, card_number):
        """Check if there is less than 3 failed login attempts
        or enough time has passed to unblock the card"""
        failed_logins = self._card_storage.get_number_of_failed_logins(card_number)
        return failed_logins < 3 or self._enough_time_since_failed_login(card_number)

    def _enough_time_since_failed_login(self, card_number):
        """Check if enough time has passed to unblock the card"""
        last_failed_attempt = self._card_storage.get_last_failed_login_time(card_number)
        return last_failed_attempt + datetime.timedelta(
            hours=1) < datetime.datetime.now() if last_failed_attempt else True

    def _is_pin_correct(self, card_number, pin):
        """Check if pin correct"""
        return self._card_storage.get_card_by_number(card_number).pin == pin

    def authorize_access(self, pin):
        """Authorize access if card exists and pin is correct,
        else register a failed login attempt"""

        is_pin_correct = self._is_pin_correct(self.current_user_card_number, pin)
        if is_pin_correct:
            self._card_storage.reset_failed_login_attempts(self.current_user_card_number)

        else:
            self._card_storage.register_unsuccessful_login_attempt(self.current_user_card_number)
        return is_pin_correct

    def get_current_card_balance(self):
        """Return current card balance"""
        return self._card_storage.get_card_by_number(self.current_user_card_number).balance

    def does_account_number_exist(self, iin_and_account_number):
        """Check if account number is registered"""
        return self._card_storage.does_account_number_exist(iin_and_account_number)

    def does_card_exist(self, card_number):
        """Check if card exists"""
        return self._card_storage.does_card_exist(card_number)

    def add_money_to_current_card(self, sum_to_add):
        """Top up the card"""
        self._card_storage.update_card_balance(self.current_user_card_number, sum_to_add)

    def transfer_money_from_current_card_to_target(self, target_card_number, transfer_sum):
        """Transfer money"""
        self._card_storage.update_card_balance(self.current_user_card_number, -transfer_sum)
        self._card_storage.update_card_balance(target_card_number, transfer_sum)

    def close_current_account(self):
        """Close current account"""
        self._card_storage.delete_card_with_number(self.current_user_card_number)
        self.current_user_card_number = None

    def exit(self):
        """Free resources and exit"""
        self._card_storage.exit()
