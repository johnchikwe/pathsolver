from typing import List

from llstack import LLStack

class InvalidCoordinateError(Exception):
    pass

class OutOfBoundaries(Exception):
    pass

class Map:
    """
    This class is responsible for finding paths through map

    Attributes:
        grid (list): 2D grid of map
        start_loc (tuple): starting coordinates of pathfinder
        end_loc (tuple): coordinates that path is supposed to lead to

    """
    def __init__(self, grid: List[List[str]], start_loc: tuple, end_loc: tuple):
        """
        Initializes grid, start_loc, end_loc

        Raises:
            TypeError: if grid isn't a list, if rows aren't, and if the columns inside aren't strings
            ValueError: if the cells in grid are not strings in form ocean and grass

        """

        if not isinstance(grid, list):
            raise TypeError

        """
        Using or for ocean and grass means that if you have an ocean cell then a value error 
        would be raised
        """
        for r in grid:
            if not isinstance(r, list):
                raise TypeError
            for c in r:
                if not isinstance(c, str):
                    raise TypeError
                if c != "ocean" and c != "grass":
                    raise ValueError
        else:
            self.__grid = grid

        self.start_coords = start_loc
        self.end_coords = end_loc

    @property
    def start_coords(self):
        """
        This property returns starting coordinates

        Returns:
            start (tuple): starting coordinates for map
        """
        return self.__start

    @start_coords.setter
    def start_coords(self, coords):
        """
        This property sets current start coordinates to new value

        Parameters:
            coords (tuple): starting coordinates for the map

        Raises:
            TypeError: if coords isn't a tuple, if values in tuple aren't integers
            ValueError: if length of coordinates isn't 2, or values in tuple are less than 0
            OutOfBoundaries: if values in coords are out of bounds
            InvalidCoordinateError: if coords puts you into an ocean spot on grid
        """
        if not isinstance(coords, tuple):
            raise TypeError
        if len(coords) != 2:
            raise ValueError
        for v in coords:  # using a for loop is much more efficient in raising the value errors
            if not isinstance(v, int):
                raise TypeError
            if v < 0:
                raise ValueError
        if coords[0] >= len(self.__grid):
            raise OutOfBoundaries()
        if coords[1] >= len(self.__grid[coords[0]]):
            raise OutOfBoundaries()
        if self.__grid[coords[0]][coords[1]] == "ocean":
            raise InvalidCoordinateError()

        self.__start = coords

    @property
    def end_coords(self):
        """
        This property returns ending coordinates of map

        Returns:
            end (tuple): ending coordinates of map
        """
        return self.__end

    @end_coords.setter
    def end_coords(self, coords):  # this is exactly like star_coords, only change is the check with start_coords
        """
        This property sets current end coordinates to new value

        Parameters:
            coords (tuple): starting coordinates for the map

        Raises:
            TypeError: if coords isn't a tuple, if values in tuple aren't integers
            ValueError: if length of coordinates isn't 2, or values in tuple are less than 0
            or if coords are same as starting

            OutOfBoundaries: if values in coords are out of bounds
            InvalidCoordinateError: if coords puts you into an ocean spot on grid
        """
        if not isinstance(coords, tuple):
            raise TypeError
        if len(coords) != 2:
            raise ValueError
        for v in coords:
            if not isinstance(v, int):
                raise TypeError
            if v < 0:
                raise ValueError
        if coords[0] >= len(self.__grid):
            raise OutOfBoundaries()
        if coords[1] >= len(self.__grid[coords[0]]):  # using the length of row in grid to accurately check number of columns
            raise OutOfBoundaries()
        if self.__grid[coords[0]][coords[1]] == "ocean":
            raise InvalidCoordinateError()
        if coords == self.start_coords:
            raise ValueError

        self.__end = coords

    @property
    def grid(self):
        """
        This property returns the current grid

        Returns:
            grid (tuple): current grid for map
        """
        return self.__grid

    def find_path(self):
        """
        This method does some logic on a path given starting and ending coordinates
        and a grid full of cells 'ocean' and 'grass'. It calls technical helper

        Returns:
            None: if the length of grid is 0 or no paths were found
            Result (LLStack): if valid path was found
        """
        if len(self.__grid) == 0:
            return
        row = self.start_coords[0]
        col = self.start_coords[1]
        ll_stack = LLStack()
        visited = set()
        result = self.solve(self.__grid, row, col, ll_stack, visited)
        if result is not None:
            return result
        else:
            return  # return essentially just returns none
    def solve(self, grid, row, col, ll_stack, visited):  # Use set for better time complexity
        """
        This method gets called by find_path and is responsible for technicalities
        of finding the path

        Parameters:
            grid (list): current 2d grid
            row (int): current row in grid
            col (int): current column in grid
            ll_stack (LLStack): current path
            visited (set): keeps track of visited coordinates

        Returns:
            None: if row or column is wrong, coordinate was visited, coordinate value is ocean, no paths were found
            path (LLStack): if a path is found, a LLStack is returned

        """
        if not (0 <= row < len(grid)):
            return

        if not (0 <= col < len(grid[row])):  # column size isn't same always
            return
            # visited.add((row, col))  # keeps track of visited spot, still have to do something with this

        if (row, col) in visited:
            return

        ll_stack.push((row, col))
        visited.add((row, col))
        if (row, col) == self.end_coords:
            return ll_stack

        if grid[row][col] == 'ocean':
            ll_stack.pop()
            return

        """
        Named all 'path' because technically the path updates each time
        
        There's a recursive call for each possible direction and if size of llstack is greater than zero
        then the backtracking occurs with "ll_stack.pop()"
        """
        path = self.solve(grid, row + 1, col, ll_stack, visited)  # going down a row
        if path:  # if there's a result then return that result
            return path

        path = self.solve(grid, row, col + 1, ll_stack, visited)  # going one column to right
        if path:
            return path

        path = self.solve(grid, row - 1, col, ll_stack, visited)  # going backwards a row
        if path:
            return path

        path = self.solve(grid, row, col-1, ll_stack, visited)  # going leftwards a column
        if path:
            return path

        if ll_stack.size > 0:
            ll_stack.pop()
        return None
