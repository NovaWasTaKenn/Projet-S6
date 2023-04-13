from python_S6_V2.library.src.othello.game.engine import Othello

from python_S6_V2.frontends.console.renderer import ConsoleRenderer
from python_S6_V2.frontends.console.player import ConsolePlayer
from python_S6_V2.library.src.othello.logic.models import Pawn


def main() -> None:
    Othello(ConsolePlayer(Pawn.WHITE), ConsolePlayer(Pawn.BLACK), ConsoleRenderer()).play()