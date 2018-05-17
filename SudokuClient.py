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

def k_to_pos(k):
    '''
    The helper method to provide the mapping from k'th cell to grid pos.
    '''
    return (int(k/9),k-(int(k/9)*9))

def get_legal_values(k,puzzle):
    '''
    The helper method that determines the "legal" values for this cell.
    parameters :
        k     : the sequential indicator of the cell we're finding legal values
                for
        board : the status of the puzzle board at this time
    '''
    (i,j) = k_to_pos(k)
    (k,l) = (int(i/3),int(j/3))
    '''
    (k,l) tells us what subgrid we're dealing with
    '''
    row_avail  = set(np.arange(1,9)) - set(board[i,:])
    col_avail  = set(np.arange(1,9)) - set(board[:,j])
    subg_avail = set(np.arange(1,9)) - set(board[3*k:3:(k+1),3*l:3*(l+1)])

    return np.random.shuffle(np.array(list(row_avail & col_avail & subg_avail)))

def is_empty(legal_values) : return legal_values.size == 0

def makePuzzle():
    '''
    The helper method which returns a correct and valid sudoku puzzle.
    returns:
        candidate : A correct and valid sudoku puzzle (a 9*9 ndarray)
    '''

    ,puzzle = fill_puzzle(0,np.zeros((9,9))
    return puzzle

def add_cell_value(k,cell_value,puzzle):
    (i,j) = k_to_pos(k)
    puzzle[i,j] = cell_value
    return puzzle

def fill_puzzle(k,puzzle):
    '''
    The helper method to return a full, valid puzzle.
    This method recursively fills the puzzle, and is called sequentially once
    for each of the 9*9 cells of the 9 by 9 puzzle board, filling each cell in
    order (left to right, top to bottom) from the top left corner (k = 0) to
    the bottom right corner (9*9 -1).
    parameters:
        k      : the sequential cell value to fill
        puzzle : the state of the puzzle board after trying to fill the k-1 cell
    '''
    #Test if we've filled up the puzzle yet
    if k == 9*9 : return (True,puzzle)

    legal_values = get_legal_values(k,puzzle)

    #Test if we reached a dead end
    if is_empty(legal_values) : return (False,puzzle)

    cell_value =  legal_values[-1]
    legal_values = legal_values[:-1]
    candidate_puzzle = add_cell_value(k,cell_value,puzzle)
    (finished,finished_puzzle) = fill_puzzle(k+1,candidate_puzzle)

    while not finished:
        if is_empty(legal_values) : return (False,puzzle)
        cell_value = legal_values[-1]
        legal_values = legal_values[:-1]
        candidate_puzzle = add_cell_value(k,cell_value,puzzle)
        (finished,finished_puzzle) = fill_puzzle(k+1,candidate_puzzle)

    return (finished,finished_puzzle)

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
