from game.engine import Othello

from renderer import PyGameRenderer
from player import PyGamePlayer, IA
from logic.models import Pawn
from logic import settings
import pygame as pg
from logic.exceptions import StopGame 
import pygame_gui
import re

def main() -> None:
    #Othello(PyGamePlayer(Pawn.WHITE), PyGamePlayer(Pawn.BLACK), PyGameRenderer()).play()
    #Othello(PyGamePlayer(Pawn.WHITE), IA(Pawn.BLACK, 3, 7), PyGameRenderer()).play()

   

    pg.init()

    # Set up the Pygame window
    WINDOW_SIZE = (400, 540)
    window_surface = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Pygame Input Example")

    # Set up the Pygame GUI manager
    gui_manager = pygame_gui.UIManager(WINDOW_SIZE)

    # Set up the text inputs
    depthInput = pygame_gui.elements.UITextEntryLine(relative_rect=pg.Rect((50, 50), (300, 50)), 
                                                     manager=gui_manager)
    endGameDepthepthInput = pygame_gui.elements.UITextEntryLine(relative_rect=pg.Rect((50, 150), (300, 50)), 
                                                                manager=gui_manager)
    allowed = ["0","1","2","3","4","5","6","7","8","9"]
    depthInput.set_allowed_characters(allowed_characters = allowed)
    endGameDepthepthInput.set_allowed_characters(allowed_characters = allowed)

    # Set up the dropdown inputs
    whiteItems = ["IA", "Humain"]
    whiteDropDown = pygame_gui.elements.UIDropDownMenu(options_list=whiteItems,
                                                   starting_option=whiteItems[0],
                                                   relative_rect=pg.Rect((50, 250), (300, 50)),
                                                   manager=gui_manager)
    blackItems = ["IA", "Humain"]
    blackDropDown = pygame_gui.elements.UIDropDownMenu(options_list=blackItems,
                                                   starting_option=blackItems[0],
                                                   relative_rect=pg.Rect((50, 350), (300, 50)),
                                                   manager=gui_manager)
    
    confirmButton = pygame_gui.elements.UIButton(relative_rect=pg.Rect((150, 450), (100, 50)),
                                             text='Confirmer',
                                             manager=gui_manager)

    # Main Pygame loop
    windowClosed = False
    confirmed = False
    while not windowClosed and not confirmed:
        time_delta = pg.time.Clock().tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                windowClosed = True

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == confirmButton:
                  confirmed = True

            gui_manager.process_events(event)

        gui_manager.update(time_delta)

        window_surface.fill((255, 255, 255))

        gui_manager.draw_ui(window_surface)
        
        if confirmed: 
            if depthInput.get_text() == '' or endGameDepthepthInput.get_text() == '':
                confirmed = False 
            elif int(depthInput.get_text()) > 9 or int(endGameDepthepthInput.get_text()) > 9 :
                confirmed = False

        pg.display.update()


    if confirmed:

        settings.depth = int(depthInput.get_text())
        settings.endGameDepth = int(endGameDepthepthInput.get_text())

        whiteSelection = whiteDropDown.selected_option
        blackSelection = blackDropDown.selected_option

        if whiteSelection == "Humain" : white = PyGamePlayer(Pawn.WHITE)
        else: white = IA(Pawn.WHITE)

        if blackSelection == "Humain" : black = PyGamePlayer(Pawn.BLACK)
        else: black = IA(Pawn.BLACK)

    pg.quit()

    if confirmed : Othello(white, black, PyGameRenderer()).play()

    