"""
Power-up module for temporary player enhancements.
Contains power-up types, effects, and management.
"""

import pygame
import random


class PowerUp:
    """Represents a collectible power-up with temporary effects"""

    # Power-up types
    SPEED_BOOST = "speed_boost"
    EXTRA_LIFE = "extra_life"
    SLOW_ENEMIES = "slow_enemies"
    INVINCIBILITY = "invincibility"
    SCORE_MULTIPLIER = "score_multiplier"

    def __init__(self, config, x, y, power_type=None):
        """
        Initialize power-up with configuration and position.

        Args:
            config: Game configuration object
            x: Spawn x position
            y: Spawn y position
            power_type: Type of power-up (random if None)
        """
        try:
            self.config = config
            self.rect = pygame.Rect(x, y, 30, 30)  # Power-ups are 30x30

            # Choose random power-up type if not specified
            if power_type is None:
                self.power_type = random.choice([
                    self.SPEED_BOOST,
                    self.EXTRA_LIFE,
                    self.SLOW_ENEMIES,
                    self.INVINCIBILITY,
                    self.SCORE_MULTIPLIER
                ])
            else:
                self.power_type = power_type

            # Set color based on power-up type
            self.color = self._get_color_for_type()

            # Animation properties
            self.animation_timer = 0
            self.animation_offset = 0

        except Exception as e:
            raise RuntimeError(f"Failed to initialize power-up: {e}")

    def _get_color_for_type(self):
        """Get color based on power-up type"""
        color_map = {
            self.SPEED_BOOST: (0, 255, 0),        # Green
            self.EXTRA_LIFE: (255, 0, 255),       # Magenta
            self.SLOW_ENEMIES: (0, 255, 255),     # Cyan
            self.INVINCIBILITY: (255, 255, 0),    # Yellow
            self.SCORE_MULTIPLIER: (255, 165, 0)  # Orange
        }
        return color_map.get(self.power_type, (255, 255, 255))

    def update(self):
        """Update power-up animation"""
        try:
            self.animation_timer += 1
            # Simple floating animation
            self.animation_offset = int(5 * pygame.math.Vector2(0, 1).rotate(self.animation_timer * 2).y)
        except Exception as e:
            print(f"⚠️ Warning: Error updating power-up animation: {e}")

    def draw(self, screen):
        """
        Draw power-up on screen with animation.

        Args:
            screen: Pygame surface to draw on
        """
        try:
            # Draw main power-up
            draw_rect = self.rect.copy()
            draw_rect.y += self.animation_offset

            pygame.draw.rect(screen, self.color, draw_rect)

            # Draw border for better visibility
            pygame.draw.rect(screen, self.config.WHITE, draw_rect, 2)

            # Draw type indicator (small inner square)
            inner_rect = pygame.Rect(
                draw_rect.x + 8,
                draw_rect.y + 8,
                14, 14
            )
            pygame.draw.rect(screen, self._get_inner_color(), inner_rect)

        except Exception as e:
            print(f"⚠️ Warning: Failed to draw power-up: {e}")

    def _get_inner_color(self):
        """Get inner color for power-up type indicator"""
        inner_colors = {
            self.SPEED_BOOST: (255, 255, 255),      # White
            self.EXTRA_LIFE: (255, 255, 255),       # White
            self.SLOW_ENEMIES: (0, 0, 0),          # Black
            self.INVINCIBILITY: (0, 0, 0),         # Black
            self.SCORE_MULTIPLIER: (0, 0, 0)       # Black
        }
        return inner_colors.get(self.power_type, (255, 255, 255))

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
            print(f"⚠️ Warning: Error checking power-up collision: {e}")
            return False

    def get_effect_description(self):
        """Get description of power-up effect"""
        descriptions = {
            self.SPEED_BOOST: "Speed Boost",
            self.EXTRA_LIFE: "Extra Life",
            self.SLOW_ENEMIES: "Slow Enemies",
            self.INVINCIBILITY: "Invincibility",
            self.SCORE_MULTIPLIER: "Score Multiplier"
        }
        return descriptions.get(self.power_type, "Unknown Power-up")

    def get_effect_duration(self):
        """Get duration of power-up effect in frames"""
        durations = {
            self.SPEED_BOOST: 300,      # 5 seconds
            self.EXTRA_LIFE: 1,         # Instant effect
            self.SLOW_ENEMIES: 240,     # 4 seconds
            self.INVINCIBILITY: 180,    # 3 seconds
            self.SCORE_MULTIPLIER: 360  # 6 seconds
        }
        return durations.get(self.power_type, 180)
