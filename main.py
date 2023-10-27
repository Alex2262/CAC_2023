# Import modules and code/classes/objects from other files
import math
import random

import pygame.font

from objects import *


# The Main function
def main():
    # ----------------- Initializing Pygame Variables -----------------
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # The initial Pygame Screen
    clock = pygame.time.Clock()  # Clock for adjusting the frames per second

    time = 0  # Used for keeping track of seconds (60 ticks per second)

    screen.fill(pygame.Color("White"))
    pygame.display.update()
    pygame.display.set_caption("Drill Blocks")  # Game Name?

    new_mode = 0

    while True:
        if new_mode == -1:
            return
        elif new_mode == MAIN_MENU:
            main_menu(screen)
        elif new_mode == CODE_SCREEN:
            pass
        elif new_mode == DRILL_SCREEN:
            pass
        elif new_mode == TIP_SCREEN:
            pass


def main_menu(screen):

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

        screen.fill(pygame.Color("White"))
        pygame.display.update()

    # Once the loop has ended, quit the application
    pygame.quit()


if __name__ == '__main__':
    main()
