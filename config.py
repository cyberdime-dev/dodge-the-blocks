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
        
        # Enemy settings
        self.ENEMY_WIDTH = 50
        self.ENEMY_HEIGHT = 50
        self.ENEMY_BASE_SPEED = 5
        self.ENEMY_SPAWN_RATE = 30
        
        # Difficulty scaling settings
        self.DIFFICULTY_SCALING_ENABLED = True
        self.SPEED_SCALE_FACTOR = 0.1  # Speed increase per difficulty level
        self.SPAWN_RATE_SCALE_FACTOR = 0.05  # Spawn rate increase per difficulty level
        self.DIFFICULTY_INCREASE_INTERVAL = 1000  # Score points between difficulty increases
        self.MAX_DIFFICULTY_LEVEL = 20  # Maximum difficulty level cap
        self.INITIAL_DIFFICULTY_LEVEL = 1
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        
        # UI settings
        self.SCORE_POSITION = (10, 10)
        self.DIFFICULTY_POSITION = (10, 40)  # Position for difficulty display
        self.GAME_OVER_Y_OFFSET = 0.5  # Center of screen
