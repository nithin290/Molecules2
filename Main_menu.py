from Menu import MenuState
import pygame
import sys
from math import *


class MainMenu(MenuState):

    def __init__(self):
        pygame.init()

        width = 500
        height = 500

        window_width = max(300, width)
        window_height = max(400, width)

        grid_window_width = window_width - 100
        grid_window_height = window_height - 200

        padding_v = 50
        padding_h = 50

        display = pygame.display.set_mode((window_width, window_height))
        clock = pygame.time.Clock()