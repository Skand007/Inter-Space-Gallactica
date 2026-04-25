import os

# Window
WIDTH, HEIGHT = 900, 500
TITLE = "Inter-Space Gallactica - Retro Arcade Edition"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
DARK_GREY = (20, 20, 20)

# Gameplay
FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Fonts
TITLE_FONT_NAME = "couriernew"
UI_FONT_NAME = "couriernew"

# CRT overlay
CRT_LINE_COLOR = (0, 0, 0, 40)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

# ⭐ THIS WAS MISSING — ADD IT ⭐
SCORES_PATH = os.path.join(BASE_DIR, "scores.json")
