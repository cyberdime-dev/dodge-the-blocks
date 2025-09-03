"""
Enemy module containing the Enemy class.
Handles enemy movement, drawing, and collision detection.
"""

import pygame


class Enemy:
    """Enemy that falls from the top of the screen"""
    
    def __init__(self, config, x, y):
        """
        Initialize enemy with configuration and position.
        
        Args:
            config: Game configuration object
            x: Initial x position
            y: Initial y position
        """
        self.config = config
        self.rect = pygame.Rect(x, y, config.ENEMY_WIDTH, config.ENEMY_HEIGHT)
        self._speed = config.ENEMY_SPEED
    
    @property
    def speed(self):
        """Get enemy speed"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        """Set enemy speed with validation"""
        if value >= 0:
            self._speed = value
    
    def move(self):
        """Move enemy downward"""
        self.rect.y += self._speed
    
    def draw(self, screen):
        """
        Draw enemy on screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.config.RED, self.rect)
    
    def is_off_screen(self, screen_height):
        """
        Check if enemy has moved off screen.
        
        Args:
            screen_height: Height of the game screen
            
        Returns:
            bool: True if enemy is off screen, False otherwise
        """
        return self.rect.top > screen_height
    
    def collides_with(self, player):
        """
        Check collision with player.
        
        Args:
            player: Player object to check collision with
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        return self.rect.colliderect(player.rect)
    
    def get_position(self):
        """Get current enemy position"""
        return (self.rect.x, self.rect.y)
