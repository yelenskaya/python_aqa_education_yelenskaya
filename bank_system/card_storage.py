"""Manages db connection"""
import sqlite3
from datetime import datetime

from bank_system.card import BankingCard


class CardStorage:
    """Card storage in database"""

    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        self._connection = sqlite3.connect("card.s3db")
        self._cursor = self._connection.cursor()
        self._create_card_table()

    def _create_card_table(self):
        """Create card table if not exists"""
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS card(
id INTEGER PRIMARY KEY AUTOINCREMENT,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0,
login_attempts INTEGER DEFAULT O,
last_failed_login TEXT)""")
        self._connection.commit()

    def get_last_id(self):
        """Get last used card id"""
        self._cursor.execute("""SELECT id FROM card ORDER BY id DESC LIMIT 1""")
        result = self._cursor.fetchone()
        self._connection.commit()
        return result[0]

    def does_account_number_exist(self, iin_and_account_number):
        """Check if card with account number exists"""
        self._cursor.execute(
            f"""select 1 from card where number like '{iin_and_account_number}%' """)
        result = self._cursor.fetchone()
        self._connection.commit()
        return result[0] if result else 0

    def does_card_exist(self, card_number):
        """Check if card number exists"""
        self._cursor.execute(f"""select 1 from card where number={card_number}""")
        result = self._cursor.fetchone()
        self._connection.commit()
        return result[0] if result else 0

    def get_card_by_number(self, card_number):
        """Retrieve card by card number"""
        self._cursor.execute(f"select number, pin, balance from card where number={card_number}")
        result = self._cursor.fetchone()
        self._connection.commit()
        return BankingCard(*result)

    def register_card(self, card: BankingCard):
        """Register a card"""
        self._cursor.execute(f"insert into card (number, pin, balance) values("
                             f"{card.card_number}, {card.pin}, {card.balance})")
        self._connection.commit()

    def update_card_balance(self, card_number, sum_to_add):
        """Update card balance"""
        self._cursor.execute(
            f"update card set balance = balance + {sum_to_add} where number = {card_number}")
        self._connection.commit()

    def delete_card_with_number(self, card_number):
        """Delete card with number"""
        self._cursor.execute(f"delete from card where number = {card_number}")
        self._connection.commit()

    def get_number_of_failed_logins(self, card_number):
        """Retrieve number of failed login attempts"""
        self._cursor.execute(f"select login_attempts from card where number = {card_number}")
        result = self._cursor.fetchone()
        self._connection.commit()
        return result[0] if result else 0

    def reset_failed_login_attempts(self, card_number):
        """Reset number of failed login attempts"""
        self._cursor.execute(
            f"update card set login_attempts = 0, "
            f"last_failed_login = null where number = {card_number}")
        self._connection.commit()

    def register_unsuccessful_login_attempt(self, card_number):
        """Register a failed login attempt"""
        now = datetime.now().strftime(self.DATE_TIME_FORMAT)
        self._cursor.execute(
            f"update card set login_attempts = login_attempts + 1,"
            f"last_failed_login = '{now}' where number = {card_number}")
        self._connection.commit()

    def get_last_failed_login_time(self, card_number):
        """Get the last failed login attempt time"""
        self._cursor.execute(f"select last_failed_login from card where number = {card_number}")
        result = self._cursor.fetchone()
        self._connection.commit()
        return datetime.strptime(result[0], self.DATE_TIME_FORMAT) if result[0] else None

    def exit(self):
        """Close db connection"""
        self._connection.close()
