import random

from objects import *
import math


class World:
    def __init__(self, seed):

        self.block_screen = [] #Block objects
        self.seed = seed
        self.block_map = [] #ints referring to block type

    def initialize_block_map(self):
        self.block_map = []

        for i in range(20):
            block_row = []
            for j in range(SCREEN_WIDTH // BLOCK_SIZE):

                lower_bound = int(BlockMaterial.DIRT.value)
                upper_bound = min(max(i // BIOME_SIZE, BlockMaterial.COAL.value), len(BLOCK_NAMES)-1)
                material_type = BlockMaterial.EMPTY.value

                # air is independent
                non_empty_chance = 30 + (i // 4)
                if random.randint(0, 100) < non_empty_chance or i < 2:
                    material_type = random.randint(lower_bound, upper_bound)
                    
                
                
                # random ([lowerbound, upperbound])
                # if max_index <= 2:
                #     material_type = (seed + (j+1) % (i+1)) % (max_index+3) + 1
                # elif (seed+i) % 3 > 0:
                #     if seed // 10 % 9 <= 1:
                #         material_type = BlockMaterial.EMPTY
                #     elif seed // 10 % 9 <= 5:
                #         material_type = BlockMaterial.DIRT
                #     elif seed // 10 % 9 <= 7:
                #         material_type = BlockMaterial.STONE
                #     else:
                #         material_type = BlockMaterial.LAVA
                # else:
                #     material_type = (seed + (j+1) % (i+1) + 1) % (max_index+1) + 1

                block_row.append(material_type)
            self.block_map.append(block_row)

    def initialize_block_screen(self):
        for i in range(0, SCREEN_WIDTH // BLOCK_SIZE, 1):
            # domain restriction is wrong
            # if (i < 0):
            #    continue
            for j in range(0, SCREEN_HEIGHT // BLOCK_SIZE, 1):
                self.block_screen[i][j] = Block(BlockMaterial.EMPTY.value, i, j)

    def update_block_screen(self, drill_col, drill_row):
        accepted_x_start = 0  # for future scrolling: math.floor(drill.col) - HEIGHT / BLOCK_SIZE
        accepted_y_start = math.floor(drill_row) - SCREEN_HEIGHT / BLOCK_SIZE

        for i in range(accepted_x_start, accepted_x_start + SCREEN_WIDTH // BLOCK_SIZE, 1):
            # domain restriction is wrong
            # if (i < 0):
            #    continue
            for j in range(accepted_y_start, accepted_y_start + SCREEN_HEIGHT // BLOCK_SIZE, 1):
                self.block_screen[i][j].update_block(self.block_map[i][j])


class Drill(ImageRectObject):
    def __init__(self, world):
        #                                   x        y   width height
        super().__init__(NO_COLOR, (CENTER_X, CENTER_Y, 50, 50), 0, 0, "images/drill.png")

        self.row = 0
        self.col = 0
        self.direction = DIRECTIONS["south"]
        self.world = world


    def call_main(self):

        """
        This will execute whatever is stored inside the file which is the string code.
        The string code will be compiled in another file so the string code should automatically work to alter
        variables in the drill itself, and the world if necessary

        """
        pass
