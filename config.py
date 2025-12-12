# config.py - upgraded settings

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 200, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 215, 0)
NEON = (255, 0, 200)

# Game base
INITIAL_LIVES = 3
GRAVITY = 0.45

# Spawn / difficulty
FRUIT_SPAWN_RATE = 60  # frames (will be adjusted by difficulty)
BOMB_PROBABILITY = 0.12
SPECIAL_PROBABILITY = 0.06   # golden / freeze fruits

# Visuals
FRUIT_SIZE = 70
CAM_PREVIEW_SIZE = (240, 180)  # webcam preview width, height
CAM_PREVIEW_POS = (SCREEN_WIDTH - CAM_PREVIEW_SIZE[0] - 20, 10)

# Slicing & combo
SLICE_SPEED_THRESHOLD = 9.0   # camera-pixel movement per frame to count a slice
COMBO_WINDOW_MS = 300         # ms window to chain combos
COMBO_BONUS = 20
COMBO_TEXT_DURATION_MS = 800

# Particle settings
PARTICLE_COUNT = 12
PARTICLE_LIFETIME = 40

# Difficulty presets (spawn_rate, gravity, bomb_prob)
DIFFICULTY = {
    "Easy": {"spawn_rate": 80, "gravity": 0.38, "bomb_prob": 0.08},
    "Normal": {"spawn_rate": 60, "gravity": 0.45, "bomb_prob": 0.12},
    "Hard": {"spawn_rate": 42, "gravity": 0.55, "bomb_prob": 0.18}
}

# File asset hints (place PNGs and sounds in assets/ if you want)
ASSETS_DIR = "assets"
FRUIT_IMAGES = {
    "apple": "apple.png",
    "orange": "orange.png",
    "banana": "banana.png",
    "watermelon": "watermelon.png",
    "grapes": "grapes.png",
    "strawberry": "strawberry.png",
    "kiwi": "kiwi.png",
    # special
    "golden": "golden.png",
    "freeze": "freeze.png",
    "bomb": "bomb.png"
}

SOUNDS = {
    "slice": "slice.wav",
    "bomb": "bomb.wav",
    "music": "music.mp3"
}
