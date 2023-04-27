from game.engine import Othello

from renderer import PyGameRenderer
from player import PyGamePlayer, IA
from logic.models import Pawn


def main() -> None:
    Othello(PyGamePlayer(Pawn.WHITE), PyGamePlayer(Pawn.BLACK), PyGameRenderer()).play()
    #Othello(PyGamePlayer(Pawn.WHITE), IA(Pawn.BLACK), PyGameRenderer()).play()
    #Othello(IA(Pawn.WHITE), IA(Pawn.BLACK), PyGameRenderer()).play()
