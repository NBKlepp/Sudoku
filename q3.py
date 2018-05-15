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
    Exception to be raised for setting a cell with an invalid value (i.e. < 0 or > 9)
    Attribues: 
        pos -- the position the user tried to set  
        val -- the value the user tried to set
    '''
    self.pos = pos
    self.val = val

class InvalidCellPosError(Error,pos,val):
    '''
    Exception to be raised for trying to set a cell with an invalid position (i.e. < 0 or > 9)
    Attribues: 
        pos -- the position the user tried to set  
        val -- the value the user tried to set
    '''
    self.pos = pos
    self.val = val

class SudokuPuzzle:
    def __init__(self,missing):
        puzzle        = makePuzzle()
        self.solution = puzzle
        self.view     = getView(puzzle,missing)

    def setCell(pos,val):
        
        if ( self.view[i,j] < 0 ) :
            self.view[i,j] = 
