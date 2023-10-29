import random
import time

from objects import *
import math


class World:
    def __init__(self):

        self.block_screen = []  # Block objects
        self.block_map = []  # ints referring to block type
        self.block_preloaded_images = []

        for image_file in BLOCK_IMAGES:
            if image_file != "":
                self.block_preloaded_images.append(pygame.image.load(image_file).convert_alpha())
            else:
                self.block_preloaded_images.append(None)

    def initialize_block_map(self):
        self.block_map = []

        for y in range(WORLD_DEPTH):
            block_row = []
            for x in range(SCREEN_WIDTH // BLOCK_SIZE):

                lower_bound = int(BlockMaterial.DIRT.value)
                upper_bound = min(max(y // BIOME_SIZE, BlockMaterial.COAL.value), len(BLOCK_NAMES)-1)
                material_type = BlockMaterial.EMPTY.value

                # air is independent
                non_empty_chance = 80 + (y // 4)
                if random.randint(0, 100) < non_empty_chance or y < 2:
                    material_type = random.randint(lower_bound, upper_bound)

                block_row.append(material_type)
            self.block_map.append(block_row)

    def initialize_block_screen(self):
        for y in range(0, SCREEN_HEIGHT // BLOCK_SIZE, 1):
            block_screen_row = []
            for x in range(0, SCREEN_WIDTH // BLOCK_SIZE, 1):
                block_screen_row.append(Block(BlockMaterial.EMPTY.value, (y - CENTER_Y // BLOCK_SIZE), x,
                                                self.block_preloaded_images[BlockMaterial.EMPTY.value]))

            self.block_screen.append(block_screen_row)

    def update_block_screen(self, drill_row):
        accepted_x_start = 0  # for future scrolling: math.floor(drill.col) - HEIGHT / BLOCK_SIZE

        # Translating from middle left as origin to top left as origin
        # Drill row + 1 because blocks start one row after the drill's row

        accepted_y_start = (drill_row - 1) + CENTER_Y // BLOCK_SIZE
        print(accepted_y_start)

        for y in range(0, SCREEN_HEIGHT // BLOCK_SIZE, 1):
            if y - max(SCREEN_HEIGHT // BLOCK_SIZE - accepted_y_start, 0) < 0:
                continue

            for x in range(accepted_x_start, accepted_x_start + SCREEN_WIDTH // BLOCK_SIZE, 1):

                current_block_material = self.block_map[drill_row + y - CENTER_Y // BLOCK_SIZE][x]

                self.block_screen[y][x].update_block(current_block_material,
                                                     self.block_preloaded_images[current_block_material])


class Drill(ImageRectObject):
    def __init__(self, world):
        #                                   x        y   width height
        super().__init__(NO_COLOR, (8 * BLOCK_SIZE, CENTER_Y, 50, 50), 0, 0, "images/drill.png")

        self.row = 0
        self.col = 8
        self.direction = DIRECTIONS["south"]
        self.world = world
        self.inventory = []

        self.main_block = None
        self.real_code_blocks = []

    def call_main(self):

        """
        This will execute whatever is stored inside the file which is the string code.
        The string code will be compiled in another file so the string code should automatically work to alter
        variables in the drill itself, and the world if necessary

        """

        compiling = True
        next_block = self.main_block.child

        code_string = ""
        while compiling:
            code_string += next_block.string_code

            if next_block.child is None:
                break

            next_block = next_block.child

        print(code_string)

        exec(code_string)

        print(self.row)
        print(self.world.block_map[self.row][self.col])
        self.world.update_block_screen(self.row)

    def die(self):
        pass

