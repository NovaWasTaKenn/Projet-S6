
from python_S6_V2.library.src.othello.game.players import Player
from python_S6_V2.library.src.othello.logic.models import Move, GameState
from python_S6_V2.library.src.othello.logic.exceptions import InvalidMove
from python_S6_V2.library.src.othello.logic.validators import validatePositionStr

class ConsolePlayer(Player):
    def getMove(self, gameState : GameState) -> Move: 
        
        while True:

            positionStr = input("Entrez la position où placer le pion  ex : A3")

            try:
                validatePositionStr(positionStr)
                position = positionStr.split(",").strip()
                move = Move(self.pawn, position, gameState)
            except Exception as ex:
                print(str(ex))

            return move