from dataclasses import dataclass
# from typing import Callable, TypeAlias

from game.players import Player
from logic.models import *
from logic.exceptions import *
from game.renderers import Renderer
# from player import PyGamePlayer
from renderer import PyGameRenderer
import pygame as pg


@dataclass(frozen=True)
class Othello:
    """
    Classe Othello comprenant l'initialisation du board, du 1° tour du jeu, les coups possibles,
    la fin du jeu et la fermeture de la fenêtre
    """
    player1: Player
    player2: Player
    renderer: Renderer

    
    def play(self) -> bool:
        """
        Initialise le 1° tour d'Othello avec deux pions noirs placés en [3,3] 
        et [4,4] et deux pions blancs placés en [3,4] et [4,3]
        """
        game = True
        while game:
            cells = np.full((8, 8), 2)
            cells[3, 4] = 1
            cells[4, 3] = 1
            cells[4, 4] = 0
            cells[3, 3] = 0

            gameState = GameState(Grid(cells), 1, Pawn.BLACK)

            start = 0
            lastMove = None
        #print("GameState created")
            while (gameState.currentTurn <= 61
                and not gameState.gameStage == GameStage.blackWin
                and not gameState.gameStage == GameStage.whiteWin
                and not gameState.gameStage == GameStage.tie):

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        raise StopGame("Player closed the window")

                #print("Turn :", gameState.currentTurn)
                # print()
                #print(f" ------> Joueur {gameState.currentPawn.name}")
                # print()

                # end = time.perf_counter()
                # timeElapsed = end-start
                if lastMove is not None:
                    PyGameRenderer.lastTurnMove = f"Coup précedent : ({lastMove.index[0]}, {lastMove.index[1]})"
                self.renderer.Render(gameState)

                # start = time.perf_counter()

                player = self.getCurrentPlayer(gameState)
                #print("current player : ", player.pawn)

                if gameState.possibleMoves == []:
                    print("No possible move")
                    # 6 : EndGame Depth maybe surface through menu or cli
                    gameState = GameState(
                        gameState.grid, gameState.currentTurn, gameState.currentPawn.other)
                else:
                    try:
                        lastMove = player.makeMove(gameState)

                        if lastMove:
                            afterState = lastMove.afterState
                        else:
                            afterState = False

                        if afterState:
                            gameState = afterState
                            #print("afterState Engine", afterState)
                        #print("Make move")
                    except InvalidMove as ex:
                        print(str(ex))

                    # except StopGame as ex :  # Vérif si fermeture fenêtre gérée sans le bool sinon ajouter done dans while pour couper le jeu
                    #    print(str(ex))
                    #    # done = True

            print("Turn : ", gameState.currentTurn)
            print("PossibleMoves : ", gameState.possibleMoves)
            print("OtherPossibleMoves : ", GameState(gameState.grid,
                gameState.currentTurn, gameState.currentPawn.other).possibleMoves)

            if(gameState.gameStage == GameStage.blackWin):
                print("Black wins")
            if(gameState.gameStage == GameStage.whiteWin):
                print("White wins")
            if(gameState.gameStage == GameStage.tie):
                print("tie")

            self.renderer.Render(gameState)
            print("Total Black : "+str(PyGameRenderer.totalBlack))
            print("Total White : "+str(PyGameRenderer.totalWhite))
            game = input("Appuyez sur entrée pour rejouer ou sur n'importe quelle touche pour quitter")
            if game == "":
                game = True
            else:
                game = False
        result = input("Appuyez sur espace pour quitter ou sur n'importe quelle touche pour rejouer")
        if result == "":
            return False
        else:
            return True

    def getCurrentPlayer(self, gameState: GameState) -> Player:
        """Retourne la classe Player à qui c'est le tour de jouer"""
        return self.player1 if self.player1.pawn == gameState.currentPawn else self.player2
