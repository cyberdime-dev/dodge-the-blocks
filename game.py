"""
Game module containing the main Game class.
Manages the game loop, state, and coordinates all game elements.
"""

import pygame
import random
import sys
import traceback

from config import Config
from player import Player
from enemy import Enemy
from spawn_manager import SpawnManager
from power_up import PowerUp, ActivePowerUp


class Game:
    """Main game controller managing game state and loop"""
    
    def __init__(self):
        """Initialize the game with configuration and game objects"""
        try:
            self.config = Config()
            
            # Initialize pygame display
            try:
                self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
                pygame.display.set_caption("Dodge the Blocks")
            except pygame.error as e:
                raise RuntimeError(f"Failed to create display: {e}")
            
            # Initialize pygame clock and font
            try:
                self.clock = pygame.time.Clock()
                self.font = pygame.font.SysFont(None, 36)
                if not self.font:
                    raise RuntimeError("Failed to create font")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize pygame components: {e}")
            
            # Game state
            self._score = 0
            self._game_over = False
            self._enemy_timer = 0
            self._lives = self.config.PLAYER_STARTING_LIVES

            # Difficulty scaling state
            self._difficulty_level = self.config.INITIAL_DIFFICULTY_LEVEL
            self._current_enemy_speed = self.config.ENEMY_BASE_SPEED
            
            # Initialize spawn manager
            try:
                self.spawn_manager = SpawnManager(self.config)
            except Exception as e:
                raise RuntimeError(f"Failed to create spawn manager: {e}")
            
            # Game objects
            try:
                self.player = Player(
                    self.config,
                    self.config.WIDTH // 2 - self.config.PLAYER_WIDTH // 2,
                    self.config.HEIGHT - self.config.PLAYER_HEIGHT - self.config.PLAYER_START_Y_OFFSET
                )
            except Exception as e:
                raise RuntimeError(f"Failed to create player: {e}")

            self.enemies = []
            self.power_ups = []  # List of active power-ups in the game world
            self.active_power_ups = []  # List of currently active power-up effects

            # Baseline speeds for restoring after power-up effects
            self._original_player_speed = self.player.speed
            self._original_enemy_speed = self._current_enemy_speed
            
        except Exception as e:
            print(f"❌ Failed to initialize game: {e}")
            raise
    
    @property
    def score(self):
        """Get current score"""
        return self._score
    
    @score.setter
    def score(self, value):
        """Set score with validation"""
        try:
            if value >= 0:
                self._score = value
                # Check if difficulty should increase
                self._check_difficulty_increase()
                # Update spawn pattern
                self.spawn_manager.update_pattern(self._score)
            else:
                print(f"⚠️ Warning: Attempted to set negative score: {value}")
        except (TypeError, ValueError) as e:
            print(f"⚠️ Warning: Invalid score value: {value}, error: {e}")
    
    @property
    def game_over(self):
        """Get game over state"""
        return self._game_over
    
    @game_over.setter
    def game_over(self, value):
        """Set game over state"""
        try:
            self._game_over = bool(value)
        except Exception as e:
            print(f"⚠️ Warning: Failed to set game over state: {e}")
    
    @property
    def enemy_timer(self):
        """Get enemy spawn timer"""
        return self._enemy_timer

    @enemy_timer.setter
    def enemy_timer(self, value):
        """Set enemy spawn timer"""
        try:
            if value >= 0:
                self._enemy_timer = value
            else:
                print(f"⚠️ Warning: Attempted to set negative timer: {value}")
        except (TypeError, ValueError) as e:
            print(f"⚠️ Warning: Invalid timer value: {value}, error: {e}")

    @property
    def lives(self):
        """Get current lives"""
        return self._lives

    @lives.setter
    def lives(self, value):
        """Set lives with validation"""
        try:
            if value >= 0:
                self._lives = value
                # Check if game should end when lives reach zero
                if self._lives == 0:
                    self.game_over = True
                    print("💔 Game Over! No lives remaining.")
            else:
                print(f"⚠️ Warning: Attempted to set negative lives: {value}")
        except (TypeError, ValueError) as e:
            print(f"⚠️ Warning: Invalid lives value: {value}, error: {e}")

    @property
    def difficulty_level(self):
        """Get current difficulty level"""
        return self._difficulty_level

    @property
    def current_enemy_speed(self):
        """Get current enemy speed"""
        return self._current_enemy_speed
    
    def _check_difficulty_increase(self):
        """Check if difficulty should increase based on score"""
        if not self.config.DIFFICULTY_SCALING_ENABLED:
            return
            
        try:
            # Find the highest level the player has reached based on score
            new_level = 1
            for level, required_score in self.config.DIFFICULTY_PROGRESSION.items():
                if self._score >= required_score:
                    new_level = level
                else:
                    break
            
            # Cap difficulty at maximum level
            new_level = min(new_level, self.config.MAX_DIFFICULTY_LEVEL)
            
            # If difficulty increased, update game parameters
            if new_level > self._difficulty_level:
                self._difficulty_level = new_level
                self._update_difficulty_parameters()
                print(f"🎯 Difficulty increased to level {self._difficulty_level}!")
                print(f"📊 Next level requires {self._get_next_level_requirement()} points")
                
        except Exception as e:
            print(f"⚠️ Warning: Error updating difficulty: {e}")
    
    def _get_next_level_requirement(self):
        """Get the score requirement for the next level"""
        try:
            next_level = self._difficulty_level + 1
            if next_level in self.config.DIFFICULTY_PROGRESSION:
                return self.config.DIFFICULTY_PROGRESSION[next_level]
            else:
                return "MAX LEVEL"
        except:
            return "N/A"
    
    def _update_difficulty_parameters(self):
        """Update game parameters based on current difficulty level"""
        try:
            # Calculate new enemy speed
            speed_increase = (self._difficulty_level - 1) * self.config.SPEED_SCALE_FACTOR
            self._current_enemy_speed = self.config.ENEMY_BASE_SPEED + speed_increase
            
            # Update spawn manager with new difficulty
            self.spawn_manager.update_spawn_rate(self._difficulty_level)
            
            # Update existing enemies to new speed
            for enemy in self.enemies:
                enemy.speed = self._current_enemy_speed
            
            # Keep baseline enemy speed in sync with current difficulty
            self._original_enemy_speed = self._current_enemy_speed
                
        except Exception as e:
            print(f"⚠️ Warning: Error updating difficulty parameters: {e}")
    
    def spawn_enemy(self, count=1, pattern_type=None):
        """
        Spawn enemies using spawn manager.
        
        Args:
            count: Number of enemies to spawn
            pattern_type: Specific spawn pattern to use
        """
        try:
            # Get spawn positions from spawn manager
            positions = self.spawn_manager.get_spawn_positions(count, pattern_type)
            
            # Create enemies at the positions
            for x, y in positions:
                enemy = Enemy(self.config, x, y, self._current_enemy_speed)
                self.enemies.append(enemy)
                
        except Exception as e:
            print(f"⚠️ Warning: Failed to spawn enemies: {e}")

    def spawn_burst(self):
        """Spawn a burst of enemies"""
        try:
            if self.spawn_manager.should_spawn_burst(self._score):
                print(f"💥 Burst spawning {self.config.BURST_SPAWN_COUNT} enemies!")
                self.spawn_enemy(self.config.BURST_SPAWN_COUNT, "clustered")

        except Exception as e:
            print(f"⚠️ Warning: Failed to spawn burst: {e}")

    def spawn_power_up(self):
        """Spawn a power-up with random chance"""
        try:
            if random.random() < self.config.POWER_UP_SPAWN_CHANCE:
                power_up = PowerUp(self.config)
                self.power_ups.append(power_up)
        except Exception as e:
            print(f"⚠️ Warning: Failed to spawn power-up: {e}")



    def update_power_ups(self):
        """Update power-ups and check for collection"""
        try:
            for power_up in self.power_ups[:]:
                try:
                    power_up.move()

                    # Check collision with player
                    if power_up.collides_with(self.player):
                        # Activate power-up effect
                        self._activate_power_up(power_up)
                        self.power_ups.remove(power_up)
                        continue

                    # Remove power-ups that are off screen
                    if power_up.is_off_screen():
                        self.power_ups.remove(power_up)

                except Exception as e:
                    print(f"⚠️ Warning: Error updating power-up: {e}")
                    # Remove problematic power-up
                    try:
                        self.power_ups.remove(power_up)
                    except:
                        pass

        except Exception as e:
            print(f"⚠️ Warning: Error in power-up update loop: {e}")

    def _activate_power_up(self, power_up):
        """Activate a power-up effect"""
        try:
            effect_type = power_up.properties.get("effect", "")
            duration = self.config.POWER_UP_DURATION

            if effect_type == "player_speed":
                # Speed boost for player
                self.player.speed = self.player.speed + 2
                # Create active power-up to track duration
                active_power_up = ActivePowerUp("speed_boost", duration)
                self.active_power_ups.append(active_power_up)
                print(f"⚡ Speed Boost activated! Player speed increased.")

            elif effect_type == "slow_motion":
                # Slow down enemies
                for enemy in self.enemies:
                    enemy.speed = max(1, enemy.speed - 2)  # Slow down but not stop
                # Create active power-up
                active_power_up = ActivePowerUp("slow_motion", duration)
                self.active_power_ups.append(active_power_up)
                print(f"🐢 Slow Motion activated! Enemies slowed down.")

            elif effect_type == "extra_life":
                # Give extra life
                self.lives += 1
                print(f"❤️ Extra Life! Lives increased to {self.lives}.")

            elif effect_type == "shield":
                # Temporary invincibility
                self.player.make_invincible()
                active_power_up = ActivePowerUp("shield", duration)
                self.active_power_ups.append(active_power_up)
                print(f"🛡️ Shield activated! Temporary invincibility.")

            else:
                print(f"⚠️ Unknown power-up effect: {effect_type}")

        except Exception as e:
            print(f"⚠️ Warning: Failed to activate power-up: {e}")

    def update_active_power_ups(self):
        """Update active power-up effects and handle expiration"""
        try:
            for active_power_up in self.active_power_ups[:]:
                active_power_up.update()

                if active_power_up.is_expired():
                    # Remove expired power-up effect
                    self._deactivate_power_up(active_power_up)
                    self.active_power_ups.remove(active_power_up)

        except Exception as e:
            print(f"⚠️ Warning: Error updating active power-ups: {e}")

    def _deactivate_power_up(self, active_power_up):
        """Deactivate a power-up effect"""
        try:
            if active_power_up.power_type == "speed_boost":
                # Restore original player speed
                self.player.restore_speed(self._original_player_speed)
                print(f"🏃 Speed Boost expired. Speed restored.")

            elif active_power_up.power_type == "slow_motion":
                # Restore original enemy speed
                for enemy in self.enemies:
                    enemy.speed = self._original_enemy_speed
                print(f"💨 Slow Motion expired. Enemy speed restored.")

            elif active_power_up.power_type == "shield":
                # Invincibility will naturally expire
                print(f"🛡️ Shield expired. Normal collision detection active.")

        except Exception as e:
            print(f"⚠️ Warning: Error deactivating power-up: {e}")

    def _apply_power_up_game_effect(self, power_type):
        """Apply game-wide effects of power-ups"""
        try:
            if power_type == "extra_life":
                self.lives += 1
                print(f"❤️ Extra life! Lives: {self.lives}")
            elif power_type == "slow_enemies":
                # Temporarily slow all enemies
                for enemy in self.enemies:
                    enemy.speed = int(enemy.speed * self.config.POWER_UP_SLOW_ENEMIES_FACTOR)
            elif power_type == "invincibility":
                # Make player invincible
                self.player.make_invincible()
        except Exception as e:
            print(f"⚠️ Warning: Failed to apply game power-up effect: {e}")

    def update_slow_enemies_effect(self):
        """Update slow enemies effect if active"""
        try:
            if self.player.has_active_power_up("slow_enemies"):
                # Keep enemies slowed
                for enemy in self.enemies:
                    target_speed = int(self._current_enemy_speed * self.config.POWER_UP_SLOW_ENEMIES_FACTOR)
                    if enemy.speed != target_speed:
                        enemy.speed = target_speed
            else:
                # Restore normal enemy speed
                for enemy in self.enemies:
                    if enemy.speed != self._current_enemy_speed:
                        enemy.speed = self._current_enemy_speed
        except Exception as e:
            print(f"⚠️ Warning: Error updating slow enemies effect: {e}")
    
    def update_enemies(self):
        """Update enemy positions and check collisions"""
        try:
            for enemy in self.enemies[:]:
                try:
                    enemy.move()

                    # Check collision with player (only if not invincible)
                    if enemy.collides_with(self.player) and not self.player.is_invincible():
                        # Lose a life and become invincible
                        self.lives -= 1
                        self.player.make_invincible()
                        print(f"💔 Life lost! {self.lives} lives remaining.")

                        # Remove the enemy that caused the collision
                        try:
                            self.enemies.remove(enemy)
                        except:
                            pass

                        # If no lives left, game over will be triggered by lives setter
                        if self.lives == 0:
                            return
                        continue

                    # Remove enemies that are off screen and award points
                    if enemy.is_off_screen(self.config.HEIGHT):
                        self.enemies.remove(enemy)
                        self.score += 1

                except Exception as e:
                    print(f"⚠️ Warning: Error updating enemy: {e}")
                    # Remove problematic enemy
                    try:
                        self.enemies.remove(enemy)
                    except:
                        pass

        except Exception as e:
            print(f"⚠️ Warning: Error in enemy update loop: {e}")
    
    def handle_input(self):
        """Handle keyboard input"""
        try:
            keys = pygame.key.get_pressed()
            
            if not self.game_over:
                try:
                    self.player.move(keys, self.config.WIDTH)
                except Exception as e:
                    print(f"⚠️ Warning: Player movement error: {e}")
            else:
                if keys[pygame.K_r]:
                    self.reset_game()
                elif keys[pygame.K_q]:
                    pygame.quit()
                    sys.exit()
                    
        except Exception as e:
            print(f"⚠️ Warning: Input handling error: {e}")

    def reset_game(self):
        """Reset game to initial state"""
        try:
            self.player.reset_position(self.config.WIDTH, self.config.HEIGHT)
            self.enemies.clear()
            self.power_ups.clear()  # Clear power-ups
            if hasattr(self, 'active_power_ups'):
                self.active_power_ups.clear()  # Clear active power-up effects
            self.score = 0
            self.game_over = False
            self.enemy_timer = 0
            self.lives = self.config.PLAYER_STARTING_LIVES  # Reset lives

            # Reset difficulty
            self._difficulty_level = self.config.INITIAL_DIFFICULTY_LEVEL
            self._current_enemy_speed = self.config.ENEMY_BASE_SPEED

            # Reset spawn manager
            self.spawn_manager = SpawnManager(self.config)

            # Restore original speeds
            if hasattr(self, '_original_player_speed'):
                self.player.restore_speed(self._original_player_speed)
            self._original_enemy_speed = self._current_enemy_speed

        except Exception as e:
            print(f"⚠️ Warning: Failed to reset game: {e}")
    
    def draw_score(self):
        """Draw score on screen"""
        try:
            score_text = self.font.render(f"Score: {self.score}", True, self.config.WHITE)
            self.screen.blit(score_text, self.config.SCORE_POSITION)
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw score: {e}")
    
    def draw_difficulty(self):
        """Draw difficulty level and progress on screen"""
        try:
            # Current level
            difficulty_text = self.font.render(f"Level: {self.difficulty_level}", True, self.config.WHITE)
            self.screen.blit(difficulty_text, self.config.DIFFICULTY_POSITION)
            
            # Progress to next level (smaller font)
            try:
                small_font = pygame.font.SysFont(None, 24)
                
                if self._difficulty_level < self.config.MAX_DIFFICULTY_LEVEL:
                    current_level_score = self.config.DIFFICULTY_PROGRESSION.get(self._difficulty_level, 0)
                    next_level_score = self.config.DIFFICULTY_PROGRESSION.get(self._difficulty_level + 1, 0)
                    
                    if next_level_score > current_level_score:
                        progress = self._score - current_level_score
                        total_needed = next_level_score - current_level_score
                        progress_text = f"Next: {progress}/{total_needed} pts"
                    else:
                        progress_text = "Next: MAX LEVEL"
                else:
                    progress_text = "MAX LEVEL REACHED!"
                
                progress_surface = small_font.render(progress_text, True, self.config.WHITE)
                progress_x = self.config.DIFFICULTY_POSITION[0]
                progress_y = self.config.DIFFICULTY_POSITION[1] + 25
                self.screen.blit(progress_surface, (progress_x, progress_y))
                
            except Exception as e:
                print(f"⚠️ Warning: Failed to draw difficulty progress: {e}")
                
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw difficulty: {e}")
    
    def draw_spawn_info(self):
        """Draw spawn rate and pattern information"""
        try:
            # Spawn rate
            spawn_rate_text = self.font.render(f"Spawn: {self.spawn_manager.get_spawn_rate_display()}", True, self.config.WHITE)
            self.screen.blit(spawn_rate_text, self.config.SPAWN_RATE_POSITION)
            
            # Current pattern (smaller font)
            try:
                small_font = pygame.font.SysFont(None, 24)
                pattern_text = small_font.render(f"Pattern: {self.spawn_manager.get_current_pattern_name()}", True, self.config.WHITE)
                pattern_x = self.config.WIDTH - pattern_text.get_width() - 10
                self.screen.blit(pattern_text, (pattern_x, 10))
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw spawn info: {e}")

    def draw_lives(self):
        """Draw lives information on screen"""
        try:
            lives_text = self.font.render(f"Lives: {self.lives}", True, self.config.WHITE)
            self.screen.blit(lives_text, self.config.LIVES_POSITION)
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw lives: {e}")

    def draw_active_power_ups(self):
        """Draw active power-up information on screen"""
        try:
            if self.active_power_ups:
                small_font = pygame.font.SysFont(None, 20)
                y_offset = self.config.POWER_UP_POSITION[1]

                for active_power_up in self.active_power_ups:
                    # Get power-up color from config
                    power_up_info = self.config.POWER_UP_TYPES.get(active_power_up.power_type, {})
                    color = power_up_info.get("color", self.config.WHITE)

                    # Create text with power-up name and remaining time
                    effect_name = active_power_up.power_type.replace("_", " ").title()
                    power_up_text = small_font.render(f"{effect_name}: {active_power_up.get_remaining_time_display()}", True, color)
                    self.screen.blit(power_up_text, (self.config.POWER_UP_POSITION[0], y_offset))
                    y_offset += 22  # Move down for next power-up

        except Exception as e:
            print(f"⚠️ Warning: Failed to draw active power-ups: {e}")

    def draw_game_over(self):
        """Draw game over screen"""
        try:
            text = self.font.render("Game Over! Press R to Restart or Q to Quit", True, self.config.WHITE)
            text_x = self.config.WIDTH // 2 - text.get_width() // 2
            text_y = int(self.config.HEIGHT * self.config.GAME_OVER_Y_OFFSET)
            self.screen.blit(text, (text_x, text_y))
            
            # Show final score and difficulty
            final_score_text = self.font.render(f"Final Score: {self.score}", True, self.config.WHITE)
            final_score_x = self.config.WIDTH // 2 - final_score_text.get_width() // 2
            final_score_y = text_y + 50
            self.screen.blit(final_score_text, (final_score_x, final_score_y))
            
            final_level_text = self.font.render(f"Final Level: {self.difficulty_level}", True, self.config.WHITE)
            final_level_x = self.config.WIDTH // 2 - final_level_text.get_width() // 2
            final_level_y = final_score_y + 40
            self.screen.blit(final_level_text, (final_level_x, final_level_y))
            
            # Show final spawn pattern
            final_pattern_text = self.font.render(f"Final Pattern: {self.spawn_manager.get_current_pattern_name()}", True, self.config.WHITE)
            final_pattern_x = self.config.WIDTH // 2 - final_pattern_text.get_width() // 2
            final_pattern_y = final_level_y + 40
            self.screen.blit(final_pattern_text, (final_pattern_x, final_pattern_y))
            
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw game over screen: {e}")
    
    def draw(self):
        """Draw all game elements"""
        try:
            self.screen.fill(self.config.BLACK)
            
            if not self.game_over:
                # Draw game elements
                try:
                    self.player.draw(self.screen)
                except Exception as e:
                    print(f"⚠️ Warning: Failed to draw player: {e}")
                    
                for enemy in self.enemies:
                    try:
                        enemy.draw(self.screen)
                    except Exception as e:
                        print(f"⚠️ Warning: Failed to draw enemy: {e}")

                # Draw power-ups
                for power_up in self.power_ups:
                    try:
                        power_up.draw(self.screen)
                    except Exception as e:
                        print(f"⚠️ Warning: Failed to draw power-up: {e}")

                self.draw_score()
                self.draw_difficulty()
                self.draw_spawn_info()
                self.draw_lives()
                self.draw_active_power_ups()
            else:
                self.draw_game_over()
                
        except Exception as e:
            print(f"⚠️ Warning: Drawing error: {e}")
    
    def update(self):
        """Update game logic"""
        try:
            if not self.game_over:
                # Spawn enemies using spawn manager
                self.enemy_timer += 1
                if self.spawn_manager.should_spawn_enemy(self.enemy_timer):
                    self.spawn_enemy(1)  # Spawn single enemy
                    self.enemy_timer = 0

                # Check for burst spawning
                if self.difficulty_level >= self.config.BURST_ACTIVATION_LEVEL:
                    self.spawn_burst()

                # Spawn power-ups randomly
                self.spawn_power_up()

                # Update enemies
                self.update_enemies()

                # Update power-ups
                self.update_power_ups()

                # Update active power-up effects
                self.update_active_power_ups()

        except Exception as e:
            print(f"⚠️ Warning: Game update error: {e}")
    
    def run(self):
        """Main game loop"""
        print("🎮 Starting game loop...")
        print(f"🎯 Initial difficulty level: {self.difficulty_level}")
        print(f"🔄 Initial spawn pattern: {self.spawn_manager.get_current_pattern_name()}")
        
        try:
            while True:
                try:
                    # Event handling
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            print("👋 Game closed by user")
                            return
                    
                    # Handle input
                    self.handle_input()

                    # Update game state
                    self.update()

                    # Update player invincibility
                    self.player.update_invincibility()

                    # Draw everything
                    self.draw()
                    
                    # Update display
                    pygame.display.flip()
                    self.clock.tick(self.config.FPS)
                    
                except Exception as e:
                    print(f"⚠️ Warning: Error in game loop iteration: {e}")
                    # Continue running the game loop
                    continue
                    
        except KeyboardInterrupt:
            print("\n⏹️ Game interrupted by user")
        except Exception as e:
            print(f"❌ Fatal error in game loop: {e}")
            traceback.print_exc()
        finally:
            print("�� Game loop ended")
