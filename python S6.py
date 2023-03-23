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
        difs = [(-2,0), (2,0),(0,-2),(0,2),(-2,-2),(-2,2),(2,-2),(2,2)]
        isSandwich = False
        for dif in difs:
            if(self.gameBoard[position[0]+dif[0], position[1]+dif[1]] == self.player
               and self.gameBoard[position[0]+dif[0]/2, position[1]+dif[1]/2] == self.player*-1): 
                isSandwich = True
                self.sandwiches.append(dif)
            
                
        return isSandwich
    
    def positionValid(self, position):
        
        return (
            self.gameBoard[position[0], position[1]] == 0
            and(
                self.gameBoard[position[0]-1, position[1]] == self.player*-1
                or self.gameBoard[position[0]+1, position[1]] == self.player*-1
                or self.gameBoard[position[0], position[1]-1] == self.player*-1
                or self.gameBoard[position[0], position[1]+1] == self.player*-1
                )
            and(
                self.findSandwiches(position)
                )
            
            )
            
    def updateGameBoard(self, position):
        self.gameBoard[position[0], position[1]] = self.player
        for diff in self.sandwiches:
            self.gameBoard[position[0]-diff[0]/2, position[1] - diff[1]/2] = self.player
                
            
    def showConsoleGameBoard(self):
        print("0 | 1 | 2 | 3 | 4 | 5 | 6 | 7")
        print("_______________________________")
        for i in range(8):
            print(" "+str(i)+" | "+" | ".join(["O" if value == -1 else 'X' if value == 1 else " " for value in self.gameBoard[i,:]]))
            print("_______________________________")
    
    def showPyGameGameBoard(self):


        background = pg.display.set_mode((540 ,540))
        background.fill("grey")
        pg.draw.rect(background, (0,102,0), (30,30,480,480))

        for i in range(30, 511, 60):
            pg.draw.line(background , (255, 255, 255), (30, i), (510, i))
            pg.draw.line(background , (255, 255, 255), (i, 30), (i, 510))
            pg.display.flip()

        for i in range(8):
            for j in range(8):
                a = self.gameBoard[i, j] 

                if a == 1 : color = (0,0,0)
                else : color = (255,255,255)

                piece = Piece(color, (60*i, 60*j))
                background.blit(piece.surf, piece.rect)




    def play(self):

        pg.init()
        running = True
        clock = pg.time.Clock()
        dt = 0
        self.showPyGameGameBoard()

        while running:
            
            

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONUP:
                    position = pg.mouse.get_pos()

                    if self.positionValid(position):
                        self.updateGameBoard(position)
                        self.showPyGameGameBoard()

        pg.quit()
            
                
            
            # print("Joueur noir (X)" if self.player == 1 else "Joueur blanc (O)")
            # print()
            # self.showGameBoard()
            # print()
            
            # positionStr = input("Saisissez la position (x,y) :")
            # position = positionStr.replace("(", "").replace(")", "").split(",")
            # while not self.positionValid(position):
            #     positionStr = input("Saisissez la position (x,y) :")
            #     position = positionStr.replace("(", "").replace(")", "").split(",")
                
            # self.updateGameBoard(position)
            
            # self.player *= -1

class  Piece(pg.sprite.Sprite):
    def __init__(self, color, position):
        super(Piece, self).__init__()

        self.x = position[0]
        self.y = position[1]

        self.surf = pg.Surface((60,60))
        self.surf.fill((0,102,0))
        pg.draw.circle(self.surf, color, (30,30), 20)
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
        
        
        
        
        
        
        
        
        
        
        