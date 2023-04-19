

from dataclasses import dataclass
from typing import Callable, TypeAlias

from othello.game.players import Player
from othello.logic.models import *
from othello.logic.exceptions import *
from othello.game.renderers import Renderer

ErrorHandler: TypeAlias = Callable[[Exception], None]

@dataclass(frozen=True)
class Othello:
    player1: Player
    player2: Player
    renderer: Renderer
    errorHandler: ErrorHandler | None = None

    def play(self) -> None:
        cells = np.full((8,8),2)
        cells[3,4] = 0
        cells[4,3] = 0
        cells[4,4] = 1
        cells[3,3] = 1

        gameState = GameState(Grid(cells), 1, 6) # 6 : EndGame Depth maybe surface through menu or cli

        #print("GameState created")
        while (gameState.currentTurn <= 60 
            and len(gameState.possibleMoves) > 0 
            and not gameState.gameStage == GameStage.blackWin  
            and not gameState.gameStage == GameStage.whiteWin
            and not gameState.gameStage == GameStage.tie):

            #print("Turn :", gameState.currentTurn)

            
            self.renderer.Render(gameState)
            #print("Game rendered")

            player = self.getCurrentPlayer(gameState)
            #print("current player : ", player.pawn)
            try:
                afterState = player.makeMove(gameState)
                if afterState: 
                    gameState = afterState
                    print("afterState Engine", afterState)
                #print("Make move")
            except InvalidMove as ex:
                print(str(ex))

            

    def getCurrentPlayer(self, gameState : GameState) -> Player:
        return self.player1 if self.player1.pawn == gameState.currentPawn else self.player2
            
