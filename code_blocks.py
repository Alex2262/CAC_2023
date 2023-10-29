

from objects import *

BASIC_CODE_BLOCK_HEIGHT = 30
BASIC_CODE_BLOCK_WIDTH  = 200
CONTAINER_LEFT_MARGIN   = 20


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
        self.is_container = False
        self.is_parameter = False

        self.string_code = ""
        self.parent = None
        self.child = None  # blocks that are attached to bottom
        self.parameters = []  # Takes 0 parameters

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
            self.parent.child = None
            self.parent = None

    def shift(self, deltas):  # scrolling
        self.x = self.real_x + deltas[0]
        self.y = self.real_y + deltas[1]

    def relocate_children(self):
        if self.child is not None:  # Move child to the new location in a chain
            self.child.assign_parent(self)
        for parameter in self.parameters:
            if parameter is not None:
                parameter.assign_parent(self)

    def assign_parent(self, parent_block):

        # Removing Parent
        if parent_block is None:
            if self.parent is not None:
                self.parent.child = None
                self.parent = None
            return

        x_margin = 0
        if parent_block.is_container and parent_block.nested_child == self:
            x_margin = CONTAINER_LEFT_MARGIN
        if self.is_parameter:
            x_margin = 30

        self.real_x = parent_block.real_x + x_margin
        self.real_y = parent_block.real_y + parent_block.height

        self.x = parent_block.x + x_margin
        self.y = parent_block.y + parent_block.height

        self.relocate_children()

        # Guard clause, parent child is self
        if parent_block.child == self:
            return

        self.parent = parent_block

        # Insertion
        if parent_block.child is not None:
            # Move the parent's old child to the end of this block's chain
            chain = [self] + self.get_children()
            parent_block.child.assign_parent(chain[-1])

        parent_block.child = self

    def get_children(self):
        if self.child is None:
            return []

        children = [self.child] + self.child.get_children()
        return children

    def highlight_adjacency(self, surface):
        pygame.draw.rect(surface, (255, 255, 155),
                         (self.x, self.y + self.height - 2, self.width, 3), 0, self.radius)


