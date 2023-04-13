
from python_S6_V2.library.src.othello.game.renderers import Renderer
from python_S6_V2.library.src.othello.logic.models import GameState

class ConsoleRenderer(Renderer):

    def showConsoleGameBoard(self, gameState : GameState):
        print("0 | 1 | 2 | 3 | 4 | 5 | 6 | 7")
        print("_______________________________")
        for i in range(8):
            print(" "+str(i)+" | "+" | ".join(["W" if value == 0 else 'B' if value == 1 else " " for value in gameState.grid.cells[i,:]]))
            print("_______________________________")