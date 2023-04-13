from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
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

    @cached_property
    def counts(self) -> int:
        return dict(zip(np.unique(self.cells, return_count=True)))
    
    

@dataclass(frozen=True)
class Move:
    pawn: Pawn
    index: tuple[int, int]
    sandwiches: list[tuple[int,int]] 
    before_state: GameState 
    after_state: GameState

    @cached_property
    def findSandwiches(self) -> bool:
        self.sandwiches = []
        difs = [(-2,0), (2,0),(0,-2),(0,2),(-2,-2),(-2,2),(2,-2),(2,2)]
        isSandwich = False

        for dif in difs:
            if(self.index[0]+dif[0] < 8 and self.index[1]+dif[1] < 8
                and self.gameBoard[self.index[0]+dif[0], self.index[1]+dif[1]] == self.pawn
                and self.gameBoard[self.index[0]+dif[0]//2, self.index[1]+dif[1]//2] == self.pawn.other): 

                isSandwich = True
                self.sandwiches.append(dif)
            
                
        return isSandwich

class gameStage(str, enum.Enum):
    gameNotStarted : 0
    earlyGame : 1
    midGame : 2
    endGame : 3
    tie : 4
    blackWin : 5
    whiteWin : 6


@dataclass(frozen=True)
class GameState:
    grid: Grid
    currrentTurn: int

    @cached_property
    def currentPawn(self) -> Pawn:
        return Pawn[self.currrentTurn%2]
    
    @cached_property
    def gameStage(self, endGameDepth) -> gameStage:
        if self.currrentTurn == 0 : return gameStage.gameNotStarted
        elif self.currrentTurn < 13 :return gameStage.earlyGame
        elif self.currrentTurn < 60 - (endGameDepth+5) : return gameStage.endGame
        elif Grid.counts["0"] == Grid.counts["1"] : return gameStage.tie
        elif Grid.counts["0"] < Grid.counts["1"]: return gameStage.blackWin
        return gameStage.whiteWin
    
    @cached_property
    def possible_moves(self):
        otherPawn = self.currentPawn.other
        otherPawns = np.where(self.grid==otherPawn.value)
        offsets =[[1,-1,0,0], [0,0,1,-1]]
        moves = []

        for i, xCoord in enumerate(otherPawns[0]):
            for j, xOffset in enumerate(offsets[0]):
                position = [xCoord+xOffset, otherPawns[1][i]+offsets[1][j]]
                move = Move(self.currentPawn, position)

                if self.grid[move.index[0], move.index[1]] == 2 and move.findSandwiches: moves.append(move)

        return moves
    
    


