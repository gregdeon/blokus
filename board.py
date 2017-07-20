from pieces import PieceList

class Move(object):
    """A Move describes how one of the players is going to spend their move.

    It contains:
    - Piece: the ID of the piece being used
    - x/y: the center coordinates of the piece [0-19)
    - Rotation: how many times the piece should be rotated CW [0-3]
    - Flip: whether the piece should be flipped (True/False)
    """
    def __init__(self, piece=0, x=0, y=0, rot=0, flip=False):
        self.piece = piece
        self.x = x
        self.y = y
        self.rot = rot
        self.flip = flip

class Board(object):
    """A Board describes the current state of the game board. It's separate from
    the game engine to allow the Input objects to check if their moves are valid,
    etc... without the help of the game engine.

    The Board stores:
    - board_w/board_h: the width and height of the playing area
    - _state: a 2D array of the board state. -1 = free; 0-3 = player x's tile
    - piece_list: A PieceList object (probably shared with the game engine) to
      help understand the moves
    """

    def __init__(self, board_w, board_h, piece_list):
        self.board_w = board_w
        self.board_h = board_h

        self._state = [[-1 for c in range(board_w)] for r in range(board_h)]
        self.piece_list = piece_list

    def addMove(self, player, move):
        """Try to add <player>'s <move>.

        If the move is legal, the board state is updated; if it's not legal, a
        ValueError is raised.

        Returns the number of tiles placed on the board.
        """
        if not self.checkMoveValid(player, move):
            raise ValueError("Move is not allowed")

        piece = self.piece_list.getPiece(move.piece)
        for t in range(piece.getNumTiles()):
            (x,y) = piece.getTile(t, move.x, move.y, move.rot, move.flip)
            self._state[y][x] = player
        return piece.getNumTiles()

    def checkMoveValid(self, player, move):
        """Check if <player> can legally perform <move>.

        For a move to be valid, it must:
        - Be completely in bounds
        - Not be intersecting any other tiles
        - Not be adjacent to any of the player's other pieces
        - Be diagonally attached to one of the player's pieces or their corner

        Return True if the move is legal or False otherwise.
        """
        piece = self.piece_list.getPiece(move.piece)
        attached_corner = False
        
        if player == 0:
            corner_x = self.board_w-1
            corner_y = 0
        elif player == 1:
            corner_x = 0
            corner_y = 0
        elif player == 2:
            corner_x = 0
            corner_y = self.board_h-1
        else: #player == 3
            corner_x = self.board_w-1
            corner_y = self.board_h-1

        for t in range(piece.getNumTiles()):
            (x,y) = piece.getTile(t, move.x, move.y, move.rot, move.flip)

            # Make sure tile in bounds
            if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
                return False

            # Make sure tile isn't intersecting other pieces
            if self._state[y][x] != -1:
                return False

            # Make sure tile isn't next to own pieces
            if x > 0 and self._state[y][x-1] == player:
                return False
            if x < self.board_w-1 and self._state[y][x+1] == player:
                return False
            if y > 0 and self._state[y-1][x] == player:
                return False
            if y < self.board_h-1 and self._state[y+1][x] == player:
                return False

            # Check if attached at corner
            if x > 0 and y > 0 and \
                self._state[y-1][x-1] == player:
                attached_corner = True
            elif x > 0 and y < self.board_h-1 and \
                self._state[y+1][x-1] == player:
                attached_corner = True
            elif x < self.board_w-1 and y < self.board_h-1 and \
                self._state[y+1][x+1] == player:
                attached_corner = True
            elif x < self.board_w-1 and y > 0 and \
                self._state[y-1][x+1] == player:
                attached_corner = True
            elif x == corner_x and y == corner_y:
                attached_corner = True
        return attached_corner

    def getState(self, x, y):
        return self._state[y][x]
