"""Entry point for banking system"""
from bank_system.banking_system import BankingSystemInterface


def main():
    """Entry point for banking system

     Supplies user input, returns prompts, handles exit condition"""
    banking_system = BankingSystemInterface()
    response = banking_system.start()
    while True:
        user_input = input(response)
        response = banking_system.take_action(user_input)
        if banking_system.state == "off":
            break


if __name__ == "__main__":
    main()
