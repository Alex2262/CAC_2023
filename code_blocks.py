

from objects import *

BASIC_CODE_BLOCK_HEIGHT = 30
BASIC_CODE_BLOCK_WIDTH  = 200
CONTAINER_LEFT_MARGIN   = 20

FAILED_ATTACHMENT = -1
BASIC_MODE = 0
NEST_MODE = 1
PARAMETER_MODE = 2


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
        self.bottom_child = None  # blocks that are attached to bottom
        self.nested_child = None
        self.parameters = []  # Takes 0 parameters

    def update_height(self):
        if self.parent is not None:
            self.parent.update_height()

    def hold(self, mouse_pos):
        new_x = mouse_pos[0] - self.width // 2
        new_y = mouse_pos[1] - self.height // 2

        if self.is_container:  # For containers, hold the top rectangle, not the center
            new_y = mouse_pos[1] - BASIC_CODE_BLOCK_HEIGHT // 2

        # Change the real position when the mouse is moving it
        self.real_x += new_x - self.x
        self.real_y += new_y - self.y

        self.x = new_x
        self.y = new_y

        self.relocate_children()

        if self.parent is not None:

            # Removing a nested block
            if self.parent.is_container and self.parent.nested_child == self and\
               self.parent.y + BASIC_CODE_BLOCK_HEIGHT != self.y:
                self.parent.nested_child = None

                # Adjust the parent container's bottom children once this nested block is remove
                self.parent.update_height()
                self.parent = None

            # Removing a normal block
            elif self.parent.bottom_child == self and self.parent.y + self.parent.height != self.y:
                self.parent.bottom_child = None
                self.parent = None

    def shift(self, deltas):  # scrolling
        self.x = self.real_x + deltas[0]
        self.y = self.real_y + deltas[1]

    def get_attachment_mode(self, position):
        return BASIC_MODE

    def relocate_children(self):
        if self.bottom_child is not None:  # Move child to the new location in a chain
            self.bottom_child.assign_parent(self, BASIC_MODE)
        for parameter in self.parameters:
            if parameter is not None:
                parameter.assign_parent(self, PARAMETER_MODE)

    def assign_parent(self, parent_block, attachment_mode):

        if attachment_mode == BASIC_MODE:
            # Removing Parent
            if parent_block is None:
                if self.parent is not None:
                    self.parent.bottom_child = None
                    self.parent = None
                return

            self.real_x = parent_block.real_x
            self.real_y = parent_block.real_y + parent_block.height

            self.x = parent_block.x
            self.y = parent_block.y + parent_block.height

            self.relocate_children()

            # Guard clause, parent child is self
            if parent_block.bottom_child == self:
                return

            self.parent = parent_block

            # Insertion
            if parent_block.bottom_child is not None:
                # Move the parent's old child to the end of this block's chain
                chain = [self] + self.get_children()
                parent_block.bottom_child.assign_parent(chain[-1], BASIC_MODE)  # Ignore useless warning

            parent_block.bottom_child = self
            parent_block.update_height()

        elif attachment_mode == NEST_MODE:  # Parent must be of Container type
            # Removing Parent
            if parent_block is None:
                if self.parent is not None:
                    self.parent.nested_child = None
                    self.parent = None
                return

            self.real_x = parent_block.real_x + CONTAINER_LEFT_MARGIN
            self.real_y = parent_block.real_y + BASIC_CODE_BLOCK_HEIGHT

            self.x = parent_block.x + CONTAINER_LEFT_MARGIN
            self.y = parent_block.y + BASIC_CODE_BLOCK_HEIGHT

            self.relocate_children()

            # Guard clause, parent child is self
            if parent_block.nested_child == self:
                return

            self.parent = parent_block

            # Insertion
            if parent_block.nested_child is not None:
                # Move the parent's old child to the end of this block's chain
                chain = [self] + self.get_children()
                parent_block.nested_child.assign_parent(chain[-1], BASIC_MODE)  # Ignore useless warning
                parent_block.update_height()

            parent_block.nested_child = self
            parent_block.update_height()

            # Parent's Block Height is updated so push bottom blocks down
            if parent_block.bottom_child is not None:
                parent_block.bottom_child.assign_parent(parent_block, BASIC_MODE)

    def get_children(self):
        if self.bottom_child is None:
            return []

        children = [self.bottom_child] + self.bottom_child.get_children()
        return children

    def highlight_adjacency(self, surface, mode):
        pygame.draw.rect(surface, (255, 255, 155),
                         (self.x, self.y + self.height - 2, self.width, 3), 0, self.radius)


class Container(CodeBlock):
    def __init__(self, color, position, is_template, text='', text_color=(216, 222, 233), text_size=20):
        super().__init__(color, (position[0], position[1], self.width, self.height),
                         is_template, text, text_color, text_size)
        self.is_container = True
        self.nested_child = None
        self.update_height()

    def update_height(self):
        super().update_height()

        top_rect_height = BASIC_CODE_BLOCK_HEIGHT
        left_rect_height = max(len(self.get_nested_children()) * BASIC_CODE_BLOCK_HEIGHT, BASIC_CODE_BLOCK_HEIGHT // 2)
        bottom_rect_height = BASIC_CODE_BLOCK_HEIGHT
        self.height = top_rect_height + left_rect_height + bottom_rect_height

        if self.bottom_child is not None:
            self.bottom_child.assign_parent(self, BASIC_MODE)

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

    def hold(self, mouse_pos):
        super().hold(mouse_pos)
        if self.nested_child is not None:
            self.nested_child.hold((mouse_pos[0] + CONTAINER_LEFT_MARGIN, mouse_pos[1] + BASIC_CODE_BLOCK_HEIGHT))

    def get_nested_children(self):
        if self.nested_child is None:
            return []

        return [self.nested_child] + self.nested_child.get_children()

    def get_attachment_mode(self, position):
        # Assumes the object has been selected
        top_rect_height = BASIC_CODE_BLOCK_HEIGHT
        left_rect_height = max(len(self.get_nested_children()) * BASIC_CODE_BLOCK_HEIGHT, BASIC_CODE_BLOCK_HEIGHT // 2)
        # bottom_rect_height = BASIC_CODE_BLOCK_HEIGHT

        # NESTING ATTACHMENT MODE
        if position[1] < self.y + top_rect_height:
            return NEST_MODE

        if position[1] < self.y + top_rect_height + left_rect_height:
            return FAILED_ATTACHMENT

        return BASIC_MODE

    def relocate_children(self):
        super().relocate_children()
        if self.nested_child is not None:  # Move nested child to the new location in a chain
            print(self.x, self.y, self.nested_child.x, self.nested_child.y)
            self.nested_child.assign_parent(self, NEST_MODE)
            print(self.x, self.y, self.nested_child.x, self.nested_child.y)

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

    def highlight_adjacency(self, surface, mode):
        top_rect_height = BASIC_CODE_BLOCK_HEIGHT
        if mode == NEST_MODE:
            pygame.draw.rect(surface, (255, 255, 155),
                             (self.x + CONTAINER_LEFT_MARGIN, self.y + top_rect_height - 2,
                              self.width - CONTAINER_LEFT_MARGIN, 3), 0, self.radius)
        else:
            pygame.draw.rect(surface, (255, 255, 155),
                            (self.x, self.y + self.height - 2, self.width, 3), 0, self.radius)


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
        self.height = 1
        super().__init__((245, 200, 0),
                         (position[0], position[1], self.width, self.height), is_template, "if")

        '''
        Conditional
        '''

        self.string_code = """
        
if {parameters}:

        """






