# from Menu import MenuState
import pygame
import sys
from math import *


class MainMenu(None):

    def __init__(self):
        pygame.init()
        screen = pygame.display

        grid_window_width = 400
        grid_window_height = 400

        cell_side = 100

        window_width = grid_window_width + 100
        window_height = grid_window_height + 200

        padding_v = 50
        padding_h = 50

        no_players = 0

        display = pygame.display.set_mode((window_width, window_height))
        clock = pygame.time.Clock()

        while True:

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                # checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN:

                    # if the mouse is clicked on the
                    # button the game is terminated
                    if window_width / 2 <= mouse[0] <= window_width / 2 + 140 and window_height / 2 <= mouse[1] <= window_height / 2 + 40:
                        pygame.quit()

                        # fills the screen with a color
            pygame.display.fill((60, 25, 60))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()

            # if mouse is hovered on a button it
            # changes to lighter shade
            if window_width / 2 <= mouse[0] <= window_width / 2 + 140 and window_height / 2 <= mouse[1] <= window_height / 2 + 40:
                pygame.draw.rect(screen, color_light, [width / 2, height / 2, 140, 40])

            else:
                pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 140, 40])

                # superimposing the text onto our button
            screen.blit(text, (width / 2 + 50, height / 2))

            # updates the frames of the game
            pygame.display.update()