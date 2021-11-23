"""Helper functions"""


def num_join(args):
    """Join numbers into a sequence"""
    return int("".join(str(num) for num in args))


def get_list_of_digits(num):
    """Get list of digits from a number"""
    return [int(char) for char in str(num)]


def sum_digits(num):
    """Sum all digits in a number"""
    return sum(get_list_of_digits(num))
