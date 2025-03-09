import pygame, sys
from pygame.locals import *
import random
from classes import *
from colors import *

pygame.init()
main_window = window(800,600,"Arcade")
player1 = starship(["nave","weapon1"],1,368,450,8,800, 8,0,0)

control_game = game(player1,30, main_window)
tdisplay = text_display(main_window,control_game,TEAL,TEAL2)

star_background = stars([[GREEN,2],[YELLOW,3],[BLUE,1]], main_window)

while True: # main game loop
    #contador
    current_time = pygame.time.get_ticks()
    main_window.clean_screen()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            control_game.control_inputs(event)

    control_game.control_input_player()

    star_background.update_stars()
    control_game.update_game()

    tdisplay.draw()

    pygame.display.update()
    control_game.clock.tick(control_game.fps)
