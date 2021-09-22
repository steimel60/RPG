from os import path

##Load Folders
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')
font_folder = path.join(game_folder, 'Fonts')

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
screenWidth = 1024   # 16 * 64 or 32 * 32 or 64 * 16
screenHeight = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Potter Pixels"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = screenWidth / TILESIZE
GRIDHEIGHT = screenHeight / TILESIZE


# Player Settings
WALK_SPEED = 2
RUN_SPEED = 4
skin_colors = [(245,185,158),(234,154,95),(127,67,41)]

#
