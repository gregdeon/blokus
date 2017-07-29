"""Classes and utilities to describe all of the game pieces.
"""

def negateList(lst):
    """Helper function: negate every item in a list
    """
    return [-x for x in lst]

class Piece(object):
    """A piece is a collection of tiles with various (x,y) offsets.

    Variables:
    - x: Lists of x coordinates of the piece
    - y: Lists of y coordinates of the piece

    x and y each have 8 elements, which are:
    x/y[0]: Initial orientation
    x/y[1]: Rotated CW once
    x/y[2]: Rotated CW twice
    x/y[3]: Rotated CW three times
    x/y[k+4]: x/y[k] flipped horizontally
    """

    def __init__(self, x_list, y_list):
        if len(x_list) != len(y_list):
            raise ValueError(
                "Length of x and y lists are unequal (%d and %d)" % \
                (len(x_list), len(y_list)))
        if len(x_list) == 0:
            raise ValueError("No tiles provided!")
        if len(x_list) > 5:
            raise ValueError("%d tiles provided; maximum 5" % len(x_list))

        # Calculate flipped lists
        x_list_flipped = negateList(x_list)
        y_list_flipped = negateList(y_list)

        # Set up data structure
        self.x = []
        self.y = []

        # Position 0: default
        self.x.append(x_list)
        self.y.append(y_list)

        # Position 1: rotated x1
        self.x.append(y_list)
        self.y.append(x_list_flipped)

        # Position 2: rotated x2
        self.x.append(x_list_flipped)
        self.y.append(y_list_flipped)

        # Position 3: rotated x3
        self.x.append(y_list_flipped)
        self.y.append(x_list)

        # Positions 4-7: flipped copies
        for i in range(4):
            self.x.append(negateList(self.x[i]))
            self.y.append(self.y[i])

        print self.x

    def getNumTiles(self):
        """Return the number of tiles in this block. Helpful for iterating 
        through each tile.
        """
        return len(self.x[0])

    def getTile(self, tile, x_offset=0, y_offset=0, rot=0, flip=False):
        """Return the (x,y) position of the <tile>th tile in this piece.

        x_offset, y_offset, rot, and flip are provided to help easily calculate 
        positions on the game board.
        """

        # Find the correct rotation/flip in the list
        idx = rot
        if flip:
            idx += 4

        x = self.x[idx]
        y = self.y[idx]

        # Add offsets
        return (x[tile] + x_offset, y[tile] + y_offset)

class PieceList(object):
    """The PieceList class stores a list of all of the Blokus game pieces (the
    distinct 5-polyominos).
    """

    def __init__(self, fname):
        """Read the game pieces from the file <fname>

        File format must be:
        - Line 1: N (number of pieces)
        - For k in [0, N):
          - Line 1: L (number of lines in piece)
          - Lines 2 - L+1: layout of piece (# means tile, O means center)

        Sample file:
        2
        2
        O#
        ##
        1
        ##O##
        """
        self.pieces = []
        with open(fname) as f:
            lines = f.read().splitlines()

        N = int(lines[0])
        L = 1
        for i in range(N):
            x_origin = 0
            y_origin = 0

            x_list = []
            y_list = []

            num_lines = int(lines[L])
            for j in range(num_lines):
                line = lines[L+1+j]
                for k in range(len(line)):
                    if line[k] in ('O', 'o', '0'):
                        x_origin = k
                        y_origin = j
                    if line[k] is not ' ':
                        x_list.append(k)
                        y_list.append(j)

            x_list = [x - x_origin for x in x_list]
            y_list = [y - y_origin for y in y_list]
            self.pieces.append(Piece(x_list, y_list))

            L += 1 + num_lines
        
    def getNumPieces(self):
        """Return the number of distinct pieces in the list.
        """
        return len(self.pieces)

    def getPiece(self, n):
        """Return piece <n> from this list.
        """
        if n < 0:
            raise ValueError("Can't retrieve piece %d" % n)

        return self.pieces[n]

"""global_piece_list: A shared PieceList object. Use the following functions to 
access it from other modules.
"""
global_piece_list = None

def initPieceList(fname):
    """Create a global list of pieces by reading from <fname>.

    Stores a single list so that other modules don't need to re-run the 
    piece list initialization. 
    
    Call this once during startup.
    """
    global global_piece_list

    global_piece_list = PieceList(fname)

def getPieceList():
    """Return the shared global piece list.
    """
    return global_piece_list

if __name__ == "__main__":
    # Test piece list loading
    pl = PieceList("valid_pieces.txt")
    print pl.getNumPieces()
    for i in range(pl.getNumPieces()):
        print pl.getPiece(i).getNumTiles()
