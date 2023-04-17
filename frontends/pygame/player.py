
import pygame as pg
from library.src.othello.game.players import Player
from library.src.othello.logic.models import *
from library.src.othello.logic.exceptions import *


class PyGamePlayer(Player):
    
    def getMove(self, gameState: GameState) -> Move:

        for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    raise StopGame("Player closed the window")
                elif event.type == pg.MOUSEBUTTONUP:

                    try:
                        position = pg.mouse.get_pos()
                        position = ((position[0]-30)//60, (position[1]-30)//60)
                        move = Move(gameState.currentPawn, position, gameState)

                    except Exception as ex:
                         print(str(ex))

                    return move
