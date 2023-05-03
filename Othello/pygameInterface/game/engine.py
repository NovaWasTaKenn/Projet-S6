from dataclasses import dataclass
from typing import Callable, TypeAlias

from game.players import Player
from logic.models import *
from logic.exceptions import *
from game.renderers import Renderer
import time
import functools
import pygame as pg

@dataclass(frozen=True)
class Othello:
    player1: Player
    player2: Player
    renderer: Renderer

    def play(self) -> None:
        cells = np.full((8,8),2)
        cells[3,4] = 0
        cells[4,3] = 0
        cells[4,4] = 1
        cells[3,3] = 1

        gameState = GameState(Grid(cells), 1, Pawn.BLACK)

        start = 0
        lastMove = None

        #print("GameState created")
        while (gameState.currentTurn <= 60 
            and not gameState.gameStage == GameStage.blackWin  
            and not gameState.gameStage == GameStage.whiteWin
            and not gameState.gameStage == GameStage.tie):

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    raise StopGame("Player closed the window")

            #print("Turn :", gameState.currentTurn)
            #print()
            #print(f" ------> Joueur {gameState.currentPawn.name}")
            #print()

            end = time.perf_counter()
            timeElapsed = end-start
            self.renderer.Render(gameState, timeElapsed, lastMove)

            start = time.perf_counter()

            player = self.getCurrentPlayer(gameState)
            #print("current player : ", player.pawn)
            
            if gameState.possibleMoves == []:
                print("No possible move")
                gameState = GameState(gameState.grid, gameState.currentTurn, gameState.currentPawn.other) # 6 : EndGame Depth maybe surface through menu or cli
            else :
                try:
                    lastMove = player.makeMove(gameState)
                    if lastMove is not None:
                        afterState = lastMove.afterState
                    if afterState: 
                        gameState = afterState
                        #print("afterState Engine", afterState)
                    #print("Make move")
                except InvalidMove as ex:
                    print(str(ex))

                #except StopGame as ex :  # Vérif si fermeture fenêtre gérée sans le bool sinon ajouter done dans while pour couper le jeu
                #    print(str(ex))
                #    # done = True

        
        print("Turn : ", gameState.currentTurn)
        print("PossibleMoves : ", gameState.possibleMoves)
        print("OtherPossibleMoves : ", GameState(gameState.grid, gameState.currentTurn, gameState.currentPawn.other).possibleMoves)

        if(gameState.gameStage == GameStage.blackWin): print("Black wins")
        if(gameState.gameStage == GameStage.whiteWin): print("White wins")
        if(gameState.gameStage == GameStage.tie) : print("tie")

    def getCurrentPlayer(self, gameState : GameState) -> Player:
        return self.player1 if self.player1.pawn == gameState.currentPawn else self.player2
    
def timer(fonction):
    @functools.wraps(fonction)
    def wrap(*param, **param2):
        start = time.perf_counter()
        value = fonction(*param, **param2)
        end = time.perf_counter()
        runTime = end - start
        print()
        print(f" ------> Function {fonction.__name__} finished in {runTime} seconds")
        print()
        return value
    return wrap

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug
            
