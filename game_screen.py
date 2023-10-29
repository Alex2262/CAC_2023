
from drill import *

import math


def game_screen(screen, world, drill):

    # ----------------- Initializing Objects -----------------

    clock = pygame.time.Clock()  # Clock for adjusting the frames per second
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

            # ----------------- Mouse Released -----------------
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                selected_object = get_selected_object(mouse_pos, buttons)

                if selected_object is None:
                    continue

                actions = selected_object.action.split(":")

                if actions[0] == "menu":

                    if actions[1] != MAIN_MENU:
                        return int(actions[1])

        mouse_pos = pygame.mouse.get_pos()
        selected_object = get_selected_object(mouse_pos, buttons)

        screen.fill(pygame.Color("White"))
        pygame.display.update()

        # time += 1
        # if time % 60 == 0 and time >= 300:  # Wait 5 seconds
        #     drill.call_main()

    return -1


# If the mouse is touching an object that can be selected, return it.
# Else, return None for no selected object
def get_selected_object(mouse_pos, buttons):
    for button in buttons:
        if button.is_selecting(mouse_pos):
            return button

    return None


def draw_blocks(screen, world):
    for y in range(0, SCREEN_HEIGHT // BLOCK_SIZE, 1):
        for x in range(0, SCREEN_WIDTH // BLOCK_SIZE, 1):
            world.block_screen[y][x].draw(screen, False)


def draw_buttons(screen, selected_object, buttons):
    for button in buttons:
        button.draw(screen, selected_object == button)



