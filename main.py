# Import modules and code/classes/objects from other files
import math
import random

import pygame.font

from objects import *

from drill import World, Drill
from game_screen import game_screen
from code_screen import code_screen


# The Main function
def main():
    # ----------------- Initializing Pygame Variables -----------------
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # The initial Pygame Screen
    clock = pygame.time.Clock()  # Clock for adjusting the frames per second

    time = 0  # Used for keeping track of seconds (60 ticks per second)

    screen.fill(MENU_SCREEN_COLOR)
    pygame.display.update()
    pygame.display.set_caption("Drill Blocks")  # Game Name?

    new_menu = 0

    world = World(0)
    seed = random.randrange(100000, 999999)
    world.initialize_block_map()
    print(world.block_map)
    print(seed)
    drill = Drill(world)

    while True:
        if new_menu == -1:
            break
        elif new_menu == MAIN_MENU:
            new_menu = main_menu(screen)
        elif new_menu == CODE_SCREEN:
            new_menu = code_screen(screen)
        elif new_menu == DRILL_SCREEN:
            new_menu = game_screen(screen, world, drill)
        elif new_menu == TIP_SCREEN:
            pass

    pygame.quit()


# The main menu which you enter the game in
def main_menu(screen):

    # ----------------- Initializing Objects -----------------
    # Used to determine which objects are selected

    selected_object = None

    buttons = [
        RectTextButton((46, 52, 64), (CENTER_X - 300, CENTER_Y, 600, 60), 0, 0,
                       "menu:1", "Code", (76, 86, 106), 44),
        RectTextButton((46, 52, 64), (CENTER_X - 300, CENTER_Y + 70, 600, 60), 0, 0,
                       "menu:2", "Drill", (76, 86, 106), 44),
        RectTextButton((46, 52, 64), (CENTER_X - 300, CENTER_Y + 140, 600, 60), 0, 0,
                       "menu:3", "Tips", (76, 86, 106), 44),
    ]

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

        screen.fill(MENU_SCREEN_COLOR)
        # draw_basic_objects(screen, basic_objects)
        draw_buttons(screen, selected_object, buttons)

        pygame.display.update()

    # Exit the application
    return -1


# If the mouse is touching an object that can be selected, return it.
# Else, return None for no selected object
def get_selected_object(mouse_pos, buttons):
    for button in buttons:
        if button.is_selecting(mouse_pos):
            return button

    return None


def draw_basic_objects(screen, basic_objects):
    for basic_object in basic_objects:
        basic_object.draw(screen, False)


def draw_buttons(screen, selected_object, buttons):
    for button in buttons:
        button.draw(screen, selected_object == button)


if __name__ == '__main__':
    main()
