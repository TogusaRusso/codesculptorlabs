"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    #create empty array equal to line
    outline = [0] * len(line)
    #index in output array
    index = 0
    #flag meaning we can merge
    can_merge = False
    for cell in line:
        if cell > 0:
            if can_merge:
                if cell == outline[index - 1]:
                    #current cel equal to previous
                    #let's merge them together
                    outline[index - 1] += cell
                    #and we can't merge more
                    #for now
                    can_merge = False
                else:
                    #not equal just put it to next cell
                    outline[index] = cell
                    index += 1
            else:
                #we can't merge, so just put
                outline[index] = cell
                index += 1
                #and on next step we can merge
                can_merge = True
    return outline


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.__sides = {}
        left_list = []
        right_list = []
        for row in xrange(grid_height):
            left_list.append((row, 0))
            right_list.append((row, grid_width - 1))
        self.__sides[LEFT] =  left_list
        self.__sides[RIGHT] = right_list
        up_list = []
        down_list = []
        for col in xrange(grid_width):
            up_list.append((0, col))
            down_list.append((grid_height - 1, col))
        self.__sides[UP] =  up_list
        self.__sides[DOWN] = down_list
        #print self.__sides
        self.__height = grid_height
        self.__width = grid_width
        self.reset()
        

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        #little trick for get rid of unused variable
        #warning
        self.__grid = [[0  for dummy_col in xrange(self.get_grid_width())]
                           for dummy_row in xrange(self.get_grid_height())]
        self.new_tile()
        self.new_tile()


    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ""
        for row in xrange(self.get_grid_height()):
            string += '['
            for col in xrange(self.get_grid_width()):
                string += str(self.get_tile(row, col))
                if col < self.get_grid_width() - 1:
                    string += ', '
            string += ']'
            if row < self.get_grid_height() - 1:
                string += '\n'
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.__height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.__width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        #get starting points of lines
        start_points = self.__sides[direction]
        #set flag is tiles moved
        is_moved = False
        for start_point in start_points:
            #fill current line
            temp_list = []
            row = start_point[0]
            col = start_point[1]
            while (row >= 0 and col >= 0 
                   and row < self.get_grid_height() 
                   and col < self.get_grid_width()):
                temp_list.append(self.get_tile(row, col))
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            #merge current line
            temp_list = merge(temp_list)
            #and put merged line back
            row = start_point[0]
            col = start_point[1]
            while (row >= 0 and col >= 0 
                   and row < self.get_grid_height() 
                   and col < self.get_grid_width()):
                new_value = temp_list.pop(0)
                #if tile changed, set it new value
                #and set flag to True
                if new_value != self.get_tile(row, col):
                    self.set_tile(row, col, new_value)
                    is_moved = True
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
        #if any tile moved, setting new tile
        if is_moved:
            self.new_tile()
                   
            
                                          

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if random.randrange(10) == 0:
            value = 4
        else:
            value = 2
        row = random.randrange(self.get_grid_height())
        col = random.randrange(self.get_grid_width())
        while self.get_tile(row, col) > 0:
            row = random.randrange(self.get_grid_height())
            col = random.randrange(self.get_grid_width())
        self.set_tile(row, col, value)
                                            

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.__grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.__grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
