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

        #print()
        #print()
        #print("Sandwichs : ", self.sandwiches)

        for sandwich in self.sandwiches:
            #print(sandwich)

            for i in range(1,8):

                    if ( self.index[0]+i*sandwich[0] > 7 or self.index[1]+i*sandwich[1] > 7
                    or self.index[0]+i*sandwich[0] < 0 or self.index[1]+i*sandwich[1] < 0
                    or cells[self.index[0]+i*sandwich[0], self.index[1]+i*sandwich[1]] == self.pawn.value):
                        break

                    if cells[self.index[0]+i*sandwich[0], self.index[1]+i*sandwich[1]] == self.pawn.other.value:
                        cells[self.index[0]+i*sandwich[0], self.index[1]+i*sandwich[1]] = self.pawn.value
                    

        afterState_ = GameState(Grid(cells), self.beforeState.currentTurn+1, 3, self.pawn.other)
        #print()
        #print()
        #print("afterstate : ", afterState_)
        return afterState_ 

    @cached_property
    def sandwiches(self) -> list:
        sandwiches = []
        difs = [(0, -1), (0, 1), (-1, 0), (1, 0),
                (-1, -1), (1, 1), (1, -1), (-1, 1)]

        

        for dif in difs:

            foundAdversary = False
             
            for i in range (1,8):

                otherPosition = [self.index[0]+i*dif[0], self.index[1]+i*dif[1]]

                if (otherPosition[0] < 0 or otherPosition[0] > 7
                or otherPosition[1] < 0 or otherPosition[1] > 7
                or self.beforeState.grid.cells[otherPosition[0], otherPosition[1]] == 2):
                    break

                if self.beforeState.grid.cells[otherPosition[0], otherPosition[1]] == self.pawn.other.value:
                    foundAdversary = True

                if self.beforeState.grid.cells[otherPosition[0], otherPosition[1]] == self.pawn.value and not foundAdversary:
                    break

                if self.beforeState.grid.cells[otherPosition[0], otherPosition[1]] == self.pawn.value and foundAdversary:

                    if (self.index[0]+i*dif[0], self.index[1]+i*dif[1]) != (self.index[0], self.index[1]):
                        sandwiches.append(dif)
                    break
        #print()
        #print()
        #print("sandwichs : ",sandwiches)
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
        if self.currentTurn == 1 and len(self.possibleMoves) != 0: return GameStage.gameNotStarted
        elif self.currentTurn < 13 and len(self.possibleMoves) != 0: return GameStage.earlyGame
        elif self.currentTurn < 60 - (self.endGameDepth+5) and len(self.possibleMoves) != 0: return GameStage.midGame
        elif self.currentTurn <= 60 and len(self.possibleMoves) != 0: return GameStage.endGame
        elif self.grid.counts[0] > self.grid.counts[1] : return GameStage.whiteWin
        elif self.grid.counts[0] < self.grid.counts[1]: return GameStage.blackWin

        return GameStage.tie
    
    @cached_property
    def possibleMoves(self):
        otherPawn = self.currentPawn.other
        otherPawns = np.where(self.grid.cells==otherPawn.value)
        #print("otherPawns : ",otherPawns)
        offsets =[[1,-1,0,0], [0,0,1,-1]]
        moves = []

        for i, xCoord in enumerate(otherPawns[0]):
            for j, xOffset in enumerate(offsets[0]):

                position = [xCoord+xOffset, otherPawns[1][i]+offsets[1][j]]

                if (position[0] >= 0 and position[0] < 8
                    and position[1] >= 0 and position[1] <8 
                    and not len(list(filter(lambda x : x.index[0]==position[0] and x.index[1]==position[1], moves))) >  0):
                    try: 
                        move = Move(self.currentPawn, position, self)
                        moves.append(move)
                    except InvalidMove:
                        #print("")
                        None
        #print()
        #print()      
        #print("moves : ",moves)
        return moves
    



