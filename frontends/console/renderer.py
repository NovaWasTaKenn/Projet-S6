
from library.src.othello.game.renderers import Renderer
from library.src.othello.logic.models import GameState

class ConsoleRenderer(Renderer):

    def showConsoleGameBoard(self, gameState : GameState):
        print("A | B | C | D | E | F | G | H")
        print("_______________________________")
        for i in range(8):
            print(" "+str(i)+" | "+" | ".join(["W" if value == 0 else 'B' if value == 1 else " " for value in gameState.grid.cells[i,:]]))
            print("_______________________________")