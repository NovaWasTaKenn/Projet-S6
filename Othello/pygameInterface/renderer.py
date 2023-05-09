import pygame as pg

from game.renderers import Renderer
from logic.models import GameState, Pawn, Move



class PyGameRenderer(Renderer):
    
    lastTurnBlack = 0
    lastTurnWhite = 0
    lastTurnMove = "Pas de coup précédent"
    counter = 0
    blackPieces = 0
    whitePieces = 0

    def __init__(self,prediction = False):
        
        pg.init()

        self.font = pg.font.SysFont('Comic Sans MS', 15, True)
        self.background = pg.display.set_mode((750 ,540))
        self.prediction = prediction



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

            timeElapsedWhite = self.font.render(f"Temps du dernier tour blanc: \n{PyGameRenderer.lastTurnWhite:5.4f} seconds", False, (0, 0, 0))
            self.background.blit(timeElapsedWhite, (540, 75))

            timeElapsedBlack = self.font.render(f"Temps du dernier tour noir : \n{PyGameRenderer.lastTurnBlack:5.4f} seconds", False, (0, 0, 0))
            self.background.blit(timeElapsedBlack, (540, 125))

            lastMoveTxt = self.font.render(PyGameRenderer.lastTurnMove, False, (0, 0, 0))
            self.background.blit(lastMoveTxt, (540 , 175))

            if self.prediction: possibleMove= [(state.index[0], state.index[1]) for state in gameState.possibleMoves]
            
            PyGameRenderer.blackPieces = 0
            PyGameRenderer.whitePieces = 0


            for i in range(8):
                for j in range(8):
                    a = int(gameState.grid.cells[i, j]) 

                    if a == Pawn.BLACK.value : color = (0,0,0)
                        
                        
                    elif a == Pawn.WHITE.value : color = (255,255,255)
                        

                    if a != 2:
                        if a == 0:
                            PyGameRenderer.blackPieces += 1 
                        else:
                            PyGameRenderer.whitePieces += 1
                        piece = Piece(color, (30 + 60*i +5, 30 + 60*j + 5),0)
                        self.background.blit(piece.surf, piece.rect)
                    # Ajoute la couleur de la case si elle est jouable  

                    
                    if self.prediction:
                        if (i, j) in possibleMove:
                            piece = Piece('red', (30 + 60*i + 5, 30 + 60*j + 5),5)
                            self.background.blit(piece.surf, piece.rect)

            
            blackText = self.font.render("Noir", False, (0, 0, 0))
            self.background.blit(blackText, (655, 290))
            blackCounter = self.font.render(str(PyGameRenderer.blackPieces), False, (0, 0, 0))
            self.background.blit(blackCounter, (663, 310))

            whiteText = self.font.render("Blanc", False, (0, 0, 0))
            self.background.blit(whiteText, (575, 290))
            whiteCounter = self.font.render(str(PyGameRenderer.whitePieces), False, (0, 0, 0))
            self.background.blit(whiteCounter, (586, 310))
                        
            pg.display.flip()

class  Piece(pg.sprite.Sprite):
    def __init__(self, color, position,width):
        super(Piece, self).__init__()

        self.x = position[0]
        self.y = position[1]
        self.width = width

        self.surf = pg.Surface((50,50))
        self.surf.fill((0,102,0))
        pg.draw.circle(self.surf, color, (25,25), 20, self.width)
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))




