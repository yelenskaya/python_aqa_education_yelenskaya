"""
The fifth stage

Describes coffee machine operation, runs coffee machine
"""


class CoffeeRecipe:
    """
    Class describing coffee recipe
    """

    def __init__(self, name, water_amount, coffee_beans_quantity, price, milk_amount=0):
        self.name = name
        self.water_amount = water_amount
        self.coffee_beans_quantity = coffee_beans_quantity
        self.milk_amount = milk_amount
        self.price = price


class CoffeeMachine:
    """
    Describes coffee machine operation
    """
    BUY_ACTION = 'buy'
    FILL_ACTION = 'fill'
    TAKE_ACTION = 'take'
    REMAINING_ACTION = 'remaining'
    EXIT_ACTION = 'exit'
    BACK_ACTION = 'back'

    AVAILABLE_TOP_LEVEL_ACTIONS = (BUY_ACTION, FILL_ACTION,
                                   TAKE_ACTION, REMAINING_ACTION, EXIT_ACTION)

    ESPRESSO = CoffeeRecipe(name='espresso',
                            water_amount=250,
                            coffee_beans_quantity=16,
                            price=4)
    LATTE = CoffeeRecipe(name='latte',
                         water_amount=350,
                         coffee_beans_quantity=20,
                         price=7,
                         milk_amount=75)
    CAPPUCCINO = CoffeeRecipe(name='cappuccino',
                              water_amount=200,
                              coffee_beans_quantity=12,
                              price=6,
                              milk_amount=100)

    COFFEE_TYPES = {1: ESPRESSO, 2: LATTE, 3: CAPPUCCINO}

    def __init__(self, water_amount, milk_amount,
                 coffee_beans_quantity, disposable_cups, money_amount):
        self.water_amount = water_amount
        self.milk_amount = milk_amount
        self.coffee_beans_quantity = coffee_beans_quantity
        self.disposable_cups = disposable_cups
        self.money_amount = money_amount

    def prepare_coffee(self, coffee: CoffeeRecipe):
        """
        Prepares coffee, calculate changes in resources and in money
        depending on prepared coffee type
        :param coffee: coffee to prepare
        """

        # Determine if there are enough resources
        remaining_water = self.water_amount - coffee.water_amount
        remaining_milk = self.milk_amount - coffee.milk_amount
        remaining_coffee = self.coffee_beans_quantity - coffee.coffee_beans_quantity
        remaining_cups = self.disposable_cups - 1

        # If yes - print success, subtract expended resources, count income
        if (remaining_water >= 0 and remaining_milk >= 0
                and remaining_coffee >= 0 and remaining_cups >= 0):
            self.print_preparation_success()
            self.water_amount = remaining_water
            self.milk_amount = remaining_milk
            self.disposable_cups = remaining_cups
            self.coffee_beans_quantity = remaining_coffee
            self.money_amount += coffee.price

        # If no - print missing resources and do not take money
        else:
            missing_resources = []
            if remaining_water < 0:
                missing_resources.append("water")
            if remaining_milk < 0:
                missing_resources.append("milk")
            if remaining_coffee < 0:
                missing_resources.append("coffee beans")
            if remaining_cups < 0:
                missing_resources.append("cups")
            self.print_not_enough_resources_error(', '.join(missing_resources))

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
        Describes coffee machine operation: asks for action to perform
        BUY: prepare coffee of requested coffee type, recalculate resources
        FILL: replenish coffee machine resources
        TAKE: withdraw all the money from coffee machine
        REMAINING: print current state of resources
        EXIT: quit the program
        """

        while True:
            requested_action = self.validate_action(self.ask_for_action())

            if requested_action == self.BUY_ACTION:
                requested_coffee_type = self.ask_for_coffee_type()
                if requested_coffee_type == self.BACK_ACTION:
                    continue
                requested_coffee_type = self.validate_coffee_option(requested_coffee_type)
                self.prepare_coffee(self.COFFEE_TYPES.get(requested_coffee_type))
            elif requested_action == self.FILL_ACTION:
                self.fill_resources()
            elif requested_action == self.TAKE_ACTION:
                self.withdraw_money()
            elif requested_action == self.REMAINING_ACTION:
                self.print_current_state()
            elif requested_action == self.EXIT_ACTION:
                break

    @classmethod
    def validate_action(cls, action):
        """
        Check if action is available
        :param action: action to check
        :return: action if valid
        """
        if action not in cls.AVAILABLE_TOP_LEVEL_ACTIONS:
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
        return input(f"Write action ({', '.join(cls.AVAILABLE_TOP_LEVEL_ACTIONS)}): \n")

    @classmethod
    def list_coffee_options(cls):
        """
        Constructs a numbered list of coffee options based on coffee types
        :return: list of coffee options as a string
        """
        return ', '.join(
            [f'{index} - {coffee_type.name}' for index, coffee_type in cls.COFFEE_TYPES.items()])

    @classmethod
    def ask_for_coffee_type(cls):
        """
        Ask user input for coffee type to prepare
        """
        return int(input(f'What do you want to buy? '
                         f'{cls.list_coffee_options()}, {cls.BACK_ACTION} - to the main menu\n'))

    @classmethod
    def print_preparation_success(cls):
        """
        Prints message that there are enough resources
        """
        print('I have enough resources, making you a coffee!')

    @classmethod
    def print_not_enough_resources_error(cls, resource_name):
        """
        Prints message that there are NOT enough resources
        """
        print(f'Sorry, not enough {resource_name}!')

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
