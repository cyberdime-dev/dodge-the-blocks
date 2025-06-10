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

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

# Player setup
player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT)

# Enemy list
enemies = []

# Score tracking
score = 0
game_over = False

# Function to spawn a new enemy
def spawn_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    enemy = pygame.Rect(x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemies.append(enemy)

# Function to display score
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Game Over screen
def show_game_over():
    text = font.render("Game Over! Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

# Main Game Loop
def main():
    global score, game_over, enemies

    enemy_timer = 0

    while True:
        screen.fill(BLACK)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            # Player movement
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += PLAYER_SPEED

            # Enemy spawn timer
            enemy_timer += 1
            if enemy_timer >= 30:  # Adjust spawn frequency
                spawn_enemy()
                enemy_timer = 0

            # Move enemies and check for collision
            for enemy in enemies[:]:
                enemy.y += ENEMY_SPEED
                if enemy.colliderect(player):
                    game_over = True
                if enemy.top > HEIGHT:
                    enemies.remove(enemy)
                    score += 1

            # Draw player
            pygame.draw.rect(screen, BLUE, player)

            # Draw enemies
            for enemy in enemies:
                pygame.draw.rect(screen, RED, enemy)

            # Draw score
            draw_score()

        else:
            show_game_over()
            if keys[pygame.K_r]:
                # Reset game
                player.x = WIDTH // 2 - PLAYER_WIDTH // 2
                enemies.clear()
                score = 0
                game_over = False
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()
