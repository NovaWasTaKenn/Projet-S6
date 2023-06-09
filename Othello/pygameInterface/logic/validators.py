from __future__ import annotations
from typing import TYPE_CHECKING

import importlib
import numpy as np
import re
from logic.exceptions import InvalidGameState,InvalidGrid,InvalidMove


if TYPE_CHECKING:
    from logic.models import Grid, GameState, Move
    from game.players import Player

def validateMove(move:Move) -> bool:
    """Valide un mouvement en fonction de l'état du jeu et de la grille"""

    Models = importlib.import_module("logic.models")

    cellEmpty = move.beforeState.grid.cells[move.index[0], move.index[1]] == 2

    if not cellEmpty :  raise InvalidMove("The target cell is not empty")

    #print(move.index[0])
    #print(move.index[1])
    #print(move.pawn.other)
    #print(Models.Pawn(move.beforeState.grid.cells[move.index[0], move.index[1]+1]))

    neighbourAdversary = (
        (move.index[0]-1 >= 0 and move.beforeState.grid.cells[move.index[0]-1, move.index[1]] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0]-1, move.index[1]]) == move.pawn.other)
        or (move.index[0]+1 < 8 and move.beforeState.grid.cells[move.index[0]+1, move.index[1]] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0]+1, move.index[1]]) == move.pawn.other)
        or (move.index[1]-1 >= 0 and move.beforeState.grid.cells[move.index[0], move.index[1]-1] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0], move.index[1]-1]) == move.pawn.other)
        or (move.index[1]+1 < 8 and move.beforeState.grid.cells[move.index[0], move.index[1]+1] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0], move.index[1]+1]) == move.pawn.other)
        
        or (move.index[0]+1 < 8 and move.index[1]+1 < 8 
            and move.beforeState.grid.cells[move.index[0]+1, move.index[1]+1] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0]+1, move.index[1]+1]) == move.pawn.other)
        or (move.index[0]-1 < 8 and move.index[1]-1 < 8 
            and move.beforeState.grid.cells[move.index[0]-1, move.index[1]-1] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0]-1, move.index[1]-1]) == move.pawn.other)
        or (move.index[0]-1 < 8 and move.index[1]+1 < 8 
            and move.beforeState.grid.cells[move.index[0]-1, move.index[1]+1] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0]-1, move.index[1]+1]) == move.pawn.other)
        or (move.index[0]+1 < 8 and move.index[1]-1 < 8 
            and move.beforeState.grid.cells[move.index[0]+1, move.index[1]-1] != 2 and Models.Pawn(move.beforeState.grid.cells[move.index[0]+1, move.index[1]-1]) == move.pawn.other)

        )
    
    if not neighbourAdversary: raise InvalidMove("No adversay in the neighbouring cells")
    
    hasSandwiches = len(move.sandwiches) > 0

    if not hasSandwiches : raise InvalidMove("Placing the pawn here does not create flip an adversary pawn")

#def validateGameState(gameState: GameState):
#    try:    
#        validateGrid(gameState.grid)
#    except InvalidGrid as e:
#        raise InvalidGameState(f"Le grid n'est pas valide : {str(e)}")
#    if gameState.currentTurn <= 100 and gameState.currentTurn > 0 : return True
#    raise InvalidGameState("Le nombre de tour est supérieur à 60 ou inférieur à 0")



def validateGrid(grid: Grid):
    """Valide une grille de jeu selon la valeur des cellules"""
    if all([i in [0,1,2] for i in np.unique(grid.cells)]) : return True
    raise InvalidGrid()

def validatePositionStr(position : str):
    """Valide une position donnée par un humain sous la forme d'une chaine de caractère"""
    if len(re.findall("^[abcdefghABCDEFGH][1-8]$", position)) == 0 : return True
    raise ValueError("Veuillez saisir la position sous le format : i,j ")

def validatePosition(position : tuple[int, int]):
    """Valide une position donnée sous la forme d'un tuple de int"""
    if position[0] < 8 and position[0] >= 0 and position[1] < 8 and position[1] >= 0: return True
    raise ValueError("La position est en dehors du plateau")

def validatePlayerTurn(player: Player, gameState: GameState):
    """Valide que le joueur peut jouer"""
    #print("player :", player.pawn.value)
    #print("gameState current turn :", gameState.currentTurn)
    #print("gameState current pawn : ", gameState.currentPawn)
    #print("equality : ", player.pawn == gameState.currentPawn)

    if player.pawn == gameState.currentPawn: return True
    raise InvalidMove("Not your turn")
