# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:15:23 2023

@author: Quentin Le Nestour
"""

import numpy as np
import pygame as pg
import time

class Othello : 
    def __init__(self):
        self.gameBoard = np.zeros((8,8))
        self.gameBoard[3,3] = 1
        self.gameBoard[4,4] = 1
        self.gameBoard[3,4] = -1
        self.gameBoard[4,3] = -1
        self.player = 1
        self.sandwiches = []
        
    
    def findSandwiches(self, position):
        self.sandwiches = []
        difs = [(-2,0), (2,0),(0,-2),(0,2),(-2,-2),(-2,2),(2,-2),(2,2)]
        isSandwich = False
        for dif in difs:
            if(position[0]+dif[0] < 8 and position[1]+dif[1] < 8
                and self.gameBoard[position[0]+dif[0], position[1]+dif[1]] == self.player
                and self.gameBoard[position[0]+dif[0]//2, position[1]+dif[1]//2] == self.player*-1): 

                isSandwich = True
                self.sandwiches.append(dif)
            
                
        return isSandwich
    
    def positionValid(self, position):
        
        condition1 = self.gameBoard[position[0], position[1]] == 0
        condition2 = (
            (position[0]-1 >= 0 and self.gameBoard[position[0]-1, position[1]] == self.player*-1)
            or (position[0]+1 < 8 and self.gameBoard[position[0]+1, position[1]] == self.player*-1)
            or (position[1]-1 >= 0 and self.gameBoard[position[0], position[1]-1] == self.player*-1)
            or (position[1]+1 < 8 and self.gameBoard[position[0], position[1]+1] == self.player*-1)
            )
           
        condition3 = self.findSandwiches(position)
                

        return condition1 and condition2 and condition3
            
            
            
            
    def updateGameBoard(self, position):
        self.gameBoard[position[0], position[1]] = self.player
        for diff in self.sandwiches:
            self.gameBoard[position[0] + diff[0]//2, position[1] + diff[1]//2] = self.player
                
            
    def showConsoleGameBoard(self):
        print("0 | 1 | 2 | 3 | 4 | 5 | 6 | 7")
        print("_______________________________")
        for i in range(8):
            print(" "+str(i)+" | "+" | ".join(["O" if value == -1 else 'X' if value == 1 else " " for value in self.gameBoard[i,:]]))
            print("_______________________________")
    
    def showPyGameGameBoard(self, my_font, background):
        pg.font.init()
        

        background.fill("grey")
        pg.draw.rect(background, (0,102,0), (30,30,480,480))

        for i in range(30, 511, 60):

            if (i-30)//60 != 8:
                columnCoord = my_font.render(str((i-30)//60), False, (0, 0, 0))
                lineCoord = my_font.render(str((i-30)//60), False, (0, 0, 0))
                background.blit(columnCoord, (i+10 , 10))
                background.blit(lineCoord, (10 , i+10))

            pg.draw.line(background , (255, 255, 255), (30, i), (510, i))
            pg.draw.line(background , (255, 255, 255), (i, 30), (i, 510))

        currentPlayer = my_font.render("Joueur actuel : noir" if self.player == 1 else "Joueur actuel : blanc", False, (0, 0, 0))
        background.blit(currentPlayer, (540 , 50))

        for i in range(8):
            for j in range(8):
                a = int(self.gameBoard[i, j]) 

                if a == 1 : color = (0,0,0)
                elif a == -1 : color = (255,255,255)

                if a != 0:
                    piece = Piece(color, (30 + 60*i +5, 30 + 60*j + 5))
                    background.blit(piece.surf, piece.rect)

        pg.display.flip()


    def count(self):
        return dict(zip(np.unique(self.gameBoard, return_counts = True)))

    def play(self):

        pg.init()

        my_font = pg.font.SysFont('Comic Sans MS', 15, True)
        background = pg.display.set_mode((740 ,540))

        running = True
        clock = pg.time.Clock()
        dt = 0
        self.showPyGameGameBoard(my_font, background)
        i = 0

        while  running and i <= 60:
            
            

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONUP:
                    position = pg.mouse.get_pos()

                    position = ((position[0]-30)//60, (position[1]-30)//60)

                    if self.positionValid(position):
                        self.updateGameBoard(position)
                        self.player *= -1
                        i += 1
                        self.showPyGameGameBoard(my_font, background)
                        
                        
        count = self.count()

        my_font = pg.font.SysFont('Comic Sans MS', 50, True)

        if count["1"] > count["-1"]:
            victoryMessage = my_font.render("Les noirs gagnent !", False, (0, 0, 0))

        elif count["1"] > count["-1"]:
            victoryMessage = my_font.render("Les blancs gagnent !", False, (0, 0, 0))

        elif count["1"] == count["-1"]:
            victoryMessage = my_font.render("Match nul !", False, (0, 0, 0))

        background.fill('grey')
        background.blit(victoryMessage, (250,250))

        pg.quit()
            

class  Piece(pg.sprite.Sprite):
    def __init__(self, color, position):
        super(Piece, self).__init__()

        self.x = position[0]
        self.y = position[1]

        self.surf = pg.Surface((50,50))
        self.surf.fill((0,102,0))
        pg.draw.circle(self.surf, color, (25,25), 20)
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
            
def timer(fonction):
    def inner(*param, **param2):
        t1 = time.time()
        fonction(*param, **param2)
        t2 = time.time()
        print(t2-t1)
    return inner
        

game = Othello()
game.play()       
        
        

        
        
        
        
        
        
        
        