"""
Tic tac toe game business logic
"""

from tictactoe.game_exceptions import MoveNotValidError


class TicTacToe:
    """
    Stores and changes the Tic tac toe table
    """

    def __init__(self):
        self.matrix = None
        self.reset_matrix()

    def _get_cell_value(self, x_axis, y_axis):
        """Retrieve value from cell"""
        return self.matrix[y_axis][self._find_column(x_axis)]

    def set_cell_value(self, x_axis, y_axis, value):
        """Set value to cell"""
        self.validate_move_to_cell(x_axis, y_axis)
        self.matrix[y_axis][self._find_column(x_axis)] = value

    def validate_move_to_cell(self, x_axis, y_axis):
        """Validate move to cell not to override existing moves"""
        if self._get_cell_value(x_axis, y_axis):
            raise MoveNotValidError(f"The cell {x_axis}{y_axis} already filled. Pick another")

    def _find_column(self, x_axis):
        """Find column index"""
        return self.matrix[0].index(x_axis)

    def _get_columns(self):
        """Slice table to columns"""
        return [[row[i] for row in self._strip_matrix_to_values()] for i in
                range(len(self._strip_matrix_to_values()[0]))]

    def _get_diagonals(self):
        """Retrieve table diagonals"""
        first_diagonal = [row[index] for index, row in enumerate(self._strip_matrix_to_values())]
        second_diagonal = [row[~index] for index, row in enumerate(self._strip_matrix_to_values())]
        return [first_diagonal, second_diagonal]

    def _strip_matrix_to_values(self):
        """Get all the table values without headers"""
        return [row[1:] for row in self.matrix[1:]]

    def check_matrix_for_win(self):
        """Check if there is any 3-figure line is the table"""
        return any([self._check_rows_for_win(),
                    self._check_columns_for_win(),
                    self._check_diagonals_for_win()])

    def _check_rows_for_win(self):
        """Check if there is 3-figure horizontal line"""
        return any(self._all_values_equal_and_non_empty(row)
                   for row in self._strip_matrix_to_values())

    def _check_columns_for_win(self):
        """Check if there is 3-figure vertical line"""
        return any(self._all_values_equal_and_non_empty(column)
                   for column in self._get_columns())

    def _check_diagonals_for_win(self):
        """Check if there is 3-figure diagonal line"""
        return any(self._all_values_equal_and_non_empty(diagonal)
                   for diagonal in self._get_diagonals())

    def is_matrix_filled(self):
        """Check if the table is fully filled"""
        return all(all(row) for row in self._strip_matrix_to_values())

    def reset_matrix(self):
        """Reset the table to initial state"""
        self.matrix = [[0, "A", "B", "C"],
                       [1, "", "", ""],
                       [2, "", "", ""],
                       [3, "", "", ""]]

    @staticmethod
    def _all_values_equal_and_non_empty(values):
        """Check if all supplied values are same and not empty"""
        return all(values) and len(set(values)) == 1
