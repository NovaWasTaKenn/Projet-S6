from othello.game.engine import Othello

from .renderer import ConsoleRenderer
from .player import ConsolePlayer
from othello.logic.models import Pawn


def main() -> None:
    Othello(ConsolePlayer(Pawn.WHITE), ConsolePlayer(Pawn.BLACK), ConsoleRenderer()).play()