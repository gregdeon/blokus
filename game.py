
class Display(object):
    """Display class defines an interface for the game engine to draw the
    game state onto the screen.

    Child classes can use game engine data to draw the game onto the
    command line, on a GUI, etc...
    """

    display_error_string = "Error: using base display class"

    def drawBoard(self, engine):
        raise NotImplementedError(display_error_string)

class CLIDisplay(Display):
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

class GameEngine(object):
    """Game engine class stores the current game state and controls when to 
    get input/draw output
    """

    board_w = 20
    board_h = 20

    def __init__(self, display):
        self.display = display

        self.turn_num = 0
        self._state = [[0 for c in range(self.board_w)] for r in range(self.board_h)]

    def _playTurn(self):
        self.turn_num += 1
        print "Starting turn %d" % self.turn_num
        print "Board state:"
        self.display.drawBoard(self)
        print "Ending turn %d" % self.turn_num

    def playGame(self):
        while self.turn_num < 10:
            self._playTurn()

    def getState(self, x, y):
        return self._state[y][x]


def main():
    disp = CLIDisplay()
    engine = GameEngine(disp)
    engine.playGame()

if __name__ == "__main__":
    main()
