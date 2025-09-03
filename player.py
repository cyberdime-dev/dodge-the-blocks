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
        try:
            self.config = config
            self.rect = pygame.Rect(x, y, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
            self._speed = config.PLAYER_SPEED
            self.invincibility_timer = 0  # Timer for invincibility after losing a life
        except Exception as e:
            raise RuntimeError(f"Failed to initialize player: {e}")
        
    @property
    def speed(self):
        """Get player speed"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        """Set player speed with validation"""
        try:
            if value >= 0:
                self._speed = value
            else:
                print(f"⚠️ Warning: Attempted to set negative player speed: {value}")
        except (TypeError, ValueError) as e:
            print(f"⚠️ Warning: Invalid player speed value: {value}, error: {e}")
    
    def move(self, keys, screen_width):
        """
        Move player based on key input.
        
        Args:
            keys: Pygame key state
            screen_width: Width of the game screen
        """
        try:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self._speed
            if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += self._speed
        except Exception as e:
            print(f"⚠️ Warning: Player movement error: {e}")
    
    def draw(self, screen):
        """
        Draw player on screen.

        Args:
            screen: Pygame surface to draw on
        """
        try:
            # Draw invincible effect if active, otherwise normal player
            if self.is_invincible():
                self.draw_invincible_effect(screen)
            else:
                pygame.draw.rect(screen, self.config.BLUE, self.rect)
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw player: {e}")
    
    def reset_position(self, screen_width, screen_height):
        """
        Reset player to starting position.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        try:
            self.rect.x = screen_width // 2 - self.config.PLAYER_WIDTH // 2
            self.rect.y = screen_height - self.config.PLAYER_HEIGHT - self.config.PLAYER_START_Y_OFFSET
        except Exception as e:
            print(f"⚠️ Warning: Failed to reset player position: {e}")
    
    def get_position(self):
        """Get current player position"""
        try:
            return (self.rect.x, self.rect.y)
        except Exception as e:
            print(f"⚠️ Warning: Failed to get player position: {e}")
            return (0, 0)
    
    def set_position(self, x, y):
        """
        Set player position with bounds checking.

        Args:
            x: New x position
            y: New y position
        """
        try:
            if 0 <= x <= self.config.WIDTH - self.config.PLAYER_WIDTH:
                self.rect.x = x
            if 0 <= y <= self.config.HEIGHT - self.config.PLAYER_HEIGHT:
                self.rect.y = y
        except Exception as e:
            print(f"⚠️ Warning: Failed to set player position: {e}")

    def is_invincible(self):
        """Check if player is currently invincible"""
        return self.invincibility_timer > 0

    def make_invincible(self):
        """Make player invincible for a set period"""
        self.invincibility_timer = self.config.PLAYER_INVINCIBILITY_TIME

    def update_invincibility(self):
        """Update invincibility timer (call this every frame)"""
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

    def draw_invincible_effect(self, screen):
        """Draw visual effect when player is invincible"""
        if self.is_invincible():
            # Create a flashing effect by drawing a different color
            alpha = (self.invincibility_timer % 20) // 10  # Flash every 10 frames
            if alpha == 0:
                # Draw with a different color to show invincibility
                pygame.draw.rect(screen, (0, 255, 255), self.rect)  # Cyan color
