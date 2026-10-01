APP_TITLE = "Simulator Taman UI"
SAVE_FILE = "savegame.json"
SAVE_VERSION = 1

GRID_ROWS = 3
GRID_COLS = 3

CELL_SIZE = 140
CELL_GAP = 16
CANVAS_MARGIN = 36

CANVAS_WIDTH = (
    CANVAS_MARGIN * 2
    + GRID_COLS * CELL_SIZE
    + (GRID_COLS - 1) * CELL_GAP
)

CANVAS_HEIGHT = (
    CANVAS_MARGIN * 2
    + GRID_ROWS * CELL_SIZE
    + (GRID_ROWS - 1) * CELL_GAP
)

MAX_ENERGY = 8

BG_MAIN = "#f5efe4"
PANEL_BG = "#fffaf1"
ACCENT = "#8b5e34"
ACCENT_SOFT = "#d8b486"
TEXT_DARK = "#4c3723"
TEXT_LIGHT = "#7a6046"
HIGHLIGHT = "#f2b86b"
SUCCESS = "#6ea96e"
WARNING = "#cc6a4c"

SOIL_OUTER = "#e8bf84"
SOIL_INNER = "#c98f52"
SOIL_LINE = "#b67c45"
GRID_BORDER = "#b78651"
GRID_SHADOW = "#d7b184"
SELECTED_BORDER = "#f2a23a"

PLANT_TYPES = {
    "tomat": {
        "name": "Tomat",
        "grow_days": 4,
        "seed_price": 8,
        "harvest_value": 24,
        "max_health": 100,
        "leaf_color": "#6e9f4a",
        "fruit_color": "#ef7a3a",
    },
    "wortel": {
        "name": "Wortel",
        "grow_days": 3,
        "seed_price": 6,
        "harvest_value": 18,
        "max_health": 100,
        "leaf_color": "#6fa04a",
        "fruit_color": "#f08b33",
    },
    "stroberi": {
        "name": "Stroberi",
        "grow_days": 5,
        "seed_price": 10,
        "harvest_value": 30,
        "max_health": 100,
        "leaf_color": "#609240",
        "fruit_color": "#d63f4a",
    },
    "bunga_matahari": {
        "name": "Bunga Matahari",
        "grow_days": 6,
        "seed_price": 12,
        "harvest_value": 38,
        "max_health": 100,
        "leaf_color": "#6c9b47",
        "fruit_color": "#f2c84a",
    },
}

STARTING_SEEDS = {
    "tomat": 2,
    "wortel": 2,
    "stroberi": 1,
    "bunga_matahari": 1,
}