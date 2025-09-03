"""
Spawn Manager module for handling enemy spawning with advanced progression.
Manages spawn rates, burst spawning, and dynamic spawn patterns.
"""

import random
import math


class SpawnManager:
    """Manages enemy spawning with advanced progression and patterns"""
    
    def __init__(self, config):
        """
        Initialize spawn manager with configuration.
        
        Args:
            config: Game configuration object
        """
        self.config = config
        self.current_spawn_rate = config.ENEMY_BASE_SPAWN_RATE
        self.current_pattern_index = 0
        self.burst_timer = 0
        self.pattern_timer = 0
        self.last_burst_score = 0
        
    def update_spawn_rate(self, difficulty_level):
        """
        Update spawn rate based on difficulty level.
        
        Args:
            difficulty_level: Current difficulty level
        """
        try:
            if not self.config.SPAWN_RATE_PROGRESSION_ENABLED:
                return
                
            # Calculate new spawn rate (lower = faster spawning)
            spawn_rate_decrease = (difficulty_level - 1) * self.config.SPAWN_RATE_SCALE_FACTOR
            new_spawn_rate = self.config.ENEMY_BASE_SPAWN_RATE - spawn_rate_decrease
            
            # Ensure spawn rate doesn't go below minimum
            self.current_spawn_rate = max(self.config.MIN_SPAWN_RATE, new_spawn_rate)
            
        except Exception as e:
            print(f"⚠️ Warning: Error updating spawn rate: {e}")
    
    def should_spawn_enemy(self, enemy_timer):
        """
        Check if an enemy should be spawned based on current spawn rate.
        
        Args:
            enemy_timer: Current enemy spawn timer
            
        Returns:
            bool: True if enemy should spawn
        """
        return enemy_timer >= self.current_spawn_rate
    
    def should_spawn_burst(self, score):
        """
        Check if a burst spawn should occur.
        
        Args:
            score: Current game score
            
        Returns:
            bool: True if burst spawn should occur
        """
        if not self.config.SPAWN_BURST_ENABLED:
            return False
            
        # Check if enough time has passed since last burst
        if score - self.last_burst_score >= self.config.BURST_SPAWN_INTERVAL:
            self.last_burst_score = score
            return True
            
        return False
    
    def get_spawn_positions(self, count=1, pattern_type=None):
        """
        Get spawn positions based on current pattern.
        
        Args:
            count: Number of positions to generate
            pattern_type: Specific pattern to use (None for current)
            
        Returns:
            list: List of (x, y) spawn positions
        """
        try:
            if pattern_type is None:
                pattern_type = self.config.SPAWN_PATTERNS[self.current_pattern_index]
            
            positions = []
            
            if pattern_type == "random":
                positions = self._get_random_positions(count)
            elif pattern_type == "wave":
                positions = self._get_wave_positions(count)
            elif pattern_type == "clustered":
                positions = self._get_clustered_positions(count)
            elif pattern_type == "alternating":
                positions = self._get_alternating_positions(count)
            else:
                # Fallback to random
                positions = self._get_random_positions(count)
                
            return positions
            
        except Exception as e:
            print(f"⚠️ Warning: Error generating spawn positions: {e}")
            # Fallback to random positions
            return self._get_random_positions(count)
    
    def _get_random_positions(self, count):
        """Generate random spawn positions"""
        positions = []
        for _ in range(count):
            x = random.randint(0, self.config.WIDTH - self.config.ENEMY_WIDTH)
            y = -self.config.ENEMY_HEIGHT
            positions.append((x, y))
        return positions
    
    def _get_wave_positions(self, count):
        """Generate wave-like spawn positions"""
        positions = []
        if count == 1:
            return self._get_random_positions(1)
            
        # Create a wave pattern across the screen
        for i in range(count):
            # Use sine wave for x position
            wave_progress = i / (count - 1) if count > 1 else 0.5
            wave_x = int(self.config.WIDTH * 0.1 + 
                        (self.config.WIDTH * 0.8) * wave_progress)
            
            # Add some randomness to the wave
            random_offset = random.randint(-20, 20)
            wave_x = max(0, min(self.config.WIDTH - self.config.ENEMY_WIDTH, 
                               wave_x + random_offset))
            
            y = -self.config.ENEMY_HEIGHT
            positions.append((wave_x, y))
            
        return positions
    
    def _get_clustered_positions(self, count):
        """Generate clustered spawn positions"""
        positions = []
        if count == 1:
            return self._get_random_positions(1)
            
        # Choose a cluster center
        cluster_center = random.randint(self.config.ENEMY_WIDTH, 
                                      self.config.WIDTH - self.config.ENEMY_WIDTH)
        
        for i in range(count):
            # Spread enemies around the cluster center
            spread = 30  # Maximum spread from center
            x_offset = random.randint(-spread, spread)
            x = max(0, min(self.config.WIDTH - self.config.ENEMY_WIDTH, 
                          cluster_center + x_offset))
            
            y = -self.config.ENEMY_HEIGHT
            positions.append((x, y))
            
        return positions
    
    def _get_alternating_positions(self, count):
        """Generate alternating side spawn positions"""
        positions = []
        if count == 1:
            return self._get_random_positions(1)
            
        for i in range(count):
            if i % 2 == 0:
                # Left side
                x = random.randint(0, self.config.WIDTH // 3)
            else:
                # Right side
                x = random.randint(2 * self.config.WIDTH // 3, 
                                 self.config.WIDTH - self.config.ENEMY_WIDTH)
            
            y = -self.config.ENEMY_HEIGHT
            positions.append((x, y))
            
        return positions
    
    def update_pattern(self, score):
        """
        Update spawn pattern based on score.
        
        Args:
            score: Current game score
        """
        try:
            if not self.config.DYNAMIC_SPAWN_PATTERNS:
                return
                
            # Change pattern every PATTERN_CHANGE_INTERVAL points
            if score - self.pattern_timer >= self.config.PATTERN_CHANGE_INTERVAL:
                self.current_pattern_index = (self.current_pattern_index + 1) % len(self.config.SPAWN_PATTERNS)
                self.pattern_timer = score
                print(f"🔄 Spawn pattern changed to: {self.config.SPAWN_PATTERNS[self.current_pattern_index]}")
                
        except Exception as e:
            print(f"⚠️ Warning: Error updating spawn pattern: {e}")
    
    def get_current_pattern_name(self):
        """Get the name of the current spawn pattern"""
        try:
            return self.config.SPAWN_PATTERNS[self.current_pattern_index]
        except:
            return "random"
    
    def get_spawn_rate_display(self):
        """Get spawn rate for display purposes"""
        try:
            # Convert frames to spawns per second for display
            spawns_per_second = self.config.FPS / self.current_spawn_rate
            return f"{spawns_per_second:.1f}/s"
        except:
            return "N/A"
