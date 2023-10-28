
from enum import Enum

# Screen Information
SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 800

CENTER_X = 600
CENTER_Y = 400

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Modes
MAIN_MENU    = 0
CODE_SCREEN  = 1
DRILL_SCREEN = 2
TIP_SCREEN   = 3

# Colors
NO_COLOR = (0, 0, 0, 0)

MENU_SCREEN_COLOR = (216, 222, 233)

LAYER_COLORS = [
    (36, 42, 54),   # NORD DARK 1
    (46, 52, 64),   # NORD DARK 2
    (59, 66, 82),   # NORD DARK 3
    (62, 71, 89),   # NORD DARK 4
    (67, 76, 94),   # NORD DARK 5
    (76, 86, 106),  # NORD DARK 6

    (150, 157, 171),
    (181, 186, 196),
    (197, 203, 214),
    (216, 222, 233),  # NORD LIGHT 1
    (229, 233, 240),  # NORD LIGHT 2
    (236, 239, 244),  # NORD LIGHT 3
    (94, 129, 172),      # NORD MID BLUE 1
    (129, 161, 193),     # NORD MID BLUE 2
]


# Information Layers
# Each are written to maximize dependency on each other,
# so if one value is changed, the others will be changed respectively

# Suffixes for numbers for scaling
NUMBER_SUFFIX = [" ", "K", "M", "B", "T", "Qa", "Qu", "Sx"]

# Item information indexed by item type
# Position in array corresponds to type of item
NUM_ITEMS = 9
ITEM_NAMES = []

ITEM_PRICES = []
ITEM_RATES = []

# The descriptions for the tower popups
ITEM_INFO = [

]


# This keeps a list of which towers the upgrade rates will affect
UPGRADE_ACTIONS = [

]

# A rate for upgrades
# These numbers multiply the rate of the tower
UPGRADE_RATES = [

]

UPGRADE_COSTS = [
]

# The descriptions for the upgrade popups
# Each array contains the descriptions for one type of upgrade
UPGRADE_INFO = [

]

# Sorts the upgrades in ascending order based on cost
UPGRADE_ORDER = []

for i_upgrade in range(len(UPGRADE_COSTS)):
    for j_upgrade in range(len(UPGRADE_COSTS[i_upgrade])):
        UPGRADE_ORDER.append([i_upgrade, j_upgrade])

UPGRADE_ORDER = sorted(UPGRADE_ORDER, key=lambda x: UPGRADE_COSTS[x[0]][x[1]])




# BLOCKS

BLOCK_SIZE = 50

BLOCK_NAMES = ["EMPTY", "DIRT", "STONE", "COAL", "ROCK", "IRON", "LAVA"]


class BlockMaterial(Enum):
    EMPTY = 0
    DIRT = 1
    STONE = 2
    COAL = 3
    ROCK = 4
    IRON = 5
    LAVA = 6


BIOME_SIZE = 30 #the amount of blocks before new stuff can begin spawning

DIRECTIONS = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0),}

BLOCK_IMAGES = []

CODEBLOCK_COLORS = ["BLUE", "GREEN"]

