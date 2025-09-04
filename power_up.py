"""
Power-up module containing the PowerUp class.
Handles power-up spawning, collection, and effects.
"""

import pygame
import random


class PowerUp:
    """Power-up that provides temporary benefits when collected"""

    def __init__(self, config, x=None, y=None, power_type=None):
        """
        Initialize power-up with configuration and position.

        Args:
            config: Game configuration object
            x: X position (random if None)
            y: Y position (top if None)
            power_type: Specific power-up type (random if None)
        """
        try:
            self.config = config

            # Set position
            if x is None:
                x = random.randint(self.config.POWER_UP_SIZE,
                                   self.config.WIDTH - self.config.POWER_UP_SIZE)
            if y is None:
                y = -self.config.POWER_UP_SIZE

            self.rect = pygame.Rect(x, y, self.config.POWER_UP_SIZE, self.config.POWER_UP_SIZE)

            # Set power-up type
            if power_type is None:
                power_type = random.choice(list(self.config.POWER_UP_TYPES.keys()))
            self.power_type = power_type

            # Get properties for this power-up type
            self.properties = self.config.POWER_UP_TYPES.get(self.power_type, {})
            self.color = self.properties.get("color", (255, 255, 255))

        except Exception as e:
            raise RuntimeError(f"Failed to initialize power-up: {e}")

    def move(self):
        """Move power-up downward (slower than enemies)"""
        try:
            # Move slower than enemies so they're collectible
            self.rect.y += 2
        except Exception as e:
            print(f"\u26a0\ufe0f Warning: Power-up movement error: {e}")

    def draw(self, screen):
        """
        Draw power-up on screen.

        Args:
            screen: Pygame surface to draw on
        """
        try:
            # Draw the power-up square
            pygame.draw.rect(screen, self.color, self.rect)

            # Add a border to make it more visible
            border_color = (255, 255, 255)  # White border
            pygame.draw.rect(screen, border_color, self.rect, 2)

            # Add a small inner highlight
            inner_rect = pygame.Rect(
                self.rect.x + 3, self.rect.y + 3,
                self.rect.width - 6, self.rect.height - 6
            )
            highlight_color = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.rect(screen, highlight_color, inner_rect)

        except Exception as e:
            print(f"\u26a0\ufe0f Warning: Failed to draw power-up: {e}")

    def is_off_screen(self):
        """Check if power-up has moved off screen"""
        try:
            return self.rect.top > self.config.HEIGHT
        except Exception as e:
            print(f"\u26a0\ufe0f Warning: Error checking if power-up is off screen: {e}")
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
            print(f"\u26a0\ufe0f Warning: Error checking power-up collision: {e}")
            return False

    def get_effect_description(self):
        """Get a description of what this power-up does"""
        try:
            descriptions = {
                "speed_boost": "Speed Boost",
                "slow_motion": "Slow Motion",
                "extra_life": "Extra Life",
                "shield": "Shield"
            }
            return descriptions.get(self.power_type, self.power_type)
        except:
            return self.power_type

    def get_position(self):
        """Get current power-up position"""
        try:
            return (self.rect.x, self.rect.y)
        except Exception as e:
            print(f"\u26a0\ufe0f Warning: Failed to get power-up position: {e}")
            return (0, 0)


class ActivePowerUp:
    """Represents an active power-up effect on the player"""

    def __init__(self, power_type, duration):
        """
        Initialize active power-up.

        Args:
            power_type: Type of power-up
            duration: Duration in frames
        """
        self.power_type = power_type
        self.duration = duration
        self.remaining_time = duration

    def update(self):
        """Update the power-up timer"""
        if self.remaining_time > 0:
            self.remaining_time -= 1

    def is_expired(self):
        """Check if power-up has expired"""
        return self.remaining_time <= 0

    def get_remaining_time_display(self):
        """Get remaining time in seconds for display"""
        try:
            seconds = self.remaining_time // 60  # Assuming 60 FPS
            return f"{seconds}s"
        except:
            return "0s"
