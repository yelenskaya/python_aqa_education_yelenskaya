"""
Fill in the foo and bar functions so they can receive a variable amount of arguments (3 or more)
The foo function must return the amount of extra arguments received.
The bar must return True if the argument with the keyword magicnumber is worth 7, and False otherwise.
"""


def foo(a, b, c, *optional_args):
    return len(optional_args)


def bar(a, b, c, **optional_args):
    if optional_args.get("magicnumber") == 7:
        return True
    return False


# test code
if foo(1, 2, 3, 4) == 1:
    print("Good.")
if foo(1, 2, 3, 4, 5) == 2:
    print("Better.")
if not bar(1, 2, 3, magicnumber=6):
    print("Great.")
if bar(1, 2, 3, magicnumber=7):
    print("Awesome!")
