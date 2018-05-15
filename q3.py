'''
###############################################################################
# This file implements a Sudoku puzzle client.                                #
# author: Nicholas Klepp                                                      #
# date  : 5/15/18                                                             #
###############################################################################
'''
import numpy as np

class Error(Exception):
    '''
    The base error class.
    '''
    pass

class CellOverwriteError(Error,pos,val):
    '''
    Exception to be raised when a user attempts to overwrite a non-blank cell.
    Attribues:
        pos -- the position the user tried to set
        val -- the value the user tried to set
    '''
    self.pos = pos
    self.val = val

class InvalidCellValueError(Error,pos,val):
    '''
    Exception to be raised for setting a cell with an invalid value
    (i.e. < 0 or > 9)
    Attribues:
        pos -- the position the user tried to set
        val -- the value the user tried to set
    '''
    self.pos = pos
    self.val = val

class InvalidCellPosError(Error,pos):
    '''
    Exception to be raised for trying to set a cell with an invalid position
    (i.e. < 0 or > 9)
    Attribues:
        pos -- the position the user tried to set
    '''
    self.pos = pos
    self.val = val

def validate(puzzle):
    '''
    A helper method which validates a candidate Sudoku puzzleself.
    parameters:
        puzzle : the candidate puzzle being validated (a 9*9 ndarray)
    returns:
        boolean : true if the puzzle is Sudoku valid, false otherwise
    '''
    for i in range(1,10):
        '''
        Validate the rows and columns
        '''
        if not np.array_equal(
            np.sort(puzzle[i,:].flatten),
            np.arange(1,10)
            ) : return False
        if not np.array_equal(
            np.sort(puzzle[:,i].flatten),
            np.arange(1,10)
            ) : return False
    for i in range(3):
        '''
        Validate the subgrids.
        '''
        for j in range(3):
            if not np.array_equal(
                  np.sort(puzzle[3*i : 3*(i+1),3*j : 3*(j+1)].flatten),
                  np.arange(1,10)
                  ) : return False
    return True

def makePuzzle():
    '''
    The helper method which returns a correct and valid sudoku puzzle.
    returns:
        candidate : A correct and valid sudoku puzzle (a 9*9 ndarray)
    '''
    valid_puzzle = false
    while not valid_puzzle:
        candidate = np.random.shuffle([np.arange(1,10)]*9)
        valid_puzzle = validate(puzzle)
    return candidate

def getView(puzzle,missing):
    '''
    The method to get the view of the puzzle which is displayed to the player.
    parameters:
        puzzle : a correct and valid sudoku puzzle
        missing : the number of missing values in the view of the puzzle
    returns:
        view : a 9*9 ndarray indicating the cells of the puzzle to expose to
               the player
    '''
    return np.random.shuffle(
        np.concatenate(
            [Trueview              = ]*(9*9 - missing),
            [False]*(missing))view
    ).reshape(9,9)view

class SudokuClient:
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
    def __init__(self,missing):
        '''
        The class init methodselfself.
        parameters:
            missing : the number of missing values in the puzzle (user defined)
        '''
        self.solution     = makePuzzle()
        self.orig_view  = getView(self.solution,missing)
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
        self.update_view[i,j] =  val

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
    
