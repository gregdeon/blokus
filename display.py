"""Classes to control the game's display (screen, GUI, etc)
"""

class Display(object):
    """the Display class defines an interface for the game engine to draw the
    game state onto the screen.

    Child classes can use game engine data to draw the game onto the
    command line, on a GUI, etc...
    """

    display_error_string = "Error: using base display class"

    def drawBoard(self, engine):
        """Draw the board onto the screen, command line, etc
        """
        raise NotImplementedError(display_error_string)

class CLIDisplay(Display):
    """The CLIDisplay class prints the game board to the command line
    """
    def drawBoard(self, engine):
        str_horiz = "+" + "-"*engine.board_w + "+"

        print str_horiz
        for r in range(engine.board_h):
            str_line = "|"
            for c in range(engine.board_w):
                state_xy = engine.getState(c, r)
                if state_xy == 0:
                    str_line += "."
                else:
                    str_line += "%d" % state_xy
            str_line += "|"
            print str_line
        print str_horiz
        print ""
