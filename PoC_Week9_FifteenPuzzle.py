"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction + self
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) <> 0:
            return False
        for col in xrange(target_col + 1, self._width):
            if self.get_number(target_row, col) <> target_row * self._width + col:
                return False
        for row in xrange(target_row + 1, self._height):
            for col in xrange(self._width):
                if self.get_number(row, col) <> row * self._width + col:
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row > 1 and target_col > 0, "Incorrect call for solve_interior_tile"        
        current = self.current_position(target_row, target_col)
        
        solution = self._position_tile(target_row, target_col, current[0], current[1])

        self.update_puzzle(solution)
        
        return solution

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        #assert target_row > 1, "Incorrect call for solve_col0_tile"
        current = self.current_position(target_row, 0)
        solution = "ur"
        if current[0] == target_row - 1 and current[1] == 0:
            solution += "r" * (self._width - 2)
            self.update_puzzle(solution)
            return solution
        
        self.update_puzzle(solution)
        current = self.current_position(target_row, 0)
        solution1 = self._position_tile(target_row - 1, 1, current[0], current[1])
        self.update_puzzle(solution1)
        solution2  = "ruldrdlurdluurddlur"
        self.update_puzzle(solution2)
        solution3 = "r" * (self._width - 2)
        self.update_puzzle(solution3)

        return solution + solution1 + solution2 + solution3
    
    def _position_tile(self, t_r, t_c, c_r, c_c):
        """
        Moves tile from (c_r, c_c) to (t_r, t_c)
        """
        solution = ""
        # move to current position
        solution += "u" * max ((t_r - c_r) - 1, 0)
        if t_c > c_c:
            if t_r > c_r:
                solution += "u"
            solution += "l" * (t_c - c_c)
            if c_r > 0:
                solution += "urrdl" * max((t_c - c_c) - 1, 0)
            else:
                solution += "drrul" * max((t_c - c_c) - 1, 0)
            if t_r > c_r:
                solution += "dr"
        if t_c < c_c:
            if t_r > c_r:
                solution += "u"
            solution += "r" * (c_c - t_c)
            if c_r > 0:
                solution += "ulldr" * max((c_c - t_c) - 1, 0)
            else:
                solution += "dllur" * max((c_c - t_c) - 1, 0)
            if t_r > c_r and c_r > 0:
                solution += "ullddr"
            elif t_r > c_r:
                 solution += "dl"
        if t_r > c_r:
            solution += "ulddr" * max(0, (t_r - c_r) - 1) + "uld"
        return solution
        

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) <> 0:
            return False
        for row in xrange(2, self._height):
            for col in xrange(self._width):
                if self.get_number(row, col) <> row * self._width + col:
                    return False
        for col in xrange(target_col + 1, self._width):
            if self.get_number(0, col) <>  col:
                return False
        for col in xrange(target_col, self._width):
            if self.get_number(1, col) <>  self._width + col:
                return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.lower_row_invariant(1, target_col):
            return False
        for col in xrange(target_col + 1, self._width):
            if self.get_number(0, col) <>  col:
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        current = self.current_position(0, target_col)
        self.update_puzzle("ld")
        if current[0] == 0 and current[1] == target_col - 1:
            return "ld"

        current = self.current_position(0, target_col)
        solution = self._position_tile(1, target_col - 1, current[0], current[1])
        self.update_puzzle(solution + "urdlurrdluldrruld")
        return "ld" + solution + "urdlurrdluldrruld"

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        current = self.current_position(1, target_col)
        solution = self._position_tile(1, target_col, current[0], current[1])
        solution += "ur"
        
        self.update_puzzle(solution)
        
        return solution

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        solution = "ul"
        self.update_puzzle(solution)
        while not self.row0_invariant(0):
            solution += "rdlu"
            self.update_puzzle("rdlu")
        return solution

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        zero = self.current_position(0, 0)
        solution =  "d" * ((self._height - zero[0]) - 1)
        solution += "r" * ((self._width  - zero[1]) - 1)
        self.update_puzzle(solution)
        
        for row in xrange(self._height - 1, 1, -1):
            for col in xrange(self._width - 1, 0, -1):
                assert self.lower_row_invariant(row, col)
                solution += self.solve_interior_tile(row, col)
            assert self.lower_row_invariant(row, 0)
            solution += self.solve_col0_tile(row)
        assert self.lower_row_invariant(1, self._width - 1)

        for col in xrange(self._width - 1, 1, -1):
            assert self.row1_invariant(col)
            solution += self.solve_row1_tile(col)
            assert self.row0_invariant(col)
            solution += self.solve_row0_tile(col)
        assert self.row1_invariant(1)
        
        solution += self.solve_2x2()
        assert self.row0_invariant(0)

        return solution

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


