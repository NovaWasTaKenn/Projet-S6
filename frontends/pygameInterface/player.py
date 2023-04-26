
import pygame as pg
from game.players import Player
from logic.models import *
from logic.exceptions import *

DEPTH = 4

class PyGamePlayer(Player):
    
    def getMove(self, gameState: GameState) -> Move:

        for event in pg.event.get():
                
                
                if event.type == pg.QUIT:
                    raise StopGame("Player closed the window")
                elif event.type == pg.MOUSEBUTTONUP:
                    move = None

                    try:
                        position = pg.mouse.get_pos()
                        position = ((position[0]-30)//60, (position[1]-30)//60)
                        print("position :", position)
                        move = Move(gameState.currentPawn, position, gameState)
                        
                    except Exception as ex:
                         print(str(ex))

                    return move
                

class IA(Player):

    def getMove(self, gameState: GameState) -> Move:
        """if self.level == 1:
            return self.getMoveLevel1(gameState)
        elif self.level == 2:
            return self.getMoveLevel2(gameState)
        elif self.level == 3:
            return self.getMoveLevel3(gameState)
        else:
            return None
        """
        return self.getMoveLevel3(gameState)
    """def getMoveLevel1(self, gameState: GameState) -> Move:
        # Retourne un coup valide aléatoire
        return self.getRandomMove(gameState)

    def getMoveLevel2(self, gameState: GameState) -> Move:
        # Retourne le coup avec la valeur d'utilité maximale
        return self.getBestMove(gameState)
    """
    def getMoveLevel3(self, gameState: GameState) -> Move:
        # Implémente l'algorithme Minimax avec élagage Alpha-Bêta
        return self.alphaBetaSearch(gameState)

    def getRandomMove(self, gameState: GameState) -> Move:
        moves = self.getPossibleMoves(gameState)
        if moves:
            return moves[0]
        else:
            return None

    def getBestMove(self, gameState: GameState) -> Move:
        moves = gameState.possibleMoves
        bestMove = None
        bestUtility = -float("inf")
        for move in moves:
            utility = self.evaluateMove(move, gameState)
            if utility > bestUtility:
                bestUtility = utility
                bestMove = move
        return bestMove

    def alphaBetaSearch(self, gameState: GameState) -> Move:
        # Détermine la profondeur maximale de recherche
        depth = DEPTH

        # Appelle MAX-VALUE avec des arguments appropriés
        bestMove = None
        bestUtility = -float("inf")
        alpha = -float("inf")
        beta = float("inf")
        for move in gameState.possibleMoves:
            utility = self.minValue(self.getResult(
                gameState, move), alpha, beta, depth - 1)
            if utility > bestUtility:
                bestUtility = utility
                bestMove = move
            alpha = max(alpha, bestUtility)
        return bestMove

    def maxValue(self, gameState: GameState, alpha: float, beta: float, depth: int) -> float:
        if depth == 0 or self.isTerminal(gameState):
            return self.utility(gameState)
        v = -float("inf")
        for move in gameState.possibleMoves:
            v = max(v, self.minValue(self.getResult(
                gameState, move), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def minValue(self, gameState: GameState, alpha: float, beta: float, depth: int) -> float:
        if depth == 0 or self.isTerminal(gameState):
            return self.utility(gameState)
        v = float("inf")
        for move in self.getPossibleMoves(gameState):
            v = min(v, self.maxValue(self.getResult(
                gameState, move), alpha, beta, depth - 1))
            if v <= alpha:
                return
