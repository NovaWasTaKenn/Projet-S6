from python_S6_V2.library.src.othello.game.engine import Othello

from python_S6_V2.frontends.pygame.renderer import PyGameRenderer
from python_S6_V2.frontends.pygame.player import PyGamePlayer
from python_S6_V2.library.src.othello.logic.models import Pawn


def main() -> None:
    Othello(PyGamePlayer(Pawn.WHITE), PyGamePlayer(Pawn.BLACK), PyGameRenderer()).play()