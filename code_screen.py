
from objects import *


def code_screen(screen):

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


