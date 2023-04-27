from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from logic.validators import *
import enum
import numpy as np


class Pawn(enum.Enum):
    BLACK = 1
    WHITE = 0
    
    @cached_property
    def other(self) -> Pawn:
        return Pawn.BLACK if self is Pawn.WHITE else Pawn.WHITE
    
@dataclass(frozen=True)
class Grid:
    cells: np.array

    def __post_init__(self):

        validateGrid(self)

    @cached_property
    def counts(self) -> dict:
        uniques = np.unique(self.cells, return_counts=True)
        return dict(zip(uniques[0], uniques[1]))
    
    

@dataclass(frozen=True)
class Move:
    pawn: Pawn
    index: tuple[int, int]
    beforeState: GameState

    def __post_init__(self):
        validateMove(self)

    @cached_property
    def afterState(self) -> GameState:
        cells = np.copy(self.beforeState.grid.cells)
        cells[self.index[0], self.index[1]] = self.pawn.value
        for sandwich in self.sandwiches:
            i = 1
            j = 1
            other = []
            while (self.index[0]+i*sandwich[0] > 0 
                   and self.index[0]+i*sandwich[0] < 7 
                   and self.index[1]+j*sandwich[1] > 0 
                   and self.index[1]+j*sandwich[1] < 7 
                   and cells[self.index[0]+i*sandwich[0], self.index[1]+j*sandwich[1]] != self.pawn.value 
                   and [self.index[1]+j*sandwich[1]] != 2):
                other.append((self.index[0]+i*sandwich[0],self.index[1]+j*sandwich[1]))
                i+=1
                j+=j
            if cells[self.index[0]+i*sandwich[0], self.index[1]+j*sandwich[1]] == self.pawn.value:
                for pawn in other:
                    cells[pawn[0],pawn[1]] = self.pawn.value

        afterState_ = GameState(Grid(cells), self.beforeState.currentTurn+1, 6,self.pawn.other)
        print("afterState : ", afterState_)
        return afterState_

    @cached_property
    def sandwiches(self) -> list:
        sandwiches = []
        difs = [(0, -1), (0, 1), (-1, 0), (1, 0),
                (-1, -1), (1, 1), (1, -1), (-1, 1)]


        for dif in difs:
            for i in range (1,8):
                if self.index[0]+i*dif[0] > 7 or self.index[0]+i*dif[0] < 0:
                    break
                for j in range(1,8):
                    if self.index[1]+j*dif[1] > 7 or self.index[1]+j*dif[1] < 0:
                        break
                    otherPosition = [self.index[0]+i*dif[0], self.index[1]+j*dif[1]]

                    if self.beforeState.grid.cells[otherPosition[0], otherPosition[1]] == self.pawn.value:
                        if (self.index[0]+dif[0], self.index[1]+dif[1]) != (self.index[0], self.index[1]):
                            sandwiches.append(dif)
                        break
        return sandwiches
        


class GameStage(enum.Enum):
    gameNotStarted = 0
    earlyGame = 1
    midGame = 2
    endGame = 3
    tie = 4
    blackWin = 5
    whiteWin = 6

#Dataclass auto implements __init__, __repr__, __eq__ and order functions : __ge__, __le__, ...
@dataclass(frozen=True)
class GameState:
    grid: Grid
    currentTurn: int
    endGameDepth: int
    currentPawn: Pawn

    def __post_init__(self):
        validateGameState(self)
    
    #Possiblement plus intéressant de séparer en plusieurs propriétés
    @cached_property
    def gameStage(self) -> GameStage:
        if self.currentTurn == 1 : return GameStage.gameNotStarted
        elif self.currentTurn < 13 : return GameStage.earlyGame
        elif self.currentTurn < 60 - (self.endGameDepth+5) : return GameStage.endGame
        elif Grid.counts[0] == Grid.counts[1] : return GameStage.tie
        elif Grid.counts[0] < Grid.counts[1]: return GameStage.blackWin

        return GameStage.whiteWin
    
    @cached_property
    def possibleMoves(self):
        otherPawn = self.currentPawn.other
        otherPawns = np.where(self.grid.cells==otherPawn.value)
        print("otherPawns : ",otherPawns)
        offsets =[[1,-1,0,0], [0,0,1,-1]]
        moves = []

        for i, xCoord in enumerate(otherPawns[0]):
            for j, xOffset in enumerate(offsets[0]):

                position = [xCoord+xOffset, otherPawns[1][i]+offsets[1][j]]

                if (position[0] >= 1 and position[0] < 8
                    and position[1] >= 1 and position[1] <8 
                    and not len(list(filter(lambda x : x.index[0]==position[0] and x.index[1]==position[1], moves)))>0):
                    try: 
                        move = Move(self.currentPawn, position, self)
                        moves.append(move)
                    except InvalidMove:
                        #print("")
                        None
                

        return moves
    



