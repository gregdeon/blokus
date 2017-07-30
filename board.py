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
    - _legal: a 4 x 2D array. _legal[player][y][x] is True iff (x,y) is not
      on another player's piece or adjacent to a player's own piece
    - _connected: a 4 x 2D array. _connected[player][y][x] is True iff (x,y) is 
      diagonally connected to another one of the player's tiles
    - piece_list: A PieceList object (probably shared with the game engine) to
      help understand the moves
    """

    def __init__(self, board_w, board_h, piece_list):
        self.board_w = board_w
        self.board_h = board_h

        self.piece_list = piece_list
        self._state = [[-1 for c in range(board_w)] for r in range(board_h)]
        
        # Write down whether each (x,y) position is legal to play for each player
        # Default is True
        self._legal = [
            [
                [True for c in range(board_w)
            ] for r in range(board_h)] 
        for p in range(4)]

        # Write down whether each (x,y) is diagonally attached
        # Default is False except the corners
        self._connected = [
            [
                [False for c in range(board_w)
            ] for r in range(board_h)] 
        for p in range(4)]

        # List of moves attached at every (x,y)
        self._moves = [
            [
                [None for c in range(board_w)]
            for r in range(board_h)]
        for p in range(4)]

        # Set up initial corners for each player now
        corners = [
            (0, 0),
            (0, self.board_w-1),
            (self.board_h-1, self.board_w-1),
            (self.board_h-1, 0),
        ]

        for p in range(4):
            c_x = corners[p][0]
            c_y = corners[p][1]

            x_min = max(0, c_x - 2)
            x_max = min(board_w, c_x+3)

            y_min = max(0, c_y - 2)
            y_max = min(board_h, c_y+3)

            c_x = corners[p][0]
            c_y = corners[p][1]
            self._connected[p][c_y][c_x] = True

            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    move_list = []
                    for piece_id in range(0, 21):
                        for rot in range(0, 4):
                            for flip in [False, True]:
                                new_move = Move(piece_id, x, y, rot, flip)
                                if self.checkMoveValid(p, new_move):
                                    move_list.append(new_move)
                    self._moves[p][y][x] = move_list

    def addMove(self, player, move):
        """Try to add <player>'s <move>.

        If the move is legal, the board state is updated; if it's not legal, a
        ValueError is raised.

        Returns the number of tiles placed on the board.
        """
        if not self.checkMoveValid(player, move):
            raise ValueError("Move is not allowed")

        piece = self.piece_list.getPiece(move.piece)

        # Update internal state for each tile
        for t in range(piece.getNumTiles()):
            (x,y) = piece.getTile(t, move.x, move.y, move.rot, move.flip)
            self._state[y][x] = player

            # Nobody can play on this square
            for p in range(4):
                self._legal[p][y][x] = False

            # This player can't play next to this square
            adjs = [
                (x, y-1),
                (x, y+1),
                (x-1, y),
                (x+1, y)
            ]

            for a in adjs:
                a_x = a[0]
                a_y = a[1]
                if a_x >= 0 and a_x < self.board_w and \
                a_y >= 0 and a_y < self.board_h:
                    a_x = a[0]
                    a_y = a[1]
                    if self._legal[player][a_y][a_x]:
                        self._legal[player][a_y][a_x] = False

            # The diagonals are now attached
            diags = [
                (x-1, y-1),
                (x+1, y-1),
                (x+1, y+1),
                (x-1, y+1)
            ]

            for d in diags:
                d_x = d[0]
                d_y = d[1]

                if d_x >= 0 and d_x < self.board_w and \
                d_y >= 0 and d_y < self.board_h:
                    if not self._connected[player][d_y][d_x]:
                        self._connected[player][d_y][d_x] = True

        # Update the lists of moves for each player around this area
        self.updateState(player, move.x, move.y)

        return piece.getNumTiles()

    def updateState(self, player, x, y, ):
        """Update the lists of legal moves for each player in this area.
        """

        x_min = max(0, x - 5)
        x_max = min(self.board_w, x+6)

        y_min = max(0, y - 5)
        y_max = min(self.board_h, y+6)

        for p in range(4):
            for xi in range(x_min, x_max):
                for yi in range(y_min, y_max):
                    if not self._legal[p][yi][xi]:
                        self._moves[p][yi][xi] = []
                    elif p == player and self._moves[p][yi][xi] is None:
                        new_move_list = []
                        for piece_id in range(0, 21):
                            for rot in range(0, 4):
                                for flip in [False, True]:
                                    new_move = Move(piece_id, xi, yi, rot, flip)
                                    if self.checkMoveValid(p, new_move):
                                        new_move_list.append(new_move)
                        if len(new_move_list) > 0:
                            self._moves[p][yi][xi] = new_move_list

                    elif self._moves[p][yi][xi] is not None:
                        new_move_list = []
                        for move in self._moves[p][yi][xi]:
                            if self.checkMoveValid(p, move):
                                new_move_list.append(move)
                        self._moves[p][yi][xi] = new_move_list

    def getAllMoves(self, player):
        move_list = []
        for x in range(0, self.board_w):
            for y in range(0, self.board_h):
                if self._moves[player][y][x] is not None:
                    move_list += self._moves[player][y][x]
        return move_list

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

        xy_list = piece.getTiles(move.x, move.y, move.rot, move.flip)
        for (x,y) in xy_list:
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
        """

        # Make sure tile in bounds
        if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
            return False

        # Otherwise, it's in the lookup table
        return self._legal[player][y][x]

    def checkTileAttached(self, player, x, y):
        """Check if (<x>, <y>) is diagonally attached to <player>'s moves.

        Note that this does not check if this move is legal.

        Returns True if attached or False if not.
        """

        # Make sure tile in bounds
        if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
            return False

        # Otherwise, it's in the lookup table
        return self._connected[player][y][x]



    def getState(self, x, y):
        return self._state[y][x]
