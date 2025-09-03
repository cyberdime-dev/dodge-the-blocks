"""
Player module containing the Player class.
Handles player movement, drawing, and state management.
"""

import pygame


class Player:
    """Player character that can move left and right"""
    
    def __init__(self, config, x, y):
        """
        Initialize player with configuration and position.
        
        Args:
            config: Game configuration object
            x: Initial x position
            y: Initial y position
        """
        self.config = config
        self.rect = pygame.Rect(x, y, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
        self._speed = config.PLAYER_SPEED
        
    @property
    def speed(self):
        """Get player speed"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        """Set player speed with validation"""
        if value >= 0:
            self._speed = value
    
    def move(self, keys, screen_width):
        """
        Move player based on key input.
        
        Args:
            keys: Pygame key state
            screen_width: Width of the game screen
        """
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self._speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self._speed
    
    def draw(self, screen):
        """
        Draw player on screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.config.BLUE, self.rect)
    
    def reset_position(self, screen_width, screen_height):
        """
        Reset player to starting position.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        self.rect.x = screen_width // 2 - self.config.PLAYER_WIDTH // 2
        self.rect.y = screen_height - self.config.PLAYER_HEIGHT - self.config.PLAYER_START_Y_OFFSET
    
    def get_position(self):
        """Get current player position"""
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x, y):
        """
        Set player position with bounds checking.
        
        Args:
            x: New x position
            y: New y position
        """
        if 0 <= x <= self.config.WIDTH - self.config.PLAYER_WIDTH:
            self.rect.x = x
        if 0 <= y <= self.config.HEIGHT - self.config.PLAYER_HEIGHT:
            self.rect.y = y
