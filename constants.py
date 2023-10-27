
# Screen Information
WIDTH = 1250
HEIGHT = 800

CENTER_X = 600
CENTER_Y = 400

SCREEN_SIZE = (WIDTH, HEIGHT)

# Modes
MAIN_MENU    = 0
CODE_SCREEN  = 1
DRILL_SCREEN = 2
TIP_SCREEN   = 3

# Colors
GOLD_COLOR = (255, 206, 46)
MONEY_COLOR = (101, 214, 131)
COUNT_COLOR = (76, 135, 237)
NO_COLOR = (0, 0, 0, 0)

# Main Layer component information
LAYER_LEFT_RECT = (0, 0, 300, HEIGHT)
LAYER_MIDDLE_RECT = (LAYER_LEFT_RECT[2], 0, 400, HEIGHT)
LAYER_RIGHT_RECT = (LAYER_MIDDLE_RECT[0] + LAYER_MIDDLE_RECT[2], 0, 400, HEIGHT)

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

BLOCK_NAMES = ["EMPTY", "DIRT", "STONE"]

DIRECTIONS = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0),}

BLOCK_IMAGES = []

