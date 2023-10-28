

from objects import *


class BackgroundDot(RectObject):
    def __init__(self, position):
        self.real_x = position[0]
        self.real_y = position[1]
        super().__init__(LAYER_COLORS[2], (position[0], position[1], 1, 1), 0, 0)

    def shift(self, deltas):
        self.x = self.real_x + deltas[0] % 20
        self.y = self.real_y + deltas[1] % 20


class CodeBlock(RectTextButton):
    def __init__(self, color, rect, is_template, text='', text_color=(216, 222, 233), text_size=20):
        super().__init__(color, rect, 0, 2, "codeblock:empty", text, text_color, text_size)

        self.real_x = self.x  # top left
        self.real_y = self.y

        self.is_template = is_template
        self.string_code = ""
        self.parent = None
        self.child = None  # blocks that are attached to bottom
        # self.nested_children = []

    def hold(self, mouse_pos):
        new_x = mouse_pos[0] - self.width // 2
        new_y = mouse_pos[1] - self.height // 2

        # Change the real position when the mouse is moving it
        self.real_x += new_x - self.x
        self.real_y += new_y - self.y

        self.x = new_x
        self.y = new_y

        if self.child is not None:
            self.child.hold((mouse_pos[0], mouse_pos[1] + self.height))

    def shift(self, deltas):  # scrolling
        self.x = self.real_x + deltas[0]
        self.y = self.real_y + deltas[1]

    def assign_parent(self, parent_block):
        if parent_block.child is not None:
            pass
        if parent_block is None:
            if self.parent is not None:
                self.parent.child = None
                self.parent = None
        else:
            parent_block.child = self
            self.parent = parent_block  # this oop does not copy the object right
            self.real_x = parent_block.real_x
            self.real_y = parent_block.real_y + parent_block.height

            self.x = parent_block.x
            self.y = parent_block.y + parent_block.height
            parent_block.child = self

    def get_children(self):
        if self.child is None:
            return []

        children = [self.child] + self.child.get_children()
        return children

    def highlight_adjacency(self, surface):
        pygame.draw.rect(surface, (255, 255, 255),
                         (self.x, self.y + self.height - 1, self.width, 2), 0, self.radius)


class DrillForwards(CodeBlock):
    def __init__(self, position, is_template):
        self.width  = 200
        self.height = 30
        super().__init__((0, 0, 255),
                         (position[0], position[1], self.width, self.height), is_template, "Drill Forwards")

        '''
        Moves the drill forwards in the current direction and removes the block in its new position
        '''

        self.string_code = """
        
        self.col += self.direction[0]
        self.row += self.direction[1]
        
        self.world.block_map[self.col][self.row] = BLOCK_NAMES.index("EMPTY")
        
        """


class TurnLeft(CodeBlock):
    def __init__(self, position, is_template):
        self.width  = 200
        self.height = 30
        super().__init__((0, 0, 255), (position[0], position[1], self.width, self.height), is_template, "Turn Left")

        '''
        Turns the Drill Left (-90°)
        Rotation: Direction(x, y) -> Direction(-y, x)
        '''

        self.string_code = """

        (self.direction[0], self.direction[1]) = (-self.direction[1], self.direction[0])
            
        """


class TurnRight(CodeBlock):
    def __init__(self, position, is_template):
        self.width  = 200
        self.height = 30
        super().__init__((0, 0, 255), (position[0], position[1], self.width, self.height), is_template, "Turn Right")

        '''
        Turns the Drill Right (90°)
        Rotation: Direction(x, y) -> Direction(y, -x)
        '''

        self.string_code = """

        (self.direction[0], self.direction[1]) = (self.direction[1], -self.direction[0])

        """






