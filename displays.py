"""Classes to control the game's display (screen, GUI, etc)
"""

from board import Board
import colorama
colorama.init(autoreset=True)

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

class NoDisplay(Display):
    """The NoDisplay doesn't bother drawing the game. Useful for running many
    iterations of the game.
    """

    def drawBoard(self, board):
        pass

class CLIDisplay(Display):
    """The CLIDisplay class prints the game board to the command line
    """
    def drawBoard(self, board):
        str_horiz = "+" + "-"*board.board_w + "+"

        color_fore = [
            colorama.Fore.RED,
            colorama.Fore.YELLOW,
            colorama.Fore.GREEN,
            colorama.Fore.BLUE
        ]

        color_back = [
            colorama.Back.RED,
            colorama.Back.YELLOW,
            colorama.Back.GREEN,
            colorama.Back.BLUE
        ]

        color_reset = colorama.Style.RESET_ALL

        print str_horiz
        for r in range(board.board_h):
            str_line = "|"
            for c in range(board.board_w):
                state_xy = board.getState(c, r)
                if state_xy == -1:
                    str_line += color_reset + "."
                else:
                    p = state_xy
                    str_color = color_fore[p] + color_back[p] + "%d" % p
                    str_line += str_color
            str_line += color_reset + "|"
            print str_line
        print str_horiz
        print ""
