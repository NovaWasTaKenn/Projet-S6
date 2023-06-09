

import abc
# from typing import Tuple

from logic.models import Pawn, Move, GameState
from logic.validators import validatePlayerTurn


class Player(metaclass=abc.ABCMeta):
    """Classe comportant le pion"""
    def __init__(self, pawn: Pawn) -> None:
        self.pawn = pawn

    def makeMove(self, gameState : GameState) -> Move: 
        """retourne le coup s'il est valide"""
        #print("inside make move")

        if validatePlayerTurn(self, gameState):
            if move:= self.getMove(gameState):
                #print("move afterstate")
                return move


    @abc.abstractmethod
    def getMove(self, gameState: GameState) -> Move :
        """Gets the player move"""

