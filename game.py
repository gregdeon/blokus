import sys

from displays import CLIDisplay 
from inputs import RandomInput
from pieces import PieceList
from board import Move, Board

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
        self.passed = [False]*4
        self.score = [0]*4
        self.board = Board(self.board_w, self.board_h, self.piece_list)

    def _playTurn(self):
        """Play a single round of turns.

        Check for empty moves from the inputs (signalling passes) and ask for 
        new moves if illegal moves are provided.
        """
        self.turn_num += 1
        print "Starting turn %d" % self.turn_num

        for p in range(4):
            if self.passed[p]:
                continue

            print "Board state:"
            self.display.drawBoard(self.board)

            while True:
                move = self.inputs[p].getMove(p, self.board)
                if move is None:
                    self.passed[p] = True
                    break
                try:
                    self.score[p] += self.board.addMove(p, move)
                    break
                except ValueError as e:
                    print "Error: move is illegal. Try again:"

        print "Ending turn %d" % self.turn_num

    def _allPlayersPassed(self):
        """Return True if all players have passed.
        """
        for p in range(4):
            if not self.passed[p]:
                return False
        return True

    def _print_scores(self):
        for p in range(4):
            print "Player %d: %d pts" % (p+1, self.score[p])

    def playGame(self):
        while not self._allPlayersPassed():
            self._playTurn()
        
        self._print_scores()


def main():
    disp = CLIDisplay()
    inputs = [RandomInput() for p in range(4)]
    engine = GameEngine(disp, inputs)
    engine.playGame()

if __name__ == "__main__":
    main()
