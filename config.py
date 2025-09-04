"""
Game configuration and constants module.
Contains all game settings, dimensions, speeds, and colors.
"""


class Config:
    """Game configuration and constants"""
    
    def __init__(self):
        # Display settings
        self.WIDTH = 600
        self.HEIGHT = 800
        self.FPS = 60
        
        # Player settings
        self.PLAYER_WIDTH = 50
        self.PLAYER_HEIGHT = 50
        self.PLAYER_SPEED = 7
        self.PLAYER_START_Y_OFFSET = 20
        self.PLAYER_STARTING_LIVES = 3  # Number of lives player starts with
        self.PLAYER_INVINCIBILITY_TIME = 120  # Frames of invincibility after losing a life

        # Power-up settings
        self.POWER_UP_SPAWN_CHANCE = 0.02  # Chance per frame to spawn power-up
        self.POWER_UP_SPEED_BOOST_MULTIPLIER = 1.5  # How much faster player moves
        self.POWER_UP_SLOW_ENEMIES_FACTOR = 0.5  # How much slower enemies move
        self.POWER_UP_SCORE_MULTIPLIER = 2  # Score multiplier value
        
        # Enemy settings
        self.ENEMY_WIDTH = 50
        self.ENEMY_HEIGHT = 50
        self.ENEMY_BASE_SPEED = 5
        self.ENEMY_BASE_SPAWN_RATE = 30  # Frames between spawns (lower = faster)
        
        # Difficulty scaling settings
        self.DIFFICULTY_SCALING_ENABLED = True
        self.SPEED_SCALE_FACTOR = 0.05  # Speed increase per difficulty level (reduced for slower progression)
        self.SPAWN_RATE_SCALE_FACTOR = 0.05  # Spawn rate increase per difficulty level
        
        # Gradual difficulty progression (points required for each level)
        self.DIFFICULTY_PROGRESSION = {
            1: 0,      # Level 1 starts at 0 points
            2: 20,     # Level 2 at 20 points
            3: 40,     # Level 3 at 40 points
            4: 80,     # Level 4 at 80 points
            5: 160,    # Level 5 at 160 points
            6: 320,    # Level 6 at 320 points
            7: 640,    # Level 7 at 640 points
            8: 1280,   # Level 8 at 1280 points
            9: 2560,   # Level 9 at 2560 points
            10: 5120   # Level 10 at 5120 points
        }
        self.MAX_DIFFICULTY_LEVEL = 10  # Maximum difficulty level cap
        self.INITIAL_DIFFICULTY_LEVEL = 1
        
        # Advanced spawn rate progression
        self.SPAWN_RATE_PROGRESSION_ENABLED = True
        self.MIN_SPAWN_RATE = 8  # Fastest possible spawn rate (frames)
        self.SPAWN_BURST_ENABLED = True  # Enable burst spawning at higher levels
        self.BURST_SPAWN_COUNT = 3  # Number of enemies in a burst
        self.BURST_SPAWN_INTERVAL = 200  # Frames between burst spawns
        self.BURST_ACTIVATION_LEVEL = 5  # Level when burst spawning starts
        
        # Dynamic spawn patterns
        self.DYNAMIC_SPAWN_PATTERNS = True
        self.PATTERN_CHANGE_INTERVAL = 500  # Score points between pattern changes
        self.SPAWN_PATTERNS = [
            "random",      # Random positions
            "wave",        # Wave-like pattern
            "clustered",   # Clustered spawns
            "alternating"  # Alternating sides
        ]
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        
        # Power-up settings
        self.POWER_UP_SPAWN_CHANCE = 0.005  # Chance per frame to spawn power-up
        self.POWER_UP_DURATION = 600  # Frames (10 seconds at 60 FPS)
        self.POWER_UP_SIZE = 30  # Size of power-up squares
        self.POWER_UP_TYPES = {
            "speed_boost": {"color": (255, 255, 0), "effect": "player_speed"},  # Yellow - speed boost
            "slow_motion": {"color": (0, 255, 255), "effect": "enemy_speed"},   # Cyan - slow enemies
            "extra_life": {"color": (255, 0, 255), "effect": "lives"},          # Magenta - extra life
            "shield": {"color": (255, 165, 0), "effect": "invincibility"}       # Orange - temporary shield
        }

        # UI settings
        self.SCORE_POSITION = (10, 10)
        self.DIFFICULTY_POSITION = (10, 40)  # Position for difficulty display
        self.SPAWN_RATE_POSITION = (10, 100)  # Position for spawn rate display (moved down to avoid overlap)
        self.LIVES_POSITION = (10, 130)  # Position for lives display (moved down)
        self.POWER_UP_POSITION = (10, 160)  # Position for active power-up display (moved down)
        self.GAME_OVER_Y_OFFSET = 0.5  # Center of screen
