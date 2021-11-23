"""Banking card module"""


class BankingCard:
    """Banking card model"""

    def __init__(self, card_number, pin, balance=0):
        self.card_number = card_number
        self.pin = pin
        self.balance = balance
