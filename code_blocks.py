

from objects import *


class CodeBlock(RectTextObject):
    def __init__(self, color, rect, is_template, text='', text_color=(216, 222, 233), text_size=20):
        super().__init__(color, rect, 0, 8, text, text_color, text_size)

        self.is_template = is_template
        self.string_code = ""
        self.parent = None
        self.child = None


class DrillForwards(CodeBlock):
    def __init__(self, is_template):
        super().__init__((0, 0, 255), is_template, "Drill Forwards")

        '''
        Moves the drill forwards in the current direction and removes the block in its new position
        '''

        self.string_code = """
        
        self.col += self.direction[0]
        self.row += self.direction[1]
        
        self.world.block_map[self.col][self.row] = BLOCK_NAMES.index("EMPTY")
        
        """


class Turn(CodeBlock):
    def __init__(self, is_template):
        super().__init__((0, 0, 255), is_template, "Drill Forwards")

        '''
        Moves the drill forwards in the current direction and removes the block in its new position
        '''

        self.string_code = """

        if self.direction[0] == 0:
            

        """






