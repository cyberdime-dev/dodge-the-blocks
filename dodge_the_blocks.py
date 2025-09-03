import pygame
import random
import sys

# Initialize Pygame
pygame.init()


class Config:
    """Game configuration and constants"""
    def __init__(self):
        # Display settings
        self.WIDTH = 600
        self.HEIGHT = 800
        self.FPS = 60
        
        # Player settings
        self.PLAYER_WIDTH = 50
        self.PLAYER_HEIGHT = 50
        self.PLAYER_SPEED = 7
        self.PLAYER_START_Y_OFFSET = 20
        
        # Enemy settings
        self.ENEMY_WIDTH = 50
        self.ENEMY_HEIGHT = 50
        self.ENEMY_SPEED = 5
        self.ENEMY_SPAWN_RATE = 30
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        
        # UI settings
        self.SCORE_POSITION = (10, 10)
        self.GAME_OVER_Y_OFFSET = 0.5  # Center of screen


class Player:
    def __init__(self, config, x, y):
        self.config = config
        self.rect = pygame.Rect(x, y, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
        self._speed = config.PLAYER_SPEED
        
    @property
    def speed(self):
        """Get player speed"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        """Set player speed with validation"""
        if value >= 0:
            self._speed = value
    
    def move(self, keys, screen_width):
        """Move player based on key input"""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self._speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self._speed
    
    def draw(self, screen):
        """Draw player on screen"""
        pygame.draw.rect(screen, self.config.BLUE, self.rect)
    
    def reset_position(self, screen_width, screen_height):
        """Reset player to starting position"""
        self.rect.x = screen_width // 2 - self.config.PLAYER_WIDTH // 2
        self.rect.y = screen_height - self.config.PLAYER_HEIGHT - self.config.PLAYER_START_Y_OFFSET
    
    def get_position(self):
        """Get current player position"""
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x, y):
        """Set player position with bounds checking"""
        if 0 <= x <= self.config.WIDTH - self.config.PLAYER_WIDTH:
            self.rect.x = x
        if 0 <= y <= self.config.HEIGHT - self.config.PLAYER_HEIGHT:
            self.rect.y = y


class Enemy:
    def __init__(self, config, x, y):
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
        """Draw enemy on screen"""
        pygame.draw.rect(screen, self.config.RED, self.rect)
    
    def is_off_screen(self, screen_height):
        """Check if enemy has moved off screen"""
        return self.rect.top > screen_height
    
    def collides_with(self, player):
        """Check collision with player"""
        return self.rect.colliderect(player.rect)
    
    def get_position(self):
        """Get current enemy position"""
        return (self.rect.x, self.rect.y)


class Game:
    def __init__(self):
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("Dodge the Blocks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        
        # Game state
        self._score = 0
        self._game_over = False
        self._enemy_timer = 0
        
        # Game objects
        self.player = Player(
            self.config,
            self.config.WIDTH // 2 - self.config.PLAYER_WIDTH // 2,
            self.config.HEIGHT - self.config.PLAYER_HEIGHT - self.config.PLAYER_START_Y_OFFSET
        )
        self.enemies = []
    
    @property
    def score(self):
        """Get current score"""
        return self._score
    
    @score.setter
    def score(self, value):
        """Set score with validation"""
        if value >= 0:
            self._score = value
    
    @property
    def game_over(self):
        """Get game over state"""
        return self._game_over
    
    @game_over.setter
    def game_over(self, value):
        """Set game over state"""
        self._game_over = bool(value)
    
    @property
    def enemy_timer(self):
        """Get enemy spawn timer"""
        return self._enemy_timer
    
    @enemy_timer.setter
    def enemy_timer(self, value):
        """Set enemy spawn timer"""
        if value >= 0:
            self._enemy_timer = value
    
    def spawn_enemy(self):
        """Spawn a new enemy at random x position"""
        x = random.randint(0, self.config.WIDTH - self.config.ENEMY_WIDTH)
        enemy = Enemy(self.config, x, -self.config.ENEMY_HEIGHT)
        self.enemies.append(enemy)
    
    def update_enemies(self):
        """Update enemy positions and check collisions"""
        for enemy in self.enemies[:]:
            enemy.move()
            
            # Check collision with player
            if enemy.collides_with(self.player):
                self.game_over = True
                return
            
            # Remove enemies that are off screen and award points
            if enemy.is_off_screen(self.config.HEIGHT):
                self.enemies.remove(enemy)
                self.score += 1
    
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        if not self.game_over:
            self.player.move(keys, self.config.WIDTH)
        else:
            if keys[pygame.K_r]:
                self.reset_game()
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
    
    def reset_game(self):
        """Reset game to initial state"""
        self.player.reset_position(self.config.WIDTH, self.config.HEIGHT)
        self.enemies.clear()
        self.score = 0
        self.game_over = False
        self.enemy_timer = 0
    
    def draw_score(self):
        """Draw score on screen"""
        score_text = self.font.render(f"Score: {self.score}", True, self.config.WHITE)
        self.screen.blit(score_text, self.config.SCORE_POSITION)
    
    def draw_game_over(self):
        """Draw game over screen"""
        text = self.font.render("Game Over! Press R to Restart or Q to Quit", True, self.config.WHITE)
        text_x = self.config.WIDTH // 2 - text.get_width() // 2
        text_y = int(self.config.HEIGHT * self.config.GAME_OVER_Y_OFFSET)
        self.screen.blit(text, (text_x, text_y))
    
    def draw(self):
        """Draw all game elements"""
        self.screen.fill(self.config.BLACK)
        
        if not self.game_over:
            # Draw game elements
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.draw_score()
        else:
            self.draw_game_over()
    
    def update(self):
        """Update game logic"""
        if not self.game_over:
            # Spawn enemies
            self.enemy_timer += 1
            if self.enemy_timer >= self.config.ENEMY_SPAWN_RATE:
                self.spawn_enemy()
                self.enemy_timer = 0
            
            # Update enemies
            self.update_enemies()
    
    def run(self):
        """Main game loop"""
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Handle input
            self.handle_input()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(self.config.FPS)


def main():
    """Initialize and run the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
