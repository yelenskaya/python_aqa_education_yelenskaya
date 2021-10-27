"""
In this exercise, you will need to print an alphabetically sorted list of all functions in the re module,
which contain the word find.
"""

import re

print(sorted([re_function for re_function in dir(re) if 'find' in re_function]))
