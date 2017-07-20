"""Classes to control the game's display (screen, GUI, etc)
"""

from board import Board

class Display(object):
    """the Display class defines an interface for the game engine to draw the
    game state onto the screen.

    Child classes can use game engine data to draw the game onto the
    command line, on a GUI, etc...
    """

    display_error_string = "Error: using base display class"

    def drawBoard(self, board):
        """Draw the board onto the screen, command line, etc
        """
        raise NotImplementedError(display_error_string)

class CLIDisplay(Display):
    """The CLIDisplay class prints the game board to the command line
    """
    def drawBoard(self, board):
        str_horiz = "+" + "-"*board.board_w + "+"

        print str_horiz
        for r in range(board.board_h):
            str_line = "|"
            for c in range(board.board_w):
                state_xy = board.getState(c, r)
                if state_xy == -1:
                    str_line += "."
                else:
                    str_line += "%d" % state_xy
            str_line += "|"
            print str_line
        print str_horiz
        print ""
