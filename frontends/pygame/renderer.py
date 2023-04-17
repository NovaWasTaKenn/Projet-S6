import pygame as pg

from library.src.othello.game.renderers import Renderer
from library.src.othello.logic.models import GameState, Pawn


class PyGameRenderer(Renderer):
    
    def __init__(self):
        
        pg.init()

        self.font = pg.font.SysFont('Comic Sans MS', 15, True)
        self.background = pg.display.set_mode((740 ,540))


    def Render(self, gameState : GameState) -> None:
            pg.font.init()


            self.background.fill("grey")
            pg.draw.rect(self.background, (0,102,0), (30,30,480,480))

            for i in range(30, 511, 60):

                if (i-30)//60 != 8:
                    columnCoord = self.font.render(str((i-30)//60), False, (0, 0, 0))
                    lineCoord = self.font.render(str((i-30)//60), False, (0, 0, 0))
                    self.background.blit(columnCoord, (i+10 , 10))
                    self.background.blit(lineCoord, (10 , i+10))

                pg.draw.line(self.background , (255, 255, 255), (30, i), (510, i))
                pg.draw.line(self.background , (255, 255, 255), (i, 30), (i, 510))

            currentPlayer = self.font.render("Joueur actuel : noir" if gameState.currentPawn == Pawn.BLACK else "Joueur actuel : blanc", False, (0, 0, 0))
            self.background.blit(currentPlayer, (540 , 50))

            for i in range(8):
                for j in range(8):
                    a = int(self.gameBoard[i, j]) 

                    if a == 1 : color = (0,0,0)
                    elif a == -1 : color = (255,255,255)

                    if a != 0:
                        piece = Piece(color, (30 + 60*i +5, 30 + 60*j + 5))
                        self.background.blit(piece.surf, piece.rect)

            pg.display.flip()

class  Piece(pg.sprite.Sprite):
    def __init__(self, color, position):
        super(Piece, self).__init__()

        self.x = position[0]
        self.y = position[1]

        self.surf = pg.Surface((50,50))
        self.surf.fill((0,102,0))
        pg.draw.circle(self.surf, color, (25,25), 20)
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
