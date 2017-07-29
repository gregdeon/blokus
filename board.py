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

    TODO: improve this by adding more data structures to speed up checks
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

        for t in range(piece.getNumTiles()):
            (x,y) = piece.getTile(t, move.x, move.y, move.rot, move.flip)

            # If any tile is illegal, this move isn't valid
            if not self.checkTileLegal(player, x, y):
                return False

            if self.checkTileAttached(player, x, y):
                attached_corner = True

            # If at least one tile is attached, this move is valid
        return attached_corner

    def checkTileLegal(self, player, x, y):
        """Check if it's legal for <player> to place one tile at (<x>, <y>).

        Legal tiles:
        - Are in bounds
        - Don't intersect with existing tiles
        - Aren't adjacent to the player's existing tiles

        Returns True if legal or False if not.

        TODO: this should be a fast lookup
        """
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

        return True

    def checkTileAttached(self, player, x, y):
        """Check if (<x>, <y>) is diagonally attached to <player>'s moves.

        Note that this does not check if this move is legal.

        Returns True if attached or False if not.

        TODO: make this a fast lookup
        """
        # Find which corner the player owns
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

        if x > 0 and y > 0 and \
            self._state[y-1][x-1] == player:
            return True
        elif x > 0 and y < self.board_h-1 and \
            self._state[y+1][x-1] == player:
            return True
        elif x < self.board_w-1 and y < self.board_h-1 and \
            self._state[y+1][x+1] == player:
            return True
        elif x < self.board_w-1 and y > 0 and \
            self._state[y-1][x+1] == player:
            return True
        elif x == corner_x and y == corner_y:
            return True

    def getState(self, x, y):
        return self._state[y][x]
