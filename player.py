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

            # Power-up state
            self.active_power_ups = {}  # Dict of power_up_type -> remaining_duration
            self.base_speed = config.PLAYER_SPEED  # Store original speed
            self.speed_boost_multiplier = 1.0  # Current speed multiplier
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

    def activate_power_up(self, power_up):
        """
        Activate a power-up effect on the player.

        Args:
            power_up: PowerUp object that was collected
        """
        try:
            power_type = power_up.power_type
            duration = power_up.get_effect_duration()

            # Add or extend power-up duration
            if power_type in self.active_power_ups:
                self.active_power_ups[power_type] = max(self.active_power_ups[power_type], duration)
            else:
                self.active_power_ups[power_type] = duration

            # Apply immediate effects
            self._apply_power_up_effect(power_type)

            print(f"⚡ Power-up activated: {power_up.get_effect_description()}")

        except Exception as e:
            print(f"⚠️ Warning: Failed to activate power-up: {e}")

    def _apply_power_up_effect(self, power_type):
        """Apply the effect of a specific power-up type"""
        try:
            if power_type == "speed_boost":
                self.speed_boost_multiplier = self.config.POWER_UP_SPEED_BOOST_MULTIPLIER
                self._speed = int(self.base_speed * self.speed_boost_multiplier)
            elif power_type == "slow_enemies":
                # This will be handled by the game class
                pass
            elif power_type == "invincibility":
                # This will be handled by the game class
                pass
            elif power_type == "score_multiplier":
                # This will be handled by the game class
                pass
        except Exception as e:
            print(f"⚠️ Warning: Failed to apply power-up effect: {e}")

    def update_power_ups(self):
        """Update all active power-ups (call this every frame)"""
        try:
            # Update durations and remove expired power-ups
            expired_power_ups = []
            for power_type, duration in self.active_power_ups.items():
                self.active_power_ups[power_type] = duration - 1
                if self.active_power_ups[power_type] <= 0:
                    expired_power_ups.append(power_type)

            # Remove expired power-ups
            for power_type in expired_power_ups:
                del self.active_power_ups[power_type]
                self._remove_power_up_effect(power_type)
                print(f"⏰ Power-up expired: {power_type.replace('_', ' ').title()}")

            # Update speed if no speed boost is active
            if "speed_boost" not in self.active_power_ups:
                self.speed_boost_multiplier = 1.0
                self._speed = self.base_speed

        except Exception as e:
            print(f"⚠️ Warning: Error updating power-ups: {e}")

    def _remove_power_up_effect(self, power_type):
        """Remove the effect of a specific power-up type"""
        try:
            if power_type == "speed_boost":
                self.speed_boost_multiplier = 1.0
                self._speed = self.base_speed
        except Exception as e:
            print(f"⚠️ Warning: Failed to remove power-up effect: {e}")

    def has_active_power_up(self, power_type):
        """
        Check if a specific power-up is currently active.

        Args:
            power_type: Type of power-up to check

        Returns:
            bool: True if power-up is active
        """
        return power_type in self.active_power_ups

    def get_active_power_ups(self):
        """Get list of currently active power-up types"""
        return list(self.active_power_ups.keys())

    def draw_invincible_effect(self, screen):
        """Draw visual effect when player is invincible"""
        if self.is_invincible():
            # Create a flashing effect by drawing a different color
            alpha = (self.invincibility_timer % 20) // 10  # Flash every 10 frames
            if alpha == 0:
                # Draw with a different color to show invincibility
                pygame.draw.rect(screen, (0, 255, 255), self.rect)  # Cyan color

    def activate_power_up(self, power_up, duration):
        """Activate a power-up effect on the player"""
        try:
            effect_type = power_up.properties.get("effect", "")

            if effect_type == "player_speed":
                # Speed boost - increase player speed
                self.speed = self.speed + 2  # Boost by 2 units
                # Schedule speed restoration
                # This would need to be handled by the game loop

            elif effect_type == "lives":
                # Extra life - this would be handled by the game class
                pass  # Game class handles life increases

            elif effect_type == "invincibility":
                # Temporary invincibility
                self.make_invincible()
                # Extend invincibility duration
                self.invincibility_timer = max(self.invincibility_timer, duration)

            print(f"⚡ Power-up activated: {power_up.get_effect_description()}")

        except Exception as e:
            print(f"⚠️ Warning: Failed to activate power-up: {e}")

    def restore_speed(self, original_speed):
        """Restore player speed to original value"""
        try:
            self.speed = original_speed
        except Exception as e:
            print(f"⚠️ Warning: Failed to restore player speed: {e}")
