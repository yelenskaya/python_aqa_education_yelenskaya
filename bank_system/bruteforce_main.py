"""Alternated main cycle with bruteforce attacker supplying the inputs"""

import re

from bank_system.banking_system import BankingSystemInterface
from bank_system.card import BankingCard


def generate_card_number():
    """Generate card number using the known bank iin"""
    bank_iin = "400000"
    for num in range(0, 200):
        yield bank_iin + str(num).zfill(10)


def generate_pin():
    """Generate pin"""
    for num in range(0, 10000):
        yield str(num).zfill(4)


def print_return(func):
    """Decorator to print return value before doing the return"""
    def inner(*args):
        output = func(*args)
        print(output)
        return output
    return inner


class Bruteforce:
    """Encapsulates bruteforce logic"""
    BRUTEFORCER_CARD = BankingCard("4000000089270310", "3828")

    def __init__(self):
        self._valid_card = ""
        self._valid_pin = ""

        self._processing_card = ""
        self._processing_pin = ""

        self._balance = ""

        self._card_generator = generate_card_number()
        self._pin_generator = generate_pin()

    def _get_card(self):
        """Determine if valid card is saved, if not, generate a card number to try"""
        if self._valid_card:
            return self._valid_card

        self._processing_card = next(self._card_generator)
        print(self._processing_card)
        return self._processing_card

    @staticmethod
    def _get_balance(balance_message):
        """Parse balance sum"""
        return re.search("Balance: (\\d+)", balance_message).group(1)

    @print_return
    def generate_input(self, response):
        """Generate input to get into account and transfer money out"""
        print(response)
        if "Log into account" in response:
            return "2"
        if "Enter your card number:" in response:
            return self._get_card()
        if "Enter your PIN:" in response:
            # Therefore card is valid
            self._valid_card = self._processing_card
            self._processing_pin = next(self._pin_generator)
            return self._processing_pin
        if "1. Balance" in response and "Balance:" not in response and "Success!" not in response:
            # Therefore pin is valid
            self._valid_pin = self._processing_pin
            return "1"
        if "Balance:" in response:
            self._balance = self._get_balance(response)
            return "3"
        if "Enter card number:" in response:
            return self.BRUTEFORCER_CARD.card_number
        if "Enter how much money you want to transfer:" in response:
            return self._balance
        if "Success!" in response:
            return "0"


def main():
    """Main cycle with bruteforce attacker supplying the input"""
    b_f = Bruteforce()
    banking_system = BankingSystemInterface()
    response = banking_system.start()
    while True:
        user_input = b_f.generate_input(response)
        response = banking_system.take_action(user_input)
        if banking_system.state == "off":
            break


if __name__ == "__main__":
    main()
