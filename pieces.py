"""Classes and utilities to describe all of the game pieces.
"""

class Piece(object):
    """A piece is a collection of tiles with various (x,y) offsets.

    Variables:
    - x: List of x coordinates of the piece
    - y: List of y coordinates of the piece
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

        self.x = x_list
        self.y = y_list

    def getNumTiles(self):
        """Return the number of tiles in this block. Helpful for iterating 
        through each tile.
        """
        return len(self.x)

    def getTile(self, tile, x_offset=0, y_offset=0, rot=0, flip=False):
        """Return the (x,y) position of the <tile>th tile in this piece.

        x_offset, y_offset, rot, and flip are provided to help easily calculate 
        positions on the game board.
        """

        if rot < 0 or rot > 3:
            raise ValueError("rot must be in range [0,3] (given %d)" % rot)

        if rot == 1:
            x =  self.y
            y = -self.x
        elif rot == 2:
            x = -self.x
            y = -self.y
        elif rot == 3:
            x = -self.y
            y =  self.x
        else: # rot = 0
            x =  self.x
            y =  self.y
        if flip:
            x = -x

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
        return len(self.pieces)

    def getPiece(self, n):
        if n < 0:
            raise ValueError("Can't retrieve piece %d" % n)

        return self.pieces[n]

if __name__ == "__main__":
    pl = PieceList("valid_pieces.txt")
    print pl.getNumPieces()
    for i in range(pl.getNumPieces()):
        print pl.getPiece(i).getNumTiles()
