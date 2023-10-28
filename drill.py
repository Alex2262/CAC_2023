
from objects import *
import math


class World:
    def __init__(self):
        self.block_map = []
        self.block_screen = []

    def initialize_block_map(self):
        pass

    def initialize_block_screen(self):
        for i in range(0, math.floor(SCREEN_WIDTH / BLOCK_SIZE), 1):
            # domain restriction is wrong
            # if (i < 0):
            #    continue
            for j in range(0, math.floor(SCREEN_HEIGHT / BLOCK_SIZE), 1):
                self.block_screen[i][j] = Block(0, i, j)

    def update_block_screen(self, drill_col, drill_row):
        accepted_x_start = 0  # for future scrolling: math.floor(drill.col) - HEIGHT / BLOCK_SIZE
        accepted_y_start = math.floor(drill_row) - SCREEN_HEIGHT / BLOCK_SIZE

        for i in range(accepted_x_start, accepted_x_start + math.floor(SCREEN_WIDTH / BLOCK_SIZE), 1):
            # domain restriction is wrong
            # if (i < 0):
            #    continue
            for j in range(accepted_y_start, accepted_y_start + math.floor(SCREEN_HEIGHT / BLOCK_SIZE), 1):
                self.block_screen[i][j].update_block(self.block_map[i][j])


class Drill(ImageRectObject):
    def __init__(self, world):
        #                                   x        y   width height
        super().__init__(NO_COLOR, (CENTER_X, CENTER_Y, 50, 50), 0, 0, "images/drill.png")

        self.row = 0
        self.col = 0
        self.direction = DIRECTIONS["south"]
        self.world = world
