from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
import re

if TYPE_CHECKING:
    from othello.logic.models import Grid, GameState, Move
    from othello.logic.exceptions import *

def validateMove(move:Move) -> bool:
    
        cellEmpty = move.beforeState.grid[move.index[0], move.index[1]] == 2
        neighbourAdversary = (
            (move.index[0]-1 >= 0 and move.beforeState.grid[move.index[0]-1, move.index[1]] == move.pawn.other)
            or (move.index[0]+1 < 8 and move.beforeState.grid[move.index[0]+1, move.index[1]] == move.pawn.other)
            or (move.index[1]-1 >= 0 and move.beforeState.grid[move.index[0], move.index[1]-1] == move.pawn.other)
            or (move.index[1]+1 < 8 and move.beforeState.grid[move.index[0], move.index[1]+1] == move.pawn.other)
            )
           
        hasSandwiches = len(move.sandwiches) > 0

        if cellEmpty and neighbourAdversary and hasSandwiches: return True
        elif not cellEmpty : raise InvalidMove("The target cell is not empty")
        elif not neighbourAdversary : raise InvalidMove("No adversay in the neighbouring cells")
        elif not hasSandwiches : raise InvalidMove("Placing the pawn here does not create flip an adversary pawn")

def validateGameState(gameState: GameState):
    try:    
        validateGrid(gameState.grid)
    except InvalidGrid as e:
        raise InvalidGameState(f"Le grid n'est pas valide : {str(e)}")
    if gameState.currentTurn <= 60 and gameState.currentTurn > 0 : return True
    raise InvalidGameState("Le nombre de tour est supérieur à 60 ou inférieur à 0")



def validateGrid(grid: Grid):
    if np.unique(grid.cells) == [0,1,2]: return True
    raise InvalidGrid

def validatePositionStr(position : str):
     if len(re.findall("^[0-9],[0-9]$", position)) == 0 : return True
     raise ValueError("Veuillez saisir la position sous le format : i,j ")
