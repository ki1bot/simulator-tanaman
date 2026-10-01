APP_TITLE = "Simulator Taman"
SAVE_FILE = "savegame.json"
SAVE_VERSION = 1

GRID_ROWS = 3
GRID_COLS = 3
CELL_SIZE = 120
CELL_GAP = 12
CANVAS_MARGIN = 60

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

BG_MAIN = "#f4efe5"
PANEL_BG = "#fffaf0"
PANEL_ALT = "#f8efdf"
TEXT_DARK = "#4a3828"
TEXT_MUTED = "#7a6653"
ACCENT = "#8f633f"
ACCENT_HOVER = "#765033"
SUCCESS = "#6f9f65"
SUCCESS_HOVER = "#5e8b56"
WARNING = "#c97854"
WARNING_HOVER = "#ad6546"
BUTTON_BG = "#ead9bd"
BUTTON_HOVER = "#dcc6a2"
SELECTED_BORDER = "#e29b3f"
SOIL_OUTER = "#e5b97b"
SOIL_INNER = "#c98c4e"
SOIL_LINE = "#ad713b"
GRID_BORDER = "#b47d45"
GRID_SHADOW = "#d4ac77"
WATER_BLUE = "#6bb8df"

PLANT_TYPES = {
    "tomat": {
        "name": "Tomat",
        "grow_days": 4,
        "seed_price": 8,
        "harvest_value": 24,
        "max_health": 100,
        "leaf_color": "#6e9f4a",
        "fruit_color": "#ef7438",
    },
    "wortel": {
        "name": "Wortel",
        "grow_days": 3,
        "seed_price": 6,
        "harvest_value": 18,
        "max_health": 100,
        "leaf_color": "#6b9a49",
        "fruit_color": "#ee8a35",
    },
    "stroberi": {
        "name": "Stroberi",
        "grow_days": 5,
        "seed_price": 10,
        "harvest_value": 30,
        "max_health": 100,
        "leaf_color": "#609044",
        "fruit_color": "#d8454f",
    },
    "bunga_matahari": {
        "name": "Bunga Matahari",
        "grow_days": 6,
        "seed_price": 12,
        "harvest_value": 38,
        "max_health": 100,
        "leaf_color": "#6d9b49",
        "fruit_color": "#f0c748",
    },
}

STARTING_SEEDS = {
    "tomat": 2,
    "wortel": 2,
    "stroberi": 1,
    "bunga_matahari": 1,
}