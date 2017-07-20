from board import Move, Board

class Input(object):
    """The Input class defines an interface for the game engine to get input 
    from the players

    Child classes can use GUI input, CLI input, AI, etc... to produce moves
    """

    input_error_string = "Error: using base input class"

    def getMove(self, player, engine):
        """
        """
        raise NotImplementedError(input_error_string)

class RandomInput(Input):
    """RandomInput players choose random moves (equally distributed over piece
    number, x/y, and rotation/flip)
    """
    def getMove(self, player, board):
        import random

        move_list = []
        for piece in range(0, 21):
            for x in range(0, 20):
                for y in range(0, 20):
                    for rot in range(0, 4):
                        for flip in [False, True]:
                            new_move = Move(piece, x, y, rot, flip)
                            if board.checkMoveValid(player, new_move):
                                move_list.append(new_move)
        if len(move_list) == 0:
            return None
        else:
            n = random.randint(0, len(move_list) - 1)
            return move_list[n]


class CLIInput(Input):
    """The CLIInput class gets moves from the command line
    """
    def getMove(self, player, engine):
        # TODO
        raise NotImplementedError("TODO")

