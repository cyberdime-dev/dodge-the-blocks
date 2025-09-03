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
    
    def spawn_enemy(self):
        """Spawn a new enemy at random x position"""
        try:
            x = random.randint(0, self.config.WIDTH - self.config.ENEMY_WIDTH)
            enemy = Enemy(self.config, x, -self.config.ENEMY_HEIGHT)
            self.enemies.append(enemy)
        except Exception as e:
            print(f"⚠️ Warning: Failed to spawn enemy: {e}")
    
    def update_enemies(self):
        """Update enemy positions and check collisions"""
        try:
            for enemy in self.enemies[:]:
                try:
                    enemy.move()
                    
                    # Check collision with player
                    if enemy.collides_with(self.player):
                        self.game_over = True
                        return
                    
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
            self.score = 0
            self.game_over = False
            self.enemy_timer = 0
        except Exception as e:
            print(f"⚠️ Warning: Failed to reset game: {e}")
    
    def draw_score(self):
        """Draw score on screen"""
        try:
            score_text = self.font.render(f"Score: {self.score}", True, self.config.WHITE)
            self.screen.blit(score_text, self.config.SCORE_POSITION)
        except Exception as e:
            print(f"⚠️ Warning: Failed to draw score: {e}")
    
    def draw_game_over(self):
        """Draw game over screen"""
        try:
            text = self.font.render("Game Over! Press R to Restart or Q to Quit", True, self.config.WHITE)
            text_x = self.config.WIDTH // 2 - text.get_width() // 2
            text_y = int(self.config.HEIGHT * self.config.GAME_OVER_Y_OFFSET)
            self.screen.blit(text, (text_x, text_y))
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
                        
                self.draw_score()
            else:
                self.draw_game_over()
                
        except Exception as e:
            print(f"⚠️ Warning: Drawing error: {e}")
    
    def update(self):
        """Update game logic"""
        try:
            if not self.game_over:
                # Spawn enemies
                self.enemy_timer += 1
                if self.enemy_timer >= self.config.ENEMY_SPAWN_RATE:
                    self.spawn_enemy()
                    self.enemy_timer = 0
                
                # Update enemies
                self.update_enemies()
                
        except Exception as e:
            print(f"⚠️ Warning: Game update error: {e}")
    
    def run(self):
        """Main game loop"""
        print("🎮 Starting game loop...")
        
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
            print("🔄 Game loop ended")
