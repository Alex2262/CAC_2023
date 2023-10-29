
import threading
from drill import *

import math


def game_screen(screen, world, drill):

    # ----------------- Initializing Objects -----------------

    drill_thread = None
    clock = pygame.time.Clock()  # Clock for adjusting the frames per second
    selected_object = None

    buttons = [
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 20, 180, 40), 0, 2,
                       "menu:0", "Menu", (197, 203, 214), 30),
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 70, 180, 40), 0, 2,
                       "menu:1", "Code", (197, 203, 214), 30),
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 120, 180, 40), 0, 2,
                       "menu:3", "Tips", (197, 203, 214), 30),
    ]

    backdrop = ImageRectObject(NO_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0, "backdrops/Backdrop1.png")
    backdrop.image = pygame.transform.scale(backdrop.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    time = 0

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

        # update biome
        # backdrop.image = BACKDROPS[drill.row // BIOME_SIZE]
        backdrop.draw(screen, selected_object)

        draw_blocks(screen, world)
        draw_buttons(screen, selected_object, buttons)
        drill.draw(screen, selected_object)

        clock.tick(60)
        pygame.display.update()

        if not drill.running:
            if drill_thread is not None:
                drill_thread.join()

            drill_thread = threading.Thread(target=drill.call_main, args=())
            drill_thread.start()
            #bug: for a script with multiple blocks it needs to update the screen every time a block is run. Currently, it only moves after a sequence of blocks is compiled.

        if drill.energy < 0:
            drill.die()

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



