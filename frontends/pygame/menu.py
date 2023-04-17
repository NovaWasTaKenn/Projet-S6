from library.src.othello.game.engine import Othello

from frontends.pygame.renderer import PyGameRenderer
from frontends.pygame.player import PyGamePlayer
from library.src.othello.logic.models import Pawn


def main() -> None:
    Othello(PyGamePlayer(Pawn.WHITE), PyGamePlayer(Pawn.BLACK), PyGameRenderer()).play()