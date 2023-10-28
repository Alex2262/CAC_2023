
from code_blocks import *

CODE_BLOCK_TEMPLATES_MARGIN = 230
RIGHT_SIDE_BAR_MARGIN = SCREEN_WIDTH - 200


def code_screen(screen):

    # ----------------- Initializing Objects -----------------
    # Used to determine which objects are selected
    selected_object = None

    first_mouse_pos = (0, 0)
    last_canvas_delta = (0, 0)
    canvas_delta = (0, 0)
    scrolling = False

    # Used for creating the template code blocks
    all_code_blocks = [
        DrillForwards,
        TurnLeft,
        TurnRight
    ]

    background_dots = []

    basic_objects = [
        RectObject((197, 203, 214), (0, 0, CODE_BLOCK_TEMPLATES_MARGIN, SCREEN_HEIGHT), 0, 0),
        RectObject((197, 203, 214), (RIGHT_SIDE_BAR_MARGIN, 0, 200, SCREEN_HEIGHT), 0, 0),
        DrillForwards((10, 10, 180, 30), True),
    ]

    buttons = [
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 20, 180, 40), 0, 0,
                       "menu:0", "Menu", (197, 203, 214), 30),
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 70, 180, 40), 0, 0,
                       "menu:2", "Drill", (197, 203, 214), 30),
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 120, 180, 40), 0, 0,
                       "menu:3", "Tips", (197, 203, 214), 30),
        RectTextButton((150, 157, 171), (SCREEN_WIDTH - 190, 500, 180, 40), 0, 0,
                       "zoom:center", "Center", (197, 203, 214), 30),
    ]

    real_code_blocks = []

    # Create the background dots
    for b_x in range(CODE_BLOCK_TEMPLATES_MARGIN, RIGHT_SIDE_BAR_MARGIN, 20):
        for b_y in range(0, SCREEN_HEIGHT, 20):
            background_dots.append(BackgroundDot((b_x, b_y)))

    # Create the template code blocks
    code_block_template_y = 10
    for code_block in all_code_blocks:
        buttons.append(code_block((10, code_block_template_y), True))
        code_block_template_y += basic_objects[-1].height + 10  # +10 for the space in between each code block

    current_code_object = None

    # ----------------- The Main GUI Loop -----------------
    running = True
    while running:

        # ----------------- Looping through Pygame Events -----------------
        for event in pygame.event.get():

            # Quit Pygame
            if event.type == pygame.QUIT:
                running = False
                break

            # ----------------- Mouse Clicked -----------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                selected_object = get_selected_object(mouse_pos, buttons + real_code_blocks)

                if selected_object is None:
                    if CODE_BLOCK_TEMPLATES_MARGIN < mouse_pos[0] < RIGHT_SIDE_BAR_MARGIN:
                        first_mouse_pos = mouse_pos
                        scrolling = True
                    continue

                actions = selected_object.action.split(":")

                if actions[0] == "codeblock":

                    if selected_object.is_template:
                        real_code_blocks.append(type(selected_object)((10, selected_object.real_y), False))
                        current_code_object = real_code_blocks[-1]
                    elif CODE_BLOCK_TEMPLATES_MARGIN < mouse_pos[0] < RIGHT_SIDE_BAR_MARGIN:
                        current_code_object = selected_object

            # ----------------- Mouse Released -----------------
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                selected_object = get_selected_object(mouse_pos, buttons + real_code_blocks)

                if current_code_object is not None:
                    # block held over the deletion area
                    if mouse_pos[0] < CODE_BLOCK_TEMPLATES_MARGIN:
                        real_code_blocks.remove(current_code_object)

                    # block is held near the bottom of another block
                    adjacent_block = find_adjacent_block(current_code_object, real_code_blocks)
                    if adjacent_block is not None:
                        current_code_object.assign_parent(adjacent_block)
                    else:
                        # Map the real x and y accordingly
                        current_code_object.real_x -= canvas_delta[0]
                        current_code_object.real_y -= canvas_delta[1]

                current_code_object = None  # Have stopped holding any code blocks

                scrolling = False
                last_canvas_delta = canvas_delta

                if selected_object is None:
                    continue

                actions = selected_object.action.split(":")

                if actions[0] == "menu":

                    if actions[1] != MAIN_MENU:
                        return int(actions[1])

                if actions[0] == "zoom":
                    if actions[1] == "center":
                        last_canvas_delta = (0, 0)
                        canvas_delta = (0, 0)
                        shift_code_blocks(real_code_blocks, canvas_delta)
                        shift_background_dots(background_dots, canvas_delta)

        mouse_pos = pygame.mouse.get_pos()
        selected_object = get_selected_object(mouse_pos, buttons)

        # Shifting / Scrolling
        if scrolling:
            deltas = (mouse_pos[0] - first_mouse_pos[0], mouse_pos[1] - first_mouse_pos[1])

            canvas_delta = (last_canvas_delta[0] + deltas[0], last_canvas_delta[1] + deltas[1])
            shift_code_blocks(real_code_blocks, canvas_delta)
            shift_background_dots(background_dots, canvas_delta)

        # Holding
        if current_code_object is not None:
            current_code_object.hold(mouse_pos)

        screen.fill(MENU_SCREEN_COLOR)

        draw_basic_objects(screen, background_dots)
        draw_buttons(screen, selected_object, real_code_blocks)
        draw_basic_objects(screen, basic_objects)
        draw_buttons(screen, selected_object, buttons)

        # Redraw the current code object on the top
        if current_code_object is not None:
            draw_buttons(screen, selected_object, [current_code_object])

        pygame.display.update()

    return -1


# If the mouse is touching an object that can be selected, return it.
# Else, return None for no selected object
def get_selected_object(mouse_pos, buttons):
    for button in buttons:
        if button.is_selecting(mouse_pos):
            return button

    return None


def shift_code_blocks(code_blocks, deltas):
    for code_block in code_blocks:
        code_block.shift(deltas)


def shift_background_dots(background_dots, deltas):
    for background_dot in background_dots:
        background_dot.shift(deltas)


def draw_basic_objects(screen, basic_objects):
    for basic_object in basic_objects:
        basic_object.draw(screen, False)


def draw_buttons(screen, selected_object, buttons):
    for button in buttons:
        button.draw(screen, selected_object == button)

