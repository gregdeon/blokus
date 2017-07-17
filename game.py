import sys

from display import CLIDisplay 
from pieces import PieceList

class Move(object):
    """A Move describes how one of the players is going to spend their move.

    It contains:
    - Piece: the ID of the piece being used
    - x/y: the center coordinates of the piece [0-19)
    - Rotation: how many times the piece should be rotated CW [0-3]
    """
    def __init__(self, piece=0, x=0, y=0, rot=0):
        self.piece = piece
        self.x = x
        self.y = y
        self.rot = rot

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

        self.piece_list = PieceList("pieces.txt")

        self.turn_num = 0
        self._state = [[0 for c in range(self.board_w)] for r in range(self.board_h)]

    def _playTurn(self):
        self.turn_num += 1
        print "Starting turn %d" % self.turn_num

        for p in range(4):
            print "Board state:"
            self.display.drawBoard(self)

            move = self.inputs[p].getMove(self)
            print "Ending turn %d" % self.turn_num

    def playGame(self):
        while self.turn_num < 10:
            self._playTurn()

    def getState(self, x, y):
        return self._state[y][x]


def main():
    disp = CLIDisplay()
    inputs = [CLIInput() for p in range(4)]
    engine = GameEngine(disp, inputs)
    engine.playGame()

if __name__ == "__main__":
    pl = PieceList("pieces.txt")
    #main()
