import copy
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
        # Implémente l'algorithme Minimax avec élagage Alpha-Bêta
        return self.alphaBetaSearch(gameState)
    
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
        if depth == 0 or gameState.possibleMoves == []:
            return self.advanced_heuristic(gameState)
        v = -float("inf")
        for move in gameState.possibleMoves:
            v = max(v, self.minValue(move.afterState, alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def minValue(self, gameState: GameState, alpha: float, beta: float, depth: int) -> float:
        if depth == 0 or gameState.possibleMoves == []:
            return self.advanced_heuristic(gameState)
        v = float("inf")
        for move in gameState.possibleMoves:
            v = min(v, self.maxValue(move.afterState, alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta,v)
        return v

    def getResult(self, gameState: GameState, move: Move) -> GameState:
        return move.afterState


    def advanced_heuristic(self, state: GameState) -> float:
        mobility_weight = 0.5
        stability_weight = 0.25
        center_weight = 0.25

        current_pawn = state.currentPawn
        other_pawn = current_pawn.other

        current_mobility = len(state.possibleMoves)
        other_mobility = len(GameState(state.grid, state.currentTurn + 1, state.endGameDepth,state.currentPawn.other).possibleMoves)

        current_stability = 0
        other_stability = 0
        stable_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        stable_positions += [(0, i) for i in range(2, 6)] + \
            [(7, i) for i in range(2, 6)]
        stable_positions += [(i, 0) for i in range(2, 6)] + \
            [(i, 7) for i in range(2, 6)]
        stable_positions += [(2, 2), (2, 5), (5, 2), (5, 5)]

        for i in range(8):
            for j in range(8):
                if state.grid.cells[i, j] == current_pawn.value:
                    if (i, j) in stable_positions:
                        current_stability += 1
                elif state.grid.cells[i, j] == other_pawn.value:
                    if (i, j) in stable_positions:
                        other_stability += 1

        current_center = 0
        other_center = 0
        for i in range(8):
            for j in range(8):
                if state.grid.cells[i, j] == current_pawn.value:
                    if (2 <= i <= 5) and (2 <= j <= 5):
                        current_center += 1
                elif state.grid.cells[i, j] == other_pawn.value:
                    if (2 <= i <= 5) and (2 <= j <= 5):
                        other_center += 1

        score = (current_mobility - other_mobility) * mobility_weight
        score += (current_stability - other_stability) * stability_weight
        score += (current_center - other_center) * center_weight

        return score