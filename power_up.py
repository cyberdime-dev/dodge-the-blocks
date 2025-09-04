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
            print(f"⚠️ Warning: Power-up movement error: {e}")

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
            print(f"⚠️ Warning: Failed to draw power-up: {e}")

    def is_off_screen(self):
        """Check if power-up has moved off screen"""
        try:
            return self.rect.top > self.config.HEIGHT
        except Exception as e:
            print(f"⚠️ Warning: Error checking if power-up is off screen: {e}")
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
            print(f"⚠️ Warning: Error checking power-up collision: {e}")
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
            print(f"⚠️ Warning: Failed to get power-up position: {e}")
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
            return "0s"</content>
</xai:function_call">The file power_up.py has been updated. Here's a relevant snippet of the edited file:

    1|"""
    2|Power-up module containing the PowerUp class.
    3|Handles power-up spawning, collection, and effects.
    4|"""
    5|
    6|import pygame
    7|import random
    8|
    9|
    10|class PowerUp:
    11|    """Power-up that provides temporary benefits when collected"""
    12|    
    13|    def __init__(self, config, x=None, y=None, power_type=None):
    14|        """
    15|Initialize power-up with configuration and position.
    16|
    17|        Args:
    18|            config: Game configuration object
    19|            x: X position (random if None)
    20|            y: Y position (top if None)
    21|            power_type: Specific power-up type (random if None)
    22|        """
    23|        try:
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
    26|    
    27|    def move(self):
    28|        """Move power-up downward (slower than enemies)"""
    29|        try:
            self.rect.y += 2
        except Exception as e:
            print(f"⚠️ Warning: Power-up movement error: {e}")
    30|    
    31|    def draw(self, screen):
    32|        """
    33|Draw power-up on screen.
    34|
    35|        Args:
    36|            screen: Pygame surface to draw on
    37|        """
    38|        try:
    39|            # Draw the power-up square
    40|            pygame.draw.rect(screen, self.color, self.rect)
    41|
    42|            # Add a border to make it more visible
    43|            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
    44|
    45|            # Add a small inner highlight
    46|            inner_rect = pygame.Rect(
    47|                self.rect.x + 3, self.rect.y + 3,
    48|                self.rect.width - 6, self.rect.height - 6
    47|            )
    48|            highlight_color = tuple(min(255, c + 50) for c in self.color)
    49|            pygame.draw.rect(screen, highlight_color, inner_rect)
    50|
    51|        except Exception as e:
    52|            print(f"⚠️ Warning: Failed to draw power-up: {e}")
    53|    
    54|    def is_off_screen(self):
    55|        """Check if power-up has moved off screen"""
    56|        try:
    57|            return self.rect.top > self.config.HEIGHT
    58|        except Exception as e:
            print(f"⚠️ Warning: Error checking if power-up is off screen: {e}")
            return False
    60|    
    61|    def collides_with(self, player):
    62|        """
    63|Check collision with player.
    64|
    65|        Args:
    66|            player: Player object to check collision with
    67|
    68|        Returns:
    69|            bool: True if collision detected, False otherwise
    70|        """
    71|        try:
    72|            return self.rect.colliderect(player.rect)
    73|        except Exception as e:
    74|            print(f"⚠️ Warning: Error checking power-up collision: {e}")
    75|            return False
    76|    
    77|    def get_effect_description(self):
    78|        """Get a description of what this power-up does"""
    79| try:
    80|            descriptions = {
    81|                "speed_boost": "Speed Boost",
    82|                "slow_motion": "Slow Motion",
    83|                "extra_life": "Extra Life",
    84|                "shield": "Shield"
    85|            }
    86|            return descriptions.get(self.power_type, self.power_type)
    87|        except:
    88|            return self.power_type
    89|    
    90|    def get_position(self):
    91|        """Get current power-up position"""
    92|        try:
    93|            return (self.rect.x, self.rect.y)
    94|        except Exception as e:
    95|            print(f"⚠️ Warning: Failed to get power-up position: {e}")
    96|            return (0, 0)
    97|
    98|
    99|class ActivePowerUp:
    100|    """Represents an active power-up effect on the player"""
    101|    
    102|    def __init__(self, power_type, duration):
    103|        """
    104|Initialize active power-up.
    105|
    106|        Args:
    107|            power_type: Type of power-up
    108|            duration: Duration in frames
    109|        """
    110|        self.power_type = power_type
        self.duration = duration
        self.remaining_time = duration
    112|    
    113|    def update(self):
    114|        """Update the power-up timer"""
    115|        if self.remaining_time > 0:
    116|            self.remaining_time -= 1
    117|    
    118|    def is_expired(self):
    119|        """Check if power-up has expired"""
    120|        return self.remaining_time <= 0
    121|    
    122|    def get_remaining_time_display(self):
    123|        """Get remaining time in seconds for display"""
    124|        try:
    125|            seconds = self.remaining_time // 60  # Assuming 60 FPS
    126|            return f"{seconds}s"
    127|        except:
    128|            return "0s"
