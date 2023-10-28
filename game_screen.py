
from drill import *

import math


def game_screen(screen, world, drill):

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


def draw_blocks(screen, world, drill):
    for i in range(0, math.floor(SCREEN_WIDTH / BLOCK_SIZE), 1):
        for j in range(0, math.floor(SCREEN_HEIGHT / BLOCK_SIZE), 1):
            world.block_screen[i][j].draw(screen, False)



