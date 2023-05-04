import pygame as pg
from game.players import Player
from logic.models import *
from logic.exceptions import *
from game.engine import Othello, timer, debug

nbFeuilles = 0

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
                    #print("position :", position)
                    move = Move(gameState.currentPawn, position, gameState)
                    
                except Exception as ex:
                    print(str(ex))

                return move
            

                

class IA(Player):
    

    def getMove(self, gameState: GameState) -> Move:
        # Implémente l'algorithme Minimax avec élagage Alpha-Bêta

        #Compte le nb de feuilles parcourues par minMax
        
        global nbFeuilles

        nbFeuilles = 0

        rslt = self.alphaBetaSearch(gameState)

        print()
        print(" ----> Nombre de feuilles parcouru : ", nbFeuilles)
        print()

        return rslt
    
    def alphaBetaSearch(self, gameState: GameState) -> Move:
        # Détermine la profondeur maximale de recherche

        depth = settings.depth if gameState.gameStage != GameStage.endGame else settings.endGameDepth

        #print()
        #print(" ------>  Profondeur : ",depth)
        #print()

        # Appelle MAX-VALUE avec des arguments appropriés
        bestMove = None
        bestUtility = -float("inf")
        alpha = -float("inf")
        beta = float("inf")
        #print("Possible moves : ", gameState.possibleMoves)
        for move in gameState.possibleMoves:
            utility = self.minValue(self.getResult(move), alpha, beta, depth - 1)
            if utility > bestUtility:
                bestUtility = utility
                bestMove = move
            alpha = max(alpha, bestUtility)
            if alpha >= beta:
                break  # coupure alpha-beta
        return bestMove

    def maxValue(self, gameState: GameState, alpha: float, beta: float, depth: int) -> float:

        global nbFeuilles

        if depth == 0 or gameState.possibleMoves == []:
            nbFeuilles += 1
            return self.advanced_heuristic(gameState)
        v = -float("inf")

        #print("Possible moves : ", gameState.possibleMoves)
        for move in gameState.possibleMoves:
            v = max(v, self.minValue(move.afterState, alpha, beta, depth - 1))
            if v >= beta:
                #print("élaguage v >= beta")
                return v
            alpha = max(alpha, v)
        return v

    def minValue(self, gameState: GameState, alpha: float, beta: float, depth: int) -> float:

        global nbFeuilles

        if depth == 0 or gameState.possibleMoves == []:
            nbFeuilles += 1
            return self.advanced_heuristic(gameState)
        v = float("inf")

        #print("Possible moves : ", gameState.possibleMoves)
        for move in gameState.possibleMoves:
            v = min(v, self.maxValue(move.afterState, alpha, beta, depth - 1))
            if v <= alpha:
                #print("élaguage v >= alpha")
                return v
            beta = min(beta,v)
        return v

    def getResult(self,  move: Move) -> GameState:
        return move.afterState

    def advanced_heuristic(self, state: GameState) -> float:
        mobility_weight = 0.5
        stability_weight = 0.4
        center_weight = 0.25

        current_pawn = state.currentPawn

        current_mobility = len(state.possibleMoves)
        other_mobility = 0

        if state.currentTurn+1 <= 60 :
            other_mobility = len(GameState(state.grid, state.currentTurn + 1,state.currentPawn.other).possibleMoves) 


        current_stability, other_stability, current_center, other_center = state.grid.compute_stability_and_center_scores()
                
        score = (current_mobility - other_mobility) * mobility_weight
        score += (current_stability - other_stability) * stability_weight
        score += (current_center - other_center) * center_weight

        return score