import sys

from display import CLIDisplay 
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

class Input(object):
    """The Input class defines an interface for the game engine to get input 
    from the players

    Child classes can use GUI input, CLI input, AI, etc... to produce moves
    """

    input_error_string = "Error: using base input class"

    def getMove(self, engine):
        """
        """
        raise NotImplementedError(input_error_string)

class RandomInput(Input):
    """RandomInput players choose random moves (equally distributed over piece
    number, x/y, and rotation/flip)
    """
    def getMove(self, engine):
        import random
        piece = random.randint(0, 20)
        x = random.randint(5, 15)
        y = random.randint(5, 15)
        rot = random.randint(0, 3)
        flip = True if random.random() > 0.5 else False

        return Move(piece, x, y, rot, flip)


class CLIInput(Input):
    """The CLIInput class gets moves from the command line
    """
    def getMove(self, engine):
        # TODO
        raise NotImplementedError("TODO")

class GameEngine(object):
    """Game engine class stores the current game state and controls when to 
    get input/draw output
    """

    board_w = 20
    board_h = 20

    def __init__(self, display, inputs):
        self.display = display
        if len(inputs) != 4:
            print "Error: game engine was provided with %d inputs" % len(inputs)
            print "Need 4 input sources"
            sys.exit(1)
        self.inputs = inputs

        self.piece_list = PieceList("valid_pieces.txt")

        self.turn_num = 0
        self._state = [[-1 for c in range(self.board_w)] for r in range(self.board_h)]

    def _addMove(self, player, move):
        if not self.checkMoveValid(player, move):
            raise ValueError("Move is not allowed")

        piece = self.piece_list.getPiece(move.piece)
        for t in range(piece.getNumTiles()):
            (x,y) = piece.getTile(t, move.x, move.y, move.rot, move.flip)
            self._state[y][x] = player


    def _playTurn(self):
        self.turn_num += 1
        print "Starting turn %d" % self.turn_num

        for p in range(4):
            print "Board state:"
            self.display.drawBoard(self)

            move = self.inputs[p].getMove(self)
            self._addMove(p, move)
        print "Ending turn %d" % self.turn_num

    def checkMoveValid(self, player, move):
        piece = self.piece_list.getPiece(move.piece)
        for t in range(piece.getNumTiles()):
            (x,y) = piece.getTile(t, move.x, move.y, move.rot, move.flip)
            if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
                return False
            # TODO: check for:
            # - intersecting other pieces
            # - adjacent to player's pieces
            # - not attached at corner
        return True

    def playGame(self):
        while self.turn_num < 10:
            self._playTurn()

    def getState(self, x, y):
        return self._state[y][x]


def main():
    disp = CLIDisplay()
    inputs = [RandomInput() for p in range(4)]
    engine = GameEngine(disp, inputs)
    engine.playGame()

if __name__ == "__main__":
    main()
