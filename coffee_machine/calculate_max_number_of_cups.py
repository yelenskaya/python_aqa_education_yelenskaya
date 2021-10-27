"""
The third stage

Coffee machine asks about the quantity of ingredients, how many cups a user needs
and determines whether it is able to make a requested number of cups
"""

WATER_PER_CUP_IN_ML = 200
MILK_PER_CUP_IN_ML = 50
COFFEE_BEANS_PER_CUP_IN_G = 15


def calculate_ingredients(number_of_cups):
    """Calculates milk, water, coffee beans for the requested number of cups"""
    return (number_of_cups * WATER_PER_CUP_IN_ML,
            number_of_cups * MILK_PER_CUP_IN_ML,
            number_of_cups * COFFEE_BEANS_PER_CUP_IN_G)


def calculate_max_possible_number_of_cups(amount_of_water, amount_of_milk, amount_of_beans):
    """Calculates max number of cups which is possible to prepare"""
    return min((amount_of_water // WATER_PER_CUP_IN_ML, amount_of_milk // MILK_PER_CUP_IN_ML,
                amount_of_beans // COFFEE_BEANS_PER_CUP_IN_G))


water_available = int(input("Write how many ml of water the coffee machine has:\n"))
milk_available = int(input("Write how many ml of milk the coffee machine has:\n"))
beans_available = int(input("Write how many grams of coffee beans the coffee machine has:\n"))
expected_cups = int(input("Write how many cups of coffee you will need:\n"))

max_cups = calculate_max_possible_number_of_cups(water_available, milk_available, beans_available)

if max_cups >= expected_cups:
    MESSAGE = "Yes, I can make that amount of coffee"
    if max_cups > expected_cups:
        MESSAGE += f" (and even {max_cups - expected_cups} more than that)"
    print(MESSAGE)
else:
    print(f"No, I can make only {max_cups} cups of coffee")
