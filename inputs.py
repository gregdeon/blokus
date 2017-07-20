from board import Move, Board

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

        # Get a list of unique (x, y) points that might be legal
        # Check for all legal diagonal points and consider all points in a 
        # radius-2 box around them
        xy_list = []
        for x in range(0, 20):
            for y in range(0, 20):
                if not board.checkTileLegal(player, x, y):
                    continue
                if board.checkTileAttached(player, x, y):
                    min_x = max(0, x-2)
                    max_x = min(20, x+3)
                    min_y = max(0, y-2)
                    max_y = min(20, y+3)
                    for xi in range(min_x, max_x):
                        for yi in range(min_y, max_y):
                            xy_list.append((xi, yi))
        xy_list = sorted(set(xy_list))

        # Generate all legal moves
        move_list = []
        for piece in range(0, 21):
            if not pieces[player][piece]:
                continue
            for (x, y) in xy_list:
                for rot in range(0, 4):
                    for flip in [False, True]:
                        new_move = Move(piece, x, y, rot, flip)
                        if board.checkMoveValid(player, new_move):
                            move_list.append(new_move)

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

