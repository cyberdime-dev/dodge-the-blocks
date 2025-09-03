"""
Enemy module containing the Enemy class.
Handles enemy movement, drawing, and collision detection.
"""

import pygame


class Enemy:
    """Enemy that falls from the top of the screen"""
    
    def __init__(self, config, x, y, speed=None):
        """
        Initialize enemy with configuration and position.
        
        Args:
            config: Game configuration object
            x: Initial x position
            y: Initial y position
            speed: Optional custom speed (uses config default if None)
        """
        try:
            self.config = config
            self.rect = pygame.Rect(x, y, config.ENEMY_WIDTH, config.ENEMY_HEIGHT)
            # Use provided speed or base speed from config
            self._speed = speed if speed is not None else config.ENEMY_BASE_SPEED
        except Exception as e:
            raise RuntimeError(f"Failed to initialize enemy: {e}")
    
    @property
    def speed(self):
        """Get enemy speed"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        """Set enemy speed with validation"""
        try:
            if value >= 0:
                self._speed = value
            else:
                print(f"⚠️ Warning: Attempted to set negative enemy speed: {value}")
        except (TypeError, ValueError) as e:
            print(f"⚠️ Warning: Invalid enemy speed value: {value}, error: {e}")
    
    def move(self):
        """Move enemy downward"""
        try:
            self.rect.y += self._speed
        except Exception as e:
            print(f"⚠️ Warning: Enemy movement error: {e}")
    
    def draw(self, screen):
        """
        Draw enemy on screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
            pygame.draw.rect(screen, self.config.RED, self.rect)
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw enemy: {e}")
    
    def is_off_screen(self, screen_height):
        """
        Check if enemy has moved off screen.
        
        Args:
            screen_height: Height of the game screen
            
        Returns:
            bool: True if enemy is off screen, False otherwise
        """
        try:
            return self.rect.top > screen_height
        except Exception as e:
            print(f"⚠️ Warning: Error checking if enemy is off screen: {e}")
            return False
    
    def collides_with(self, player):
        """
        Check collision with player.
        
        Args:
            player: Player object to check collision with
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        try:
            return self.rect.colliderect(player.rect)
        except Exception as e:
            print(f"⚠️ Warning: Error checking collision: {e}")
            return False
    
    def get_position(self):
        """Get current enemy position"""
        try:
            return (self.rect.x, self.rect.y)
        except Exception as e:
            print(f"⚠️ Warning: Failed to get enemy position: {e}")
            return (0, 0)