class Container(CodeBlock):
    def __init__(self, color, position, is_template, text='', text_color=(216, 222, 233), text_size=20):
        super().__init__(color, (position[0], position[1], self.width, self.height),
                         is_template, text, text_color, text_size)
        self.is_container = True
        self.nested_child = None

    def draw(self, surface, selected):
        top_rect_height = BASIC_CODE_BLOCK_HEIGHT
        left_rect_height = max(len(self.get_nested_children()) * BASIC_CODE_BLOCK_HEIGHT, BASIC_CODE_BLOCK_HEIGHT // 2)
        bottom_rect_height = BASIC_CODE_BLOCK_HEIGHT
        self.height = top_rect_height + left_rect_height + bottom_rect_height

        left_rect_width = CONTAINER_LEFT_MARGIN

        # TOP RECT
        pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], 255),
                         (self.x, self.y, self.width, top_rect_height), self.border, self.radius)

        if self.text != '':
            self.text_surf = self.font.render(self.text, True, self.text_color)
            surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                          self.y + (top_rect_height / 2 - self.text_surf.get_height() / 2)))

        # LEFT RECT
        pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], 255),
                         (self.x, self.y + top_rect_height, left_rect_width, left_rect_height), self.border,
                         self.radius)

        # BOTTOM RECT
        pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], 255),
                         (self.x, self.y + top_rect_height + left_rect_height, self.width, bottom_rect_height),
                         self.border, self.radius)

        if selected:
            # TOP RECT
            new_surface = pygame.Surface((self.width, top_rect_height), pygame.SRCALPHA)
            new_surface.set_alpha(40)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y))

            # LEFT RECT
            new_surface = pygame.Surface((left_rect_width, left_rect_height), pygame.SRCALPHA)
            new_surface.set_alpha(40)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y + top_rect_height))

            # BOTTOM RECT
            new_surface = pygame.Surface((self.width, bottom_rect_height), pygame.SRCALPHA)
            new_surface.set_alpha(40)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y + top_rect_height + left_rect_height))

    def get_nested_children(self):
        if self.nested_child is None:
            return []

        return [self.nested_child] + self.nested_child.get_children()

    def relocate_children(self):
        if self.child is not None:  # Move child to the new location in a chain
            self.child.assign_parent(self)
        if self.nested_child is not None:  # Move nested child to the new location in a chain
            self.nested_child.assign_parent(self)

    def is_selecting(self, mouse_pos):
        top_rect_height = BASIC_CODE_BLOCK_HEIGHT
        left_rect_height = max(len(self.get_nested_children()) * BASIC_CODE_BLOCK_HEIGHT, BASIC_CODE_BLOCK_HEIGHT // 2)
        bottom_rect_height = BASIC_CODE_BLOCK_HEIGHT
        left_rect_width = CONTAINER_LEFT_MARGIN

        # TOP RECT
        if self.x < mouse_pos[0] < self.x + self.width and \
                self.y < mouse_pos[1] < self.y + top_rect_height:
            return True

        # LEFT RECT
        if self.x < mouse_pos[0] < self.x + left_rect_width and \
                self.y + top_rect_height < mouse_pos[1] < self.y + top_rect_height + left_rect_height:
            return True

        # BOTTOM RECT
        if self.x < mouse_pos[0] < self.x + self.width and \
                self.y + top_rect_height + left_rect_height < mouse_pos[1] < \
                self.y + top_rect_height + left_rect_height + bottom_rect_height:
            return True

        return False


class Main(CodeBlock):
    def __init__(self, position, is_template):
        self.width = BASIC_CODE_BLOCK_WIDTH
        self.height = BASIC_CODE_BLOCK_HEIGHT
        super().__init__((255, 0, 0),
                         (position[0], position[1], self.width, self.height), is_template, "Main")

        '''
        Moves the drill forwards in the current direction and removes the block in its new position
        '''

        self.string_code = """

        """


class DrillForwards(CodeBlock):
    def __init__(self, position, is_template):
        self.width  = BASIC_CODE_BLOCK_WIDTH
        self.height = BASIC_CODE_BLOCK_HEIGHT
        super().__init__((0, 0, 255),
                         (position[0], position[1], self.width, self.height), is_template, "Drill Forwards")

        '''
        Moves the drill forwards in the current direction and removes the block in its new position
        '''

        self.string_code = """
        
new_col = min(max(0, self.col + self.direction[0]), SCREEN_WIDTH // BLOCK_SIZE - 1)
new_row = self.row + self.direction[1]

if self.world.block_map[new_row][new_col] == BlockMaterial.LAVA.value:
    self.die()
else:
    wait_time = WAIT_TIMES[self.world.block_map[new_row][new_col]]
    
    time.sleep(wait_time / 1000.0)
    
    self.col = new_col
    self.row = new_row
    self.energy -= ENERGY_CONSUMPTIONS[self.world.block_map[new_row][new_col]]

    self.x += self.direction[0] * BLOCK_SIZE
    self.world.block_map[self.row][self.col] = BlockMaterial.EMPTY.value
        
        """


class TurnLeft(CodeBlock):
    def __init__(self, position, is_template):
        self.width  = BASIC_CODE_BLOCK_WIDTH
        self.height = BASIC_CODE_BLOCK_HEIGHT
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
        self.width  = BASIC_CODE_BLOCK_WIDTH
        self.height = BASIC_CODE_BLOCK_HEIGHT
        super().__init__((0, 0, 255), (position[0], position[1], self.width, self.height), is_template, "Turn Right")

        '''
        Turns the Drill Right (90°)
        Rotation: Direction(x, y) -> Direction(y, -x)
        '''

        self.string_code = """

self.direction = (self.direction[1], -self.direction[0])

        """


class Conditional(Container):
    def __init__(self, position, is_template):
        self.width = BASIC_CODE_BLOCK_WIDTH
        self.height = BASIC_CODE_BLOCK_HEIGHT
        super().__init__((245, 200, 0),
                         (position[0], position[1], self.width, self.height), is_template, "if")

        '''
        Conditional
        '''

        self.string_code = """
        
if {parameters}:

        """






