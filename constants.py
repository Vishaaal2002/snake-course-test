"""
constants.py - Configuration and constants for CyberSnake: Neon Blitz
"""

# Window & Grid Dimensions
GRID_SIZE = 24             # 24x24 grid cells
CELL_SIZE = 25             # 25 pixels per cell
BOARD_WIDTH = GRID_SIZE * CELL_SIZE   # 600 px
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE  # 600 px
HEADER_HEIGHT = 80         # Top HUD bar height
TOTAL_WIDTH = BOARD_WIDTH
TOTAL_HEIGHT = BOARD_HEIGHT + HEADER_HEIGHT

# High Score Storage File
HIGHSCORE_FILE = "highscore.json"

# Theme Colors (Modern Dark Neon / Cyberpunk Palette)
COLOR_BG_MAIN = "#0b0f19"         # Deep night blue/black
COLOR_BG_HEADER = "#111827"       # HUD background
COLOR_BG_BOARD = "#0d1322"        # Game board background
COLOR_GRID_LINE = "#172033"       # Subtle grid line color

# Snake Colors
COLOR_SNAKE_HEAD = "#38bdf8"      # Bright neon cyan
COLOR_SNAKE_EYE = "#ffffff"       # White eye
COLOR_SNAKE_PUPIL = "#0f172a"     # Dark pupil
COLOR_SNAKE_BODY_START = "#06b6d4"# Cyan gradient start
COLOR_SNAKE_BODY_END = "#0284c7"  # Deep cyan/blue gradient end

# Food & Power-up Colors
COLOR_FOOD_APPLE = "#f43f5e"      # Neon red
COLOR_FOOD_GOLDEN = "#facc15"     # Radiant gold
COLOR_POWERUP_SPEED = "#a855f7"   # Purple bolt
COLOR_POWERUP_SLOW = "#38bdf8"    # Ice blue
COLOR_POWERUP_CUT = "#ec4899"     # Neon pink scissor/shrink

# Text & UI Colors
COLOR_TEXT_PRIMARY = "#f8fafc"    # Crisp white
COLOR_TEXT_SECONDARY = "#94a3b8"  # Slate grey
COLOR_TEXT_MUTED = "#94a3b8"      # Muted slate grey
COLOR_TEXT_ACCENT = "#38bdf8"     # Neon cyan accent
COLOR_TEXT_GOLD = "#fbbf24"       # Gold trophy color
COLOR_BUTTON_BG = "#1e293b"       # Button background
COLOR_BUTTON_HOVER = "#334155"    # Button hover
COLOR_ACCENT_BORDER = "#1e293b"

# Difficulty Configurations
DIFFICULTIES = {
    "Easy": {
        "speed_ms": 110,
        "wrap_walls": True,
        "name": "Casual",
        "description": "Wrap around walls • Relaxed speed"
    },
    "Normal": {
        "speed_ms": 80,
        "wrap_walls": False,
        "name": "Classic",
        "description": "Solid walls • Standard arcade pace"
    },
    "Hard": {
        "speed_ms": 50,
        "wrap_walls": False,
        "name": "Insane",
        "description": "Solid walls • Super high speed"
    }
}

# Food Point Values & Durations
POINTS_APPLE = 10
POINTS_GOLDEN = 35
POINTS_BONUS_COMBO = 5

# Power-up Types
TYPE_APPLE = "apple"
TYPE_GOLDEN = "golden"
TYPE_SPEED = "speed"
TYPE_SLOW = "slow"
TYPE_CUT = "cut"

POWERUP_DURATION_TICKS = 60  # Approx 5-7 seconds depending on game speed
