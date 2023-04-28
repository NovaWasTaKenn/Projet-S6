from game.engine import Othello

from renderer import PyGameRenderer
from player import PyGamePlayer, IA
from logic.models import Pawn
from logic import settings


def main() -> None:
    #Othello(PyGamePlayer(Pawn.WHITE), PyGamePlayer(Pawn.BLACK), PyGameRenderer()).play()
    #Othello(PyGamePlayer(Pawn.WHITE), IA(Pawn.BLACK, 3, 7), PyGameRenderer()).play()
    settings.depth = 3
    settings.endGameDepth = 6
    Othello(IA(Pawn.WHITE), IA(Pawn.BLACK), PyGameRenderer()).play()
