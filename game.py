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

    def getMove(self, player, engine):
        """
        """
        raise NotImplementedError(input_error_string)

class RandomInput(Input):
    """RandomInput players choose random moves (equally distributed over piece
    number, x/y, and rotation/flip)
    """
    def getMove(self, player, engine):
        import random

        move_list = []
        for piece in range(0, 21):
            for x in range(0, 20):
                for y in range(0, 20):
                    for rot in range(0, 4):
                        for flip in [False, True]:
                            new_move = Move(piece, x, y, rot, flip)
                            if engine.checkMoveValid(player, new_move):
                                move_list.append(new_move)
        n = random.randint(0, len(move_list) - 1)
        return move_list[n]


class CLIInput(Input):
    """The CLIInput class gets moves from the command line
    """
    def getMove(self, player, engine):
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

            move = self.inputs[p].getMove(p, self)
            self._addMove(p, move)
        print "Ending turn %d" % self.turn_num

    def checkMoveValid(self, player, move):
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
