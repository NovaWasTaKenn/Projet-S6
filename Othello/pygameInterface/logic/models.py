from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from logic.validators import *
import enum
import numpy as np
from logic import settings
from typing import Tuple

class Pawn(enum.Enum):
    """Classe comportant les différentes couleurs du pion (noir,blanc)"""
    BLACK = 1
    WHITE = 0
    
    @cached_property
    def other(self) -> Pawn:
        """Change de couleur de pion à chaque tour"""
        return Pawn.BLACK if self is Pawn.WHITE else Pawn.WHITE
    
@dataclass(frozen=True)
class Grid:
    """Classe créant le board de jeu"""
    cells: np.array

    def __post_init__(self):

        validateGrid(self)

    @cached_property
    def counts(self) -> dict:
        """Retourne le nombre de pions noirs et blancs présents sur le board"""
        uniques = np.unique(self.cells, return_counts=True)
        return dict(zip(uniques[0], uniques[1]))
    
    def compute_stability_and_center_scores(self) -> Tuple[np.array, np.array]:

        """
        Calcul les scores de stabilité et de centre pour chaque type de pion dans la grille.
        Retourne un tuple de deux tableaux numpy: le premier contient le score de stabilité pour chaque type de pion,
        et le second contient le score de centre pour chaque type de pion.
        """

        # Définit la matrice de stabilité
        stability_matrix = np.array([
            [40, -10, 11, 8, 8, 11, -10, 40],
            [-10, -10, -4, 1, 1, -4, -10, -10],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-10, -10, -4, 1, 1, -4, -10, -10],
            [40, -10, 11, 8, 8, 11, -10, 40]
        ])

        # Définit la matrice de centre
        center_matrix = np.zeros((8, 8))
        center_matrix[2:6, 2:6] = np.array([
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]
        ])

        # Calcul les scores de stabilité et de centre pour chaque type de pion
        current_stability = np.sum(stability_matrix * (self.cells == 1))
        other_stability = np.sum(stability_matrix * (self.cells == 2))
        current_center = np.sum(center_matrix * (self.cells == 1))
        other_center = np.sum(center_matrix * (self.cells == 2))

        return current_stability, other_stability, current_center, other_center
        

@dataclass(frozen=True)
class Move:
    """Classe comportant le pion, l'index choisi par le joueur, et Gamestate"""
    pawn: Pawn
    index: tuple[int, int]
    beforeState: GameState

    def __post_init__(self):
        validateMove(self)

    @cached_property
    def afterState(self) -> GameState:
        """edéfinit le board en fonction du coup sélectionné par le joueur et du sandwich créee"""
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

        
        afterState_ = GameState(Grid(cells), self.beforeState.currentTurn+1, self.pawn.other)
        #print()
        #print()
        #print("afterstate : ", afterState_)
        return afterState_ 

    @cached_property
    def sandwiches(self) -> list:
        """Retourne une liste des positions encerclées par le coup choisi (sandwich)"""
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
    """Classe représentant les différents états du jeu (non commencé,début,milieu,fin,égalité ou gagnant)"""
    gameNotStarted = 0
    earlyGame = 1
    midGame = 2
    endGame = 3
    tie = 4
    blackWin = 5
    whiteWin = 6

#Dataclass auto implements __init__, __repr__, __eq__ and order functions : __ge__, __le__, ...
@dataclass(frozen=True)
class GameState(object):
    """Classe retournant la Classe GameStage en fonction du board, du tour et du joueur actuel"""
    grid: Grid
    currentTurn: int
    currentPawn: Pawn
    
    #Possiblement plus intéressant de séparer en plusieurs propriétés
    @cached_property
    def gameStage(self) -> GameStage:
        """Retournes le GameStage en fonction du board, du tour et du joueur actuel"""
        otherPossibleMoves = GameState(self.grid, self.currentTurn, self.currentPawn.other).possibleMoves

        if self.currentTurn == 1 and self.possibleMoves != [] or otherPossibleMoves != []: return GameStage.gameNotStarted
        elif self.currentTurn < 13 and self.possibleMoves != [] or otherPossibleMoves != []: return GameStage.earlyGame
        elif self.currentTurn < 60 - (settings.endGameDepth + 3) and self.possibleMoves != [] or otherPossibleMoves != []: return GameStage.midGame
        elif self.currentTurn <= 60 and self.possibleMoves != [] or otherPossibleMoves != []: return GameStage.endGame
        elif self.grid.counts[0] > self.grid.counts[1] : return GameStage.whiteWin
        elif self.grid.counts[0] < self.grid.counts[1]: return GameStage.blackWin

        return GameStage.tie
    
    @cached_property
    def possibleMoves(self):
        """retourne le coup s'il est valide en fonction de la taille du board, des positions des différents pions """
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
    
    @cached_property
    def stablePositions(self):
        """retourne l'ensemble des positions stables qui sont à prioriser pour faciliter la victoire"""
        stable_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        stable_positions += [(0, i) for i in range(1, 7)] + \
            [(7, i) for i in range(1, 7)]
        stable_positions += [(i, 0) for i in range(1, 7)] + \
            [(i, 7) for i in range(1, 7)]
        stable_positions += [(2, 2), (2, 5), (5, 2), (5, 5)]
        return stable_positions


