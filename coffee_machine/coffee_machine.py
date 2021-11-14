"""
The sixth stage

Coffee machine with the input moved to an external script and saving the state
"""


class CoffeeRecipe:
    """
    Describes coffee recipe
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
    _SELECT_ACTION_MODE = 'action'

    _BUY_ACTION = 'buy'
    _FILL_ACTION = 'fill'
    _TAKE_ACTION = 'take'
    _REMAINING_ACTION = 'remaining'
    _EXIT_ACTION = 'exit'
    _BACK_ACTION = 'back'

    _AVAILABLE_TOP_LEVEL_ACTIONS = (_BUY_ACTION, _FILL_ACTION,
                                    _TAKE_ACTION, _REMAINING_ACTION, _EXIT_ACTION)

    _ESPRESSO = CoffeeRecipe(name='espresso',
                             water_amount=250,
                             coffee_beans_quantity=16,
                             price=4)
    _LATTE = CoffeeRecipe(name='latte',
                          water_amount=350,
                          coffee_beans_quantity=20,
                          price=7,
                          milk_amount=75)
    _CAPPUCCINO = CoffeeRecipe(name='cappuccino',
                               water_amount=200,
                               coffee_beans_quantity=12,
                               price=6,
                               milk_amount=100)

    _COFFEE_TYPES = {'1': _ESPRESSO, '2': _LATTE, '3': _CAPPUCCINO}

    def __init__(self, water_amount, milk_amount,
                 coffee_beans_quantity, disposable_cups, money_amount):
        self._water_amount = water_amount
        self._milk_amount = milk_amount
        self._coffee_beans_quantity = coffee_beans_quantity
        self._disposable_cups = disposable_cups
        self._money_amount = money_amount

        self._state = self._SELECT_ACTION_MODE
        self._filled_resources_progress = {
            'ml of water': False,
            'ml of milk': False,
            'grams of coffee beans': False,
            'disposable coffee cups': False
        }

    def handle_input(self, user_input):
        """
        Accepts user input and determines the next action based on the current machine state
        :return: next prompt and whether the program should exit
        """
        next_prompt = self.get_initial_prompt()
        should_exit = False

        if self._state == self._SELECT_ACTION_MODE and user_input == self._BUY_ACTION:
            self._state = self._BUY_ACTION
            next_prompt = self._get_buy_prompt()

        elif self._state == self._BUY_ACTION and user_input == self._BACK_ACTION:
            self._state = self._SELECT_ACTION_MODE

        elif self._state == self._BUY_ACTION and user_input != self._BACK_ACTION:
            self._prepare_coffee(self._COFFEE_TYPES.get(user_input))
            self._state = self._SELECT_ACTION_MODE

        elif self._state == self._SELECT_ACTION_MODE and user_input == self._FILL_ACTION:
            self._state = self._FILL_ACTION
            next_prompt = self._get_next_resource_filling_prompt()

        elif self._state == self._FILL_ACTION:
            filling_complete = self._handle_fill(user_input)
            if filling_complete:
                self._state = self._SELECT_ACTION_MODE
            else:
                next_prompt = self._get_next_resource_filling_prompt()

        elif self._state == self._SELECT_ACTION_MODE and user_input == self._TAKE_ACTION:
            self._take()
            self._state = self._SELECT_ACTION_MODE

        elif self._state == self._SELECT_ACTION_MODE and user_input == self._REMAINING_ACTION:
            self._print_remaining()
            self._state = self._SELECT_ACTION_MODE

        elif self._state == self._SELECT_ACTION_MODE and user_input == self._EXIT_ACTION:
            should_exit = True

        return {'next_prompt': next_prompt, 'should_exit': should_exit}

    def _prepare_coffee(self, coffee: CoffeeRecipe):
        """
        Prepares coffee, calculate changes in resources and in money
        depending on prepared coffee type
        :param coffee: coffee to prepare
        """

        # Determine if there are enough resources
        remaining_water = self._water_amount - coffee.water_amount
        remaining_milk = self._milk_amount - coffee.milk_amount
        remaining_coffee = self._coffee_beans_quantity - coffee.coffee_beans_quantity
        remaining_cups = self._disposable_cups - 1

        # If yes - print success, subtract expended resources, count income
        if (remaining_water >= 0 and remaining_milk >= 0
                and remaining_coffee >= 0 and remaining_cups >= 0):
            self._print_preparation_success()
            self._water_amount = remaining_water
            self._milk_amount = remaining_milk
            self._disposable_cups = remaining_cups
            self._coffee_beans_quantity = remaining_coffee
            self._money_amount += coffee.price

        # If no - print missing resources and do not take money
        else:
            missing_resources = []
            if remaining_water < 0:
                missing_resources.append('water')
            if remaining_milk < 0:
                missing_resources.append('milk')
            if remaining_coffee < 0:
                missing_resources.append('coffee beans')
            if remaining_cups < 0:
                missing_resources.append('cups')
            self._print_not_enough_resources_error(', '.join(missing_resources))

    def _handle_fill(self, user_input):
        """
        Determine the stage of filling the resources, fill the next not filled
        :return: whether all resources are filled
        """
        # Get resources which are not filled yet
        not_filled_resources = self._get_resources_yet_to_be_filled()

        # If there are some, fill the first one
        if not_filled_resources:
            resource_to_process = not_filled_resources[0]
            self._fill_single_resource(resource_to_process, user_input)
            not_filled_resources.remove(resource_to_process)
            self._filled_resources_progress[resource_to_process] = True

        # Check if there are still some resources to be filled
        # and return whether operation is complete
        if not_filled_resources:
            return False

        # If all resources are filled, reset progress for operation to the initial state
        self._reset_resource_filling_progress()
        return True

    def _fill_single_resource(self, resource_name, user_input):
        """
        Fill a specified resource
        """

        user_input_as_number = int(user_input)

        if 'milk' in resource_name:
            self._milk_amount += user_input_as_number
        elif 'water' in resource_name:
            self._water_amount += user_input_as_number
        elif 'coffee' in resource_name:
            self._coffee_beans_quantity += user_input_as_number
        elif 'cups' in resource_name:
            self._disposable_cups += user_input_as_number

    def _take(self):
        """
        Withdraw all the money from coffee machine
        """
        print(f'I gave you {self._money_amount}')
        self._money_amount = 0

    def _print_remaining(self):
        """
             Print current state of coffee machine resources
             """
        print(self)

    def _get_resources_yet_to_be_filled(self):
        """
        Filter filling resource progress dictionary to get not filled resource
        :return: filtered list
        """
        return [coffee_resource for coffee_resource, filled in self._filled_resources_progress.items()
                if not filled]

    def _get_next_resource_filling_prompt(self):
        """
        Construct the prompt for the next not filled resource
        """
        return f'Write how many {self._get_resources_yet_to_be_filled()[0]} you want to add:\n'

    def _reset_resource_filling_progress(self):
        """
        Reset filling resource progress dictionary to unfilled state
        """
        for resource in self._filled_resources_progress:
            self._filled_resources_progress[resource] = False

    def __str__(self):
        return f'''The coffee machine has:
{self._water_amount} of water 
{self._milk_amount} of milk 
{self._coffee_beans_quantity} of coffee beans 
{self._disposable_cups} of disposable cups 
{self._money_amount} of money'''

    @classmethod
    def get_initial_prompt(cls):
        """
        Construct initial prompt
        """
        return f"Write action ({', '.join(cls._AVAILABLE_TOP_LEVEL_ACTIONS)}): \n"

    @classmethod
    def _get_buy_prompt(cls):
        """
        Construct prompt for buy action
        """
        return f'What do you want to buy? {cls._list_coffee_options()}, ' \
               f'{cls._BACK_ACTION} - to the main menu\n'

    @classmethod
    def _list_coffee_options(cls):
        """
        Constructs a numbered list of coffee options based on coffee types
        :return: list of coffee options as a string
        """
        return ', '.join(
            [f'{index} - {coffee_type.name}' for index, coffee_type in cls._COFFEE_TYPES.items()])

    @classmethod
    def _print_preparation_success(cls):
        """
        Prints message that there are enough resources
        """
        print('I have enough resources, making you a coffee!')

    @classmethod
    def _print_not_enough_resources_error(cls, resource_name):
        """
        Prints message that there are NOT enough resources
        """
        print(f'Sorry, not enough {resource_name}!')


def request_input_for_coffee_machine():
    """
    Requests user input, passes it to coffee machine to process
    """
    coffee_machine = CoffeeMachine(water_amount=400, milk_amount=540,
                                   coffee_beans_quantity=120, disposable_cups=9, money_amount=550)

    should_exit = False
    next_prompt = coffee_machine.get_initial_prompt()

    while not should_exit:
        output = coffee_machine.handle_input(input(next_prompt))
        should_exit = output['should_exit']
        next_prompt = output['next_prompt']


request_input_for_coffee_machine()
