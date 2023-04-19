from othello.game.engine import Othello

from .renderer import PyGameRenderer
from .player import PyGamePlayer
from othello.logic.models import Pawn


def main() -> None:
    Othello(PyGamePlayer(Pawn.WHITE), PyGamePlayer(Pawn.BLACK), PyGameRenderer()).play()