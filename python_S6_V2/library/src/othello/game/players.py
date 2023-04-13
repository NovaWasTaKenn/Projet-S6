

import abc

from othello.logic.models import Pawn, Move, GameState
from othello.logic.exceptions import InvalidGameState,InvalidGrid,InvalidMove


class Player(metaclass=abc.ABCMeta):
    def __init__(self, pawn: Pawn) -> None:
        self.pawn = pawn

    def makeMove(self, gameState : GameState) -> GameState: 
        if self.pawn is gameState.currentPawn:
            if move:= self.getMove(gameState):
                return move.afterState
        else: raise InvalidMove("Not your turn")
            
    @abc.abstractmethod
    def getMove(self, gameState: GameState) -> Move | None:
        """Gets the player move"""

