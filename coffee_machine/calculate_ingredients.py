"""
The second stage

Coffee machine asks how many cups a user needs and calculates the ingredients for the request
"""


def calculate_ingredients(number_of_cups):
    """Calculates milk, water, coffee beans for the requested number of cups"""
    water_per_cup_in_ml = 200
    milk_per_cup_in_ml = 50
    coffee_beans_per_cup_in_g = 15
    return (number_of_cups * water_per_cup_in_ml,
            number_of_cups * milk_per_cup_in_ml,
            number_of_cups * coffee_beans_per_cup_in_g)


cups = int(input("Write how many cups of coffee you will need:\n"))
ingredients = calculate_ingredients(cups)
print(f"""For {cups} cups of coffee you will need:
{ingredients[0]} ml of water
{ingredients[1]} ml of milk
{ingredients[2]} g of coffee beans""")
