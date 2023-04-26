
from othello.game.players import Player
from othello.logic.models import Move, GameState
from othello.logic.exceptions import InvalidMove
from othello.logic.validators import validatePositionStr

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