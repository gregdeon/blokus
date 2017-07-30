from board import Move, Board
from pieces import getPieceList

class Input(object):
    """The Input class defines an interface for the game engine to get input 
    from the players

    Child classes can use GUI input, CLI input, AI, etc... to produce moves
    """

    input_error_string = "Error: using base input class"

    def getMove(self, player, board, pieces):
        """Main per-turn function.

        Arguments:
        - player: Which player you are
        - board: A Board object with the current game state
        - pieces: 4 True/False lists describing which pieces each player has left

        Return a Move object if you want to play that move or None if you want
        to pass instead. Passing will be your final move.

        If the returned Move object is illegal, then getMove() will be called
        again with the same arguments.
        """
        raise NotImplementedError(input_error_string)

class RandomInput(Input):
    """RandomInput players choose random moves (equally distributed over piece
    number, x/y, and rotation/flip)
    """
    def getMove(self, player, board, pieces):
        import random
        piece_list = getPieceList()

        """
        # Get a list of unique (x, y) points that might be legal
        xy_list = []
        for x in range(0, 20):
            for y in range(0, 20):
                if not board.checkTileLegal(player, x, y):
                    continue
                if board.checkTileAttached(player, x, y):
                    xy_list.append((x, y))

        # Generate all legal moves
        move_list = []
        for piece_id in range(0, 21):
            if not pieces[player][piece_id]:
                continue
            for rot in range(0, 4):
                for flip in [False, True]:
                    piece = piece_list.getPiece(piece_id)
                    tiles = piece.getTiles(0, 0, rot, flip)
                    for (x, y) in xy_list:
                        for t in tiles:
                            x_off = x - t[0]
                            y_off = y - t[1]
                            new_move = Move(piece_id, x_off, y_off, rot, flip)
                            if board.checkMoveValid(player, new_move):
                                move_list.append(new_move)
        """

        all_moves = board.getAllMoves(player)
        move_list = []
        for move in all_moves:
            if pieces[player][move.piece]:
                move_list.append(move)

        # Pass if there are none
        if len(move_list) == 0:
            return None

        # Otherwise, pick a random move
        else:
            n = random.randint(0, len(move_list) - 1)
            return move_list[n]


class CLIInput(Input):
    """The CLIInput class gets moves from the command line
    """
    def getMove(self, player, engine):
        # TODO
        raise NotImplementedError("TODO")

