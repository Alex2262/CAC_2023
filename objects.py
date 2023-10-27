import pygame
from constants import *

'''
This is a file containing different objects, classes, and subclasses.
A lot of Object Oriented Programming exists in this file.
'''


# ----------------- The main Object class -----------------
class Object:
    def __init__(self, rect):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]


# ----------------- A rectangular Object -----------------
# (extends Object)
class RectObject(Object):
    # 3 panels
    def __init__(self, color, rect, border, radius):
        super().__init__(rect)
        self.color = color

        self.border = border
        self.radius = radius

    # Draw the item
    def draw(self, surface, selected):
        if len(self.color) < 4 or self.color[3] != 0:
            pygame.draw.rect(surface, self.color,
                             (self.x, self.y, self.width, self.height), self.border, self.radius)


# ----------------- A rectangular Object with an image -----------------
# (extends RectObject)
class ImageRectObject(RectObject):
    def __init__(self, color, rect, border, radius, image_file):
        super().__init__(color, rect, border, radius)
        self.image_file = image_file
        self.image = pygame.image.load(self.image_file).convert_alpha()

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))


# ----------------- The Rectangular Text Object -----------------
# (extends RectObject)
class RectTextObject(RectObject):
    # Displays the text
    def __init__(self, color, rect, border, radius, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius)

        self.text_size = text_size
        self.text = text
        self.text_color = text_color

        self.font = pygame.font.Font('fonts/AROneSans-SemiBold.ttf',
                                     text_size)
        self.text_surf = self.font.render(self.text, True, self.text_color)

    def draw(self, surface, selected):
        super().draw(surface, selected)
        if self.text != '':
            self.text_surf = self.font.render(self.text, True, self.text_color)
            surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                          self.y + (self.height / 2 - self.text_surf.get_height() / 2)))


# ----------------- The Image Rectangular Text Object -----------------
# (extends RectTextObject)
class ImageRectTextObject(RectTextObject):
    def __init__(self, color, rect, border, radius, image_file, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius, text, text_color, text_size)
        self.image_file = image_file
        self.image = pygame.image.load(self.image_file).convert_alpha()

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))
        self.text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                      self.y + (self.height / 2 - self.text_surf.get_height() / 2)))


# ----------------- Achievements -----------------
# (extends RectTextObject)
# Achievement text information that is shown when the user has reached a certain checkpoint
class AchievementText(RectTextObject):
    def __init__(self, color, rect, border, radius, text='', text_color=(0, 0, 0, 255), text_size=20):
        super().__init__(color, rect, border, radius, text, text_color, text_size)

    def draw(self, surface, selected):
        max_char_per_line = 2 * (self.width - 30) // self.text_size
        word_list = self.text.split()
        lines = []
        current_line = ""

        for i in range(len(word_list)):

            if len(current_line) + 1 + len(word_list[i]) > max_char_per_line:
                lines.append(current_line)
                current_line = ""  # NOTE: CHECK FOR COPYING

            current_line += word_list[i]
            current_line += " "

            if i == len(word_list) - 1:
                lines.append(current_line)
                break

        for i in range(len(lines)):
            self.text_surf = self.font.render(lines[i], True, self.text_color)
            surface.blit(self.text_surf, (self.x + 15, self.y + 15 + i * (self.height - 30) // len(lines)))


# ----------------- The Animated Text Object -----------------
# (extends RectTextObject)
# The text that appears when you click the earth (+1 pollution cleared
class AnimatedText(RectTextObject):
    # +1 pollution cleared
    def __init__(self, color, rect, border, radius, text='', text_color=(0, 0, 0, 255), text_size=20):
        super().__init__(color, rect, border, radius, text, text_color, text_size)

    def draw(self, surface, selected):
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_surf.set_alpha(self.text_color[3])
        surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                      self.y + (self.height / 2 - self.text_surf.get_height() / 2)))

    # rise and fade out
    def move(self):
        self.y -= 3
        self.text_color = (self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3] - 6)
        if self.y <= 0 or self.text_color[3] <= 0:
            return True
        return False


# ----------------- The Rectangular Text Button -----------------
# (extends RectTextObject)
# A general class for text buttons that are rectangular
class RectTextButton(RectTextObject):
    def __init__(self, color, rect, border, radius, action, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius, text, text_color, text_size)
        self.action = action

    def draw(self, surface, selected):
        if selected:
            pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], 255),
                             (self.x, self.y, self.width, self.height), self.border, self.radius)
        else:
            pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], 220),
                             (self.x, self.y, self.width, self.height), self.border, self.radius)

        if self.text != '':
            self.text_surf = self.font.render(self.text, True, self.text_color)
            surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                          self.y + (self.height / 2 - self.text_surf.get_height() / 2)))

    def is_selecting(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and \
                self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def get_action(self):
        return self.action


# ----------------- The Image Button -----------------
# (extends RectTextButton)
# A general class for Image Button Objects
class ImageButton(RectTextButton):
    # e.g. sell button. Buttons with images
    def __init__(self, color, rect, border, radius, action, image_file, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius, action, text, text_color, text_size)
        self.image = pygame.image.load(image_file).convert_alpha()

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))

        self.text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                      self.y + (self.height / 2 - self.text_surf.get_height() / 2)))

        if selected:
            new_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            new_surface.set_alpha(40)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y))

    def is_selecting(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and \
                self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def get_action(self):
        return self.action


# ----------------- The Scroll Bar -----------------
# (extends ImageButton)
# A scroll bar that scrolls the items up and down
class ScrollBar(ImageButton):
    def __init__(self, color, rect, border, radius, image_file):
        super().__init__(color, rect, border, radius, "", image_file, text="", text_color=(0, 0, 0), text_size=0)

    def draw(self, surface, selected):
        super().draw(surface, selected)

    def move(self, mouse_y_offset):
        self.y += mouse_y_offset


# ----------------- Item Popup Class -----------------
# The text label that pops up when you hover your cursor over an item.
# It provides a brief description about what the item does in the real world
class ItemPopup(ImageRectTextObject):
    # self, color, rect, border, radius, image_file, text='', text_color=(0, 0, 0), text_size=10
    def __init__(self, color, rect, border, radius, machine_image, popup_message="Lorem Ipsum"):
        super().__init__(color, rect, border, radius, machine_image, text=popup_message, text_color=(250, 250, 250),
                         text_size=15)

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))

        # ----------------- Code used for wrapping text and formatting -----------------

        popup_width = 390
        popup_height = 100

        # Calculate each line
        max_char_per_line = 2 * (popup_width - 30) // self.text_size
        word_list = self.text.split()
        lines = []
        current_line = ""

        # Place each formatted line into an array that will be processed
        for i in range(len(word_list)):

            if len(current_line) + 1 + len(word_list[i]) > max_char_per_line:
                lines.append(current_line)
                current_line = ""  # NOTE: CHECK FOR COPYING

            current_line += word_list[i]
            current_line += " "

            if i == len(word_list) - 1:
                lines.append(current_line)
                break

        # Place each line of text
        for i in range(len(lines)):
            self.text_surf = self.font.render(lines[i], True, self.text_color)
            surface.blit(self.text_surf, (self.x + 15, self.y + 15 + i * (popup_height - 30) // len(lines)))


