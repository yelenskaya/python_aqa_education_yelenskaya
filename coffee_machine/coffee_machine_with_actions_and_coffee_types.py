"""
The fourth stage

Describes coffee machine operation, runs coffee machine
"""

from abc import ABC


class Coffee(ABC):
    """
    Abstract class for different coffee types
    """

    def __init__(self, water_amount, coffee_beans_quantity, price, milk_amount=0):
        self.water_amount = water_amount
        self.coffee_beans_quantity = coffee_beans_quantity
        self.milk_amount = milk_amount
        self.price = price


class Espresso(Coffee):
    """
    Describes espresso coffee properties
    """
    NAME = 'espresso'

    def __init__(self):
        super().__init__(water_amount=250, coffee_beans_quantity=16, price=4)


class Latte(Coffee):
    """
    Describes latte coffee properties
    """
    NAME = 'latte'

    def __init__(self):
        super().__init__(water_amount=350, coffee_beans_quantity=20, price=7, milk_amount=75)


class Cappuccino(Coffee):
    """
    Describes cappuccino coffee properties
    """
    NAME = 'cappuccino'

    def __init__(self):
        super().__init__(water_amount=200, coffee_beans_quantity=12, price=6, milk_amount=100)


class NotEnoughResourcesError(Exception):
    """
    Exception for when a user requests more cups
    than the coffee machine can make with available resources
    """

    def __init__(self, message='There is not enough resources for your request'):
        self.message = message

    def __str__(self):
        return self.message


class CoffeeMachine:
    """
    Describes coffee machine operation
    """
    BUY_ACTION = 'buy'
    FILL_ACTION = 'fill'
    TAKE_ACTION = 'take'

    AVAILABLE_ACTIONS = (BUY_ACTION, FILL_ACTION, TAKE_ACTION)

    COFFEE_TYPES = {1: Espresso, 2: Latte, 3: Cappuccino}

    def __init__(self, water_amount, milk_amount,
                 coffee_beans_quantity, disposable_cups, money_amount):
        self.water_amount = water_amount
        self.milk_amount = milk_amount
        self.coffee_beans_quantity = coffee_beans_quantity
        self.disposable_cups = disposable_cups
        self.money_amount = money_amount

    def prepare_coffee(self, coffee: Coffee):
        """
        Calculate changes in resources and in money depending on prepared coffee type
        :param coffee: coffee to prepare
        """
        remaining_water = self.water_amount - coffee.water_amount
        remaining_milk = self.milk_amount - coffee.milk_amount
        remaining_coffee = self.coffee_beans_quantity - coffee.coffee_beans_quantity
        remaining_cups = self.disposable_cups - 1
        if (remaining_water >= 0 and remaining_milk >= 0
                and remaining_coffee >= 0 and remaining_cups >= 0):
            self.water_amount = remaining_water
            self.milk_amount = remaining_milk
            self.disposable_cups = remaining_cups
            self.coffee_beans_quantity = remaining_coffee
            self.money_amount += coffee.price
        else:
            raise NotEnoughResourcesError()

    def calculate_income(self, coffee: Coffee):
        """
        Calculate total money amount after coffee is bought
        :param coffee: coffee to prepare
        """
        self.money_amount += coffee.price

    def fill_resources(self):
        """
        Replenish coffee machine resources based on user input
        """
        self.water_amount += self.ask_for_amount_of_water_to_add()
        self.milk_amount += self.ask_for_amount_of_milk_to_add()
        self.coffee_beans_quantity += self.ask_for_amount_of_coffee_to_add()
        self.disposable_cups += self.ask_for_number_of_cups_to_add()

    def withdraw_money(self):
        """
        Withdraw all the money from coffee machine
        """
        print(f'I gave you {self.money_amount}')
        self.money_amount = 0

    def print_current_state(self):
        """
        Print current state of coffee machine resources
        """
        print(self)

    def __str__(self):
        return f'''The coffee machine has:
{self.water_amount} of water 
{self.milk_amount} of milk 
{self.coffee_beans_quantity} of coffee beans 
{self.disposable_cups} of disposable cups 
{self.money_amount} of money'''

    def operate(self):
        """
        Describes coffee machine operation: prints current state, asks for action to perform
        BUY: prepare coffee of requested coffee type, recalculate resources
        FILL: replenish coffee machine resources
        TAKE: withdraw all the money from coffee machine
        """
        self.print_current_state()

        requested_action = self.validate_action(self.ask_for_action())

        if requested_action == self.BUY_ACTION:
            requested_coffee_type = self.validate_coffee_option(self.ask_for_coffee_type())
            self.prepare_coffee(self.COFFEE_TYPES.get(requested_coffee_type)())
        elif requested_action == self.FILL_ACTION:
            self.fill_resources()
        elif requested_action == self.TAKE_ACTION:
            self.withdraw_money()

        self.print_current_state()

    @classmethod
    def validate_action(cls, action):
        """
        Check if action is available
        :param action: action to check
        :return: action if valid
        """
        if action not in cls.AVAILABLE_ACTIONS:
            raise ValueError("No such action is supported")
        return action

    @classmethod
    def validate_coffee_option(cls, option):
        """
        Check if coffee option is available
        :param option to check
        :return: option if valid
        """
        if option not in cls.COFFEE_TYPES:
            raise ValueError("No such coffee option")
        return option

    @classmethod
    def ask_for_action(cls):
        """
        Ask user input for action to perform
        """
        return input(f"Write action ({', '.join(cls.AVAILABLE_ACTIONS)}): \n")

    @classmethod
    def list_coffee_options(cls):
        """
        Constructs a numbered list of coffee options based on coffee types
        :return: list of coffee options as a string
        """
        return ', '.join(
            [f'{index} - {coffee_type.NAME}' for index, coffee_type in cls.COFFEE_TYPES.items()])

    @classmethod
    def ask_for_coffee_type(cls):
        """
        Ask user input for coffee type to prepare
        """
        return int(
            input(f'What do you want to buy? {cls.list_coffee_options()}\n'))

    @classmethod
    def ask_for_amount_of_water_to_add(cls):
        """
        Ask user input on amount of water to refill
        """
        return int(input('Write how many ml of water you want to add:\n'))

    @classmethod
    def ask_for_amount_of_milk_to_add(cls):
        """
        Ask user input on amount of milk to refill
        """
        return int(input('Write how many ml of milk you want to add:\n'))

    @classmethod
    def ask_for_amount_of_coffee_to_add(cls):
        """
        Ask user input on amount of coffee beans to refill
        """
        return int(input('Write how many grams of coffee beans you want to add:\n'))

    @classmethod
    def ask_for_number_of_cups_to_add(cls):
        """
        Ask user input on number of cups to refill
        """
        return int(input('Write how many disposable coffee cups you want to add:\n'))


coffee_machine = CoffeeMachine(water_amount=400, milk_amount=540,
                               coffee_beans_quantity=120, disposable_cups=9, money_amount=550)
coffee_machine.operate()
