
from objects import *


def code_screen(screen):

    # ----------------- Initializing Objects -----------------
    # Used to determine which objects are selected
    selected_object = None

    basic_objects = [
        RectObject((197, 203, 214), (0, 0, 200, SCREEN_HEIGHT), 0, 0),
        RectObject((197, 203, 214), (SCREEN_WIDTH - 200, 0, 200, SCREEN_HEIGHT), 0, 0),
        RectObject((255, 203, 214), (0, 0, 50, 50), 0, 0),
    ]

    buttons = [
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 20, 180, 40), 0, 0,
                       "menu:0", "Menu", (197, 203, 214), 30),
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 70, 180, 40), 0, 0,
                       "menu:2", "Drill", (197, 203, 214), 30),
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 120, 180, 40), 0, 0,
                       "menu:3", "Tips", (197, 203, 214), 30),
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
        draw_basic_objects(screen, basic_objects)
        draw_buttons(screen, selected_object, buttons)

        pygame.display.update()

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

