from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from othello.logic.validators import *
import enum
import numpy as np


class Pawn(str, enum.Enum):
    BLACK: 1
    WHITE: 0
    
    def other(self) -> Pawn:
        return Pawn.BLACK if Pawn.WHITE else Pawn.BLACK
    
@dataclass(frozen=True)
class Grid:
    cells: np.full((8,8), 2)

    def __post_init__(self):
        validateGrid(self)

    @cached_property
    def counts(self) -> int:
        return dict(zip(np.unique(self.cells, return_count=True)))
    
    

@dataclass(frozen=True)
class Move:
    pawn: Pawn
    index: tuple[int, int]
    beforeState: GameState

    def __post_init__(self):
        validateMove(self)

    @cached_property
    def afterState(self) -> GameState:
        grid = self.beforeState.grid
        grid[self.index[0], self.index[1]] = self.pawn.value
        afterState = GameState(grid, self.beforeState.currrentTurn+1)
        return afterState

    @cached_property
    def sandwiches(self) -> list:
        sandwiches = []
        difs = [(-2,0), (2,0),(0,-2),(0,2),(-2,-2),(-2,2),(2,-2),(2,2)]

        for dif in difs:

            if(self.index[0]+dif[0] < 8 and self.index[1]+dif[1] < 8
                and self.gameBoard[self.index[0]+dif[0], self.index[1]+dif[1]] == self.pawn
                and self.gameBoard[self.index[0]+dif[0]//2, self.index[1]+dif[1]//2] == self.pawn.other): 

                sandwiches.append(dif)
               
        return sandwiches
    


class GameStage(str, enum.Enum):
    gameNotStarted : 0
    earlyGame : 1
    midGame : 2
    endGame : 3
    tie : 4
    blackWin : 5
    whiteWin : 6

#Dataclass auto implements __init__, __repr__, __eq__ and order functions : __ge__, __le__, ...
@dataclass(frozen=True)
class GameState:
    grid: Grid
    currrentTurn: int

    def __post_init__(self):
        validateGameState(self)

    @cached_property
    def currentPawn(self) -> Pawn:
        return Pawn[self.currrentTurn%2]
    #Possiblement plus intéressant de séparer en plusieurs propriétés
    @cached_property
    def gameStage(self, endGameDepth) -> GameStage:
        if self.currrentTurn == 0 : return GameStage.gameNotStarted
        elif self.currrentTurn < 13 :return GameStage.earlyGame
        elif self.currrentTurn < 60 - (endGameDepth+5) : return GameStage.endGame
        elif Grid.counts["0"] == Grid.counts["1"] : return GameStage.tie
        elif Grid.counts["0"] < Grid.counts["1"]: return GameStage.blackWin

        return GameStage.whiteWin
    
    @cached_property
    def possibleMoves(self):
        otherPawn = self.currentPawn.other
        otherPawns = np.where(self.grid==otherPawn.value)
        offsets =[[1,-1,0,0], [0,0,1,-1]]
        moves = []

        for i, xCoord in enumerate(otherPawns[0]):
            for j, xOffset in enumerate(offsets[0]):
                position = [xCoord+xOffset, otherPawns[1][i]+offsets[1][j]]
                move = Move(self.currentPawn, position, self)

                if validateMove(move): moves.append(move)

        return moves
    



