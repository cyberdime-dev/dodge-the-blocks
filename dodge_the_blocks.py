import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 800
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
ENEMY_SPEED = 5
PLAYER_SPEED = 7
ENEMY_SPAWN_RATE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)


class Player:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.width = width
        self.height = height
        
    def move(self, keys, screen_width):
        """Move player based on key input"""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
    
    def draw(self, screen):
        """Draw player on screen"""
        pygame.draw.rect(screen, BLUE, self.rect)
    
    def reset_position(self, screen_width, screen_height):
        """Reset player to starting position"""
        self.rect.x = screen_width // 2 - self.width // 2
        self.rect.y = screen_height - self.height - 20


class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.width = width
        self.height = height
    
    def move(self):
        """Move enemy downward"""
        self.rect.y += self.speed
    
    def draw(self, screen):
        """Draw enemy on screen"""
        pygame.draw.rect(screen, RED, self.rect)
    
    def is_off_screen(self, screen_height):
        """Check if enemy has moved off screen"""
        return self.rect.top > screen_height
    
    def collides_with(self, player):
        """Check collision with player"""
        return self.rect.colliderect(player.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dodge the Blocks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        
        # Game state
        self.score = 0
        self.game_over = False
        self.enemy_timer = 0
        
        # Game objects
        self.player = Player(
            WIDTH // 2 - PLAYER_WIDTH // 2,
            HEIGHT - PLAYER_HEIGHT - 20,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            PLAYER_SPEED
        )
        self.enemies = []
    
    def spawn_enemy(self):
        """Spawn a new enemy at random x position"""
        x = random.randint(0, WIDTH - ENEMY_WIDTH)
        enemy = Enemy(x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED)
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
            if enemy.is_off_screen(HEIGHT):
                self.enemies.remove(enemy)
                self.score += 1
    
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        if not self.game_over:
            self.player.move(keys, WIDTH)
        else:
            if keys[pygame.K_r]:
                self.reset_game()
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
    
    def reset_game(self):
        """Reset game to initial state"""
        self.player.reset_position(WIDTH, HEIGHT)
        self.enemies.clear()
        self.score = 0
        self.game_over = False
        self.enemy_timer = 0
    
    def draw_score(self):
        """Draw score on screen"""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        """Draw game over screen"""
        text = self.font.render("Game Over! Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    
    def draw(self):
        """Draw all game elements"""
        self.screen.fill(BLACK)
        
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
            if self.enemy_timer >= ENEMY_SPAWN_RATE:
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
            self.clock.tick(FPS)


def main():
    """Initialize and run the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
