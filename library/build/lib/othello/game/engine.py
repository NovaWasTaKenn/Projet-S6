

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

        gameState = GameState(Grid(), 1)
        while (gameState.currrentTurn <= 60 
            and not gameState.gameStage == GameStage.blackWin 
            and not gameState.gameStage == GameStage.whiteWin
            and not gameState.gameStage == GameStage.tie):

            self.renderer.Render(gameState)

            player = self.getCurrentPlayer(gameState)
            try:
                gameState = player.makeMove(gameState)
            except InvalidMove as ex:
                if self.errorHandler:
                    self.errorHandler(ex)


    def getCurrentPlayer(self, gameState : GameState) -> Player:
        return self.player1 if self.player1.pawn == gameState.currentPawn else self.player2
            
