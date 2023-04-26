

import abc

from logic.models import Pawn, Move, GameState
from logic.validators import validatePlayerTurn


class Player(metaclass=abc.ABCMeta):
    def __init__(self, pawn: Pawn) -> None:
        self.pawn = pawn

    def makeMove(self, gameState : GameState) -> GameState: 

        #print("inside make move")

        if validatePlayerTurn(self, gameState):
            if move:= self.getMove(gameState):
                #print("move afterstate")
                return move.afterState


    @abc.abstractmethod
    def getMove(self, gameState: GameState) -> Move :
        """Gets the player move"""

