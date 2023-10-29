

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

        if self.child is not None:  # Move the child with the mouse when holding
            self.child.hold((mouse_pos[0], mouse_pos[1] + self.height))

        if self.parent is not None and self.parent.y + self.parent.height != self.y:
            print("real")
            self.parent.child = None
            self.parent = None

    def shift(self, deltas):  # scrolling
        self.x = self.real_x + deltas[0]
        self.y = self.real_y + deltas[1]

    def assign_parent(self, parent_block):
        if parent_block is None:
            if self.parent is not None:
                self.parent.child = None
                self.parent = None
        elif parent_block.child == self:
            self.real_x = parent_block.real_x
            self.real_y = parent_block.real_y + parent_block.height

            self.x = parent_block.x
            self.y = parent_block.y + parent_block.height
        elif parent_block.child is not None:
            pass
        else:
            parent_block.child = self
            self.parent = parent_block
            self.real_x = parent_block.real_x
            self.real_y = parent_block.real_y + parent_block.height

            self.x = parent_block.x
            self.y = parent_block.y + parent_block.height
            parent_block.child = self

            if self.child is not None:  # Move child to the new location in a chain
                self.child.assign_parent(self)

    def get_children(self):
        if self.child is None:
            return []

        children = [self.child] + self.child.get_children()
        return children

    def highlight_adjacency(self, surface):
        pygame.draw.rect(surface, (255, 255, 155),
                         (self.x, self.y + self.height - 2, self.width, 3), 0, self.radius)


class Main(CodeBlock):
    def __init__(self, position, is_template):
        self.width = 200
        self.height = 30
        super().__init__((255, 0, 0),
                         (position[0], position[1], self.width, self.height), is_template, "Main")

        '''
        Moves the drill forwards in the current direction and removes the block in its new position
        '''

        self.string_code = """

# This is the main code it really doesn't do shit lolololol ok fuck

        """


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
        

self.col = min(max(0, self.col + self.direction[0]), SCREEN_WIDTH // BLOCK_SIZE - 1)
self.row += self.direction[1]

self.x += self.direction[0] * BLOCK_SIZE

if self.world.block_map[self.row][self.col] == BlockMaterial.LAVA.value:
    self.die()
else:
    wait_time = WAIT_TIMES[self.world.block_map[self.row][self.col]]
    
    time.sleep(wait_time)
    self.world.block_map[self.row][self.col] = BlockMaterial.EMPTY.value
        
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

self.direction = (-self.direction[1], self.direction[0])
            
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

self.direction = (self.direction[1], -self.direction[0])

        """


class Test(CodeBlock):
    def __init__(self, position, is_template):
        self.width  = 200
        self.height = 30
        super().__init__((0, 0, 255), (position[0], position[1], self.width, self.height), is_template, "Test")

        '''
        Turns the Drill Right (90°)
        Rotation: Direction(x, y) -> Direction(y, -x)
        '''

        self.string_code = """

print(333)

        """






