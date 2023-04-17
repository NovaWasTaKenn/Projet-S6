from library.src.othello.game.engine import Othello

from frontends.console.renderer import ConsoleRenderer
from frontends.console.player import ConsolePlayer
from library.src.othello.logic.models import Pawn


def main() -> None:
    Othello(ConsolePlayer(Pawn.WHITE), ConsolePlayer(Pawn.BLACK), ConsoleRenderer()).play()