'''
###############################################################################
# This file implements a Sudoku puzzle client.                                #
# author: Nicholas Klepp                                                      #
# date  : 5/15/18                                                             #
###############################################################################
'''
import numpy as np

#A debug flag
DEBUG = True

class Error(Exception):
    '''
    The base error class.
    '''
    pass

class CellOverwriteError(Error):
    '''
    Exception to be raised when a user attempts to overwrite a non-blank cell.
    Attribues:
        pos -- the position the user tried to set
        val -- the value the user tried to set
    '''
    def __init__(pos,val):
        self.pos = pos
        self.val = val

class InvalidCellValueError(Error):
    '''
    Exception to be raised for setting a cell with an invalid value
    (i.e. < 0 or > 9)
    Attribues:
        pos -- the position the user tried to set
        val -- the value the user tried to set
    '''
    def __init__(pos,val):
        self.pos = pos
        self.val = val

class InvalidCellPosError(Error):
    '''
    Exception to be raised for trying to set a cell with an invalid position
    (i.e. < 0 or > 9)
    Attribues:
        pos -- the position the user tried to set
    '''
    def __init__(pos):
        self.pos = pos

def makePuzzle():
    '''
    The helper method which returns a correct and valid sudoku puzzle.
    returns:
        candidate : A correct and valid sudoku puzzle (a 9*9 ndarray)
    '''
    rows = [{1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9}]
    
    cols = [{1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9},
            {1,2,3,4,5,6,7,8,9}]
    
    subgrids = np.array([{1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9},
                         {1,2,3,4,5,6,7,8,9}]).reshape(3,3)

    if DEBUG : print("rows: {}".format(rows))
    if DEBUG : print("cols: {}".format(rows))
    if DEBUG : print("subgrids: {}".format(rows))
            
    puzzle = np.zeros((9,9))

    while 0 in puzzle:
        for i in range(3):
            if DEBUG : print("i: {}".format(i))
            for j in range(3):
                if DEBUG : print("j: {}".format(j))
                '''
                (i,j) tells us which sub-grid we're dealing with
                '''
                if 0 in puzzle[3*i:3*(i+1),3*j:3*(j+1)]:
                    k = np.random.randint(3)
                    l = np.random.randint(3)
                    while not puzzle[3*i + k,3*j+l] == 0 :
                        k = np.random.randint(3)
                        l = np.random.randint(3)
                    '''
                    (k,l) tells us which cell in the subgrid we're dealing with
                    '''
                    row = 3*i+k
                    col = 3*j+l
                    if DEBUG :
                        print("row: {}".format(row))
                        print("col: {}".format(col))                        
                    '''
                    row and col are the row and col value for the entire puzzle
                    '''
                    row_avail  = rows[row]
                    col_avail  = cols[col]
                    subg_avail = subgrids[i,j]
                    '''
                    We need to find all of the values that are legal to go into
                    the row, col and subgrid that we're dealing with. We also
                    want to perform a sanity check to make sure that there is at
                    least one such value we can insert.
                    '''
                    common_avail = row_avail & col_avail & subg_avail
                    if DEBUG :
                        print("row_avail: {}".format(row_avail))
                        print("col_avail: {}".format(col_avail))
                        print("subg_avail: {}".format(subg_avail))
                        print("common_avail: {}".format(common_avail))
                        
                    assert(not common_avail <= set() )
                    '''
                    Let's insert a random value from the common available values
                    to make a hopefully "unique" puzzle.
                    '''
                    cell_val = np.random.choice(list(common_avail))
                    '''
                    Remove the random value from the available lists for the
                    row, col and subrid we're looking at. Then set the puzzle
                    value appropriately.
                    '''
                    rows[row]     -= {cell_val}
                    cols[col]     -= {cell_val}
                    subgrids[i,j] -= {cell_val}
                    puzzle[row,col] = cell_val
                    if DEBUG :
                        print("puzzle: \n{}".format(puzzle))
                        print("rows: {}".format(rows))
                        print("cols: {}".format(cols))
                        print("subgrids: {}".format(subgrids))
                
    return candidate

def setView(puzzle,missing):
    '''
    The method to set the original view of the puzzle which is displayed to the
    user. The original view must be maintained to be sure the user doesn't try
    to reset an exposed cell.
    parameters:
        puzzle : a correct and valid sudoku puzzle
        missing : the number of missing values in the view of the puzzle
    returns:
        view : a 9*9 ndarray indicating the cells of the puzzle to expose to
               the player
    '''
    return np.random.shuffle(
        np.concatenate(
            [True]*(9*9 - missing),
            [False]*(missing)
    )).reshape(9,9)

class SudokuClient():
    '''
    The SudokuClient class includes attributes and methods to allow a user to
    enjoy a nice Sudoku puzzle challenge.

    instance attributes:
        solution : the solution for this particular puzzle
        orig_view : the original view of the puzzle (immutable)
        update_view : the updatable view of the puzzle (mutable)

    instance methods:
        getCell : get the value in the puzzle at a particular cell
        getView : get the value in the view at a particular cell
        setView : set the value in the view at a particular cell
    '''
    def __init__(self,missing=9):
        '''
        The class init methodselfself.
        parameters:
            missing : the number of missing values in the puzzle (user defined)
        '''
        self.solution     = makePuzzle()
        self.orig_view    = setView(self.solution,missing)
        self.update_view  = np.where(
            self.orig_view,
            self.solution,
            np.array([' ']*(9*9)).rehsape(9,9)
        )

    def getCell(pos):
        '''
        The method to get the value of a cell from the puzzle.
        parameters:
            pos : the position at which to get the cell value
        raises:
            InvalidCellPosError if the pos is out of bounds
        '''
        if i < 0 or j < 0 or i > 8 or j >8 :
            raise InvalidCellPosError(pos)
        return self.solution[i,j]

    def getView(pos):
        '''
        The method to get the value in the view of the puzzle.
        parameters:
            pos : the position at which to get the view (a tuple)
        raises:
            InvalidCellPosError if the cell position is out of bounds
        '''
        i = pos[0]
        j = pos[1]
        if i < 0 or j < 0 or i > 8 or j >8 :
            raise InvalidCellPosError(pos)
        return self.update_view[i,j]

    def getPuzzle():
        '''
        The moethod to get the underlying puzzle solution.
        returns:
            puzzle : the underlying puzzle solution.
        '''
    def setView(pos,val):
        '''
        The method to set the value in the view of the puzzle.
        parameters:
            pos : the position to set the view at (a tuple)
            val : the value to set the view to (an int)
        raises:
            InvalidCellPosError if the cell position is out of bounds
            InvalidCellValueError if the cell value is out of bounds
            CellOverwriteError if the cell was already exposed in the orig_view
        '''
        i = pos[0]
        j = pos[1]
        if i < 0 or j < 0 or i > 8 or j >8 :
            raise InvalidCellPosError(pos)
        if not self.orig_view[i,j] :
            raise CellOverwriteError(pos,val)
        if val < 1 or val > 9 :
            raise InvalidCellValueError(pos,val)
        self.update_view[pos[0],pos[1]]=val

    def print_view():
        '''
        The method to print the view. Could be improved to print a "pretty" view.
        '''
        print(self.update_view)

    def print_solution():
        '''
        The method to print the solution. See above note about "pretty" view.
        print(self.solution)
        '''
        print(self.solution)
