# Import modules and code/classes/objects from other files
import math
import random

import pygame.font

from objects import *


# The Main function in which all the GUI code is ran
def main():

    # ----------------- Initializing Pygame Variables -----------------
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # The initial Pygame Screen
    clock = pygame.time.Clock()  # Clock for adjusting the frames per second

    time = 0  # Used for keeping track of seconds (60 ticks per second)

    screen.fill(pygame.Color("White"))
    pygame.display.set_caption("Drill Blocks")  # Game Name?

    # ----------------- Initializing Objects -----------------
    # Used to determine which objects are selected

    selected_object = None

    # ----------------- The Main GUI Loop -----------------
    running = True
    while running:

        # ----------------- Looping through Pygame Events -----------------
        for event in pygame.event.get():

            # Quit Pygame
            if event.type == pygame.QUIT:
                running = False
                break

    # Once the loop has ended, quit the application
    pygame.quit()


if __name__ == '__main__':
    main()
