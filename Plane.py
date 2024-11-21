import random
import pygame
import time

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the Player object extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((45, 145, 245))
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        speed = 5  # Player's base speed
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the Enemy object extending pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 0, 0))  # Red enemies
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Create custom events for adding enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# Game variables
high_score = 0
running = True
game_active = False

# Function to display the home screen
def home_screen():
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        title_surface = font.render('The Interstellar Adventure', True, (255, 255, 255))
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Start button
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        button_text = pygame.font.Font(None, 36).render('Start Game', True, (0, 0, 0))
        screen.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  # Start the game

        pygame.display.flip()

# Function to display the end screen
def end_screen(score):
    global high_score
    if score > high_score:
        high_score = score

    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        game_over_surface = font.render('Game Over', True, (255, 0, 0))
        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        score_surface = pygame.font.Font(None, 36).render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, SCREEN_HEIGHT // 2))

        high_score_surface = pygame.font.Font(None, 36).render(f'High Score: {high_score}', True, (255, 255, 255))
        screen.blit(high_score_surface, (SCREEN_WIDTH // 2 - high_score_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        # Restart button
        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        pygame.draw.rect(screen, (0, 0, 255), restart_button)
        button_text = pygame.font.Font(None, 36).render('Restart', True, (255, 255, 255))
        screen.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 110))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return  # Restart the game

        pygame.display.flip()

# Main game loop
def main():
    global running, game_active
    score = 0
    score_increment_time = time.time()  # Start time for score increment

    # Create player instance
    player = Player()

    # Create sprite groups
    enemies = pygame.sprite.Group()

    while running:
        if not game_active:
            home_screen()
            game_active = True
            score = 0
            player.rect.center = (100, SCREEN_HEIGHT // 2)  # Reset player position

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == ADDENEMY:
                enemies.add(Enemy())

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # Increment score by 1 every second
        if time.time() - score_increment_time >= 1:
            score += 1
            score_increment_time = time.time()  # Reset the timer

        # Update all sprites
        enemies.update()

        # Check for collisions
        if pygame.sprite.spritecollideany(player, enemies):
            game_active = False
            end_screen(score)  # Show end screen if player collides with enemy

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw all sprites
        for entity in enemies:
            screen.blit(entity.surf, entity.rect)
        screen.blit(player.surf, player.rect)

        # Display score
        score_surface = pygame.font.Font(None, 36).render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        # Refresh the display
        pygame.display.flip()

        # Maintain frame rate
        clock.tick(30)

    pygame.quit()

# Start the game
main()
