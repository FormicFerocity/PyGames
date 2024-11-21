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
        self.invincible = False  # Track if player is invincible
        self.size = 1.0  # Size multiplier for player

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

        # Scale player size based on size multiplier
        self.surf = pygame.transform.scale(self.surf, (int(75 * self.size), int(25 * self.size)))

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

class FastEnemy(Enemy):
    def __init__(self):
        super(FastEnemy, self).__init__()
        self.speed = random.randint(10, 30)  # Faster speed

class SmallEnemy(Enemy):
    def __init__(self):
        super(SmallEnemy, self).__init__()
        self.surf = pygame.Surface((10, 5))  # Smaller size
        self.surf.fill((255, 255, 0))  # Different color for small enemies

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, effect_type):
        super(PowerUp, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.effect_type = effect_type
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        if effect_type == 'reduce_enemy_speed':
            self.surf.fill((0, 255, 0))  # Green for reducing enemy speed
        elif effect_type == 'decrease_player_size':
            self.surf.fill((0, 0, 255))  # Blue for decreasing player size
        elif effect_type == 'decrease_enemy_size':
            self.surf.fill((255, 165, 0))  # Orange for decreasing enemy size
        elif effect_type == 'invincibility':
            self.surf.fill((255, 255, 255))  # White for invincibility

        self.speed = random.randint(2, 5)  # Speed for the power-up movement

    def apply_effect(self, player, enemies):
        if self.effect_type == 'reduce_enemy_speed':
            for enemy in enemies:
                enemy.speed = max(1, enemy.speed - 5)  # Decrease speed
        elif self.effect_type == 'decrease_player_size':
            player.size = max(0.5, player.size - 0.1)  # Decrease player size
        elif self.effect_type == 'decrease_enemy_size':
            for enemy in enemies:
                enemy.rect.width = max(5, enemy.rect.width - 5)  # Decrease enemy size
        elif self.effect_type == 'invincibility':
            player.invincible = True  # Make player invincible
            pygame.time.set_timer(pygame.USEREVENT + 2, 3000)  # Invincible for 3 seconds

    # Move the power-up sprite
    def update(self):
        self.rect.move_ip(-self.speed, 0)  # Move left
        if self.rect.right < 0:
            self.kill()  # Remove if it goes off-screen

class Debuff(pygame.sprite.Sprite):
    def __init__(self, effect_type):
        super(Debuff, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.effect_type = effect_type
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        if effect_type == 'increase_enemy_speed':
            self.surf.fill((255, 0, 255))  # Magenta for increasing enemy speed
        elif effect_type == 'increase_player_size':
            self.surf.fill((255, 165, 0))  # Orange for increasing player size
        elif effect_type == 'increase_enemy_size':
            self.surf.fill((0, 255, 255))  # Cyan for increasing enemy size

    def apply_effect(self, player, enemies):
        if self.effect_type == 'increase_enemy_speed':
            for enemy in enemies:
                enemy.speed += 5  # Increase speed
        elif self.effect_type == 'increase_player_size':
            player.size += 0.1  # Increase player size
        elif self.effect_type == 'increase_enemy_size':
            for enemy in enemies:
                enemy.rect.width += 5  # Increase enemy size

# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Create custom events for adding enemies, power-ups, and debuffs
ADDENEMY = pygame.USEREVENT + 1
ADDPOWERUP = pygame.USEREVENT + 2
ADDEBUFF = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 500)
pygame.time.set_timer(ADDPOWERUP, 10000)  # Every 10 seconds
pygame.time.set_timer(ADDEBUFF, 15000)  # Every 15 seconds

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
        screen.blit(high_score_surface, (SCREEN_WIDTH // 2 - high_score_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        restart_text = pygame.font.Font(None, 36).render('Restart Game', True, (0, 0, 0))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 110))

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
while True:
    home_screen()  # Show the home screen before starting the game

    player = Player()
    enemies = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    debuffs = pygame.sprite.Group()

    score = 0
    game_active = True
    last_score_increment_time = time.time()  # Track the last time the score was incremented

    while game_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_active = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_active = False
            if event.type == ADDENEMY:
                # Randomly choose which enemy to add
                if random.random() < 0.5:
                    enemies.add(Enemy())
                elif random.random() < 0.8:
                    enemies.add(FastEnemy())
                else:
                    enemies.add(SmallEnemy())
            if event.type == ADDPOWERUP:
                effect_type = random.choice(['reduce_enemy_speed', 'decrease_player_size', 'decrease_enemy_size', 'invincibility'])
                power_ups.add(PowerUp(effect_type))
            if event.type == ADDEBUFF:
                effect_type = random.choice(['increase_enemy_speed', 'increase_player_size', 'increase_enemy_size'])
                debuffs.add(Debuff(effect_type))
            if event.type == pygame.USEREVENT + 2:  # Invincibility timer
                player.invincible = False

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        power_ups.update()
        debuffs.update()

        # Check for collisions with enemies
        if pygame.sprite.spritecollideany(player, enemies) and not player.invincible:
            game_active = False  # End game if player collides with an enemy

        # Check for collisions with power-ups
        power_up_collisions = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in power_up_collisions:
            power_up.apply_effect(player, enemies)

        # Check for collisions with debuffs
        debuff_collisions = pygame.sprite.spritecollide(player, debuffs, True)
        for debuff in debuff_collisions:
            debuff.apply_effect(player, enemies)

        # Update score every second
        if time.time() - last_score_increment_time >= 1:
            score += 1
            last_score_increment_time = time.time()  # Reset the timer

        # Drawing
        screen.fill((30, 30, 30))  # Dark background
        screen.blit(player.surf, player.rect)

        for entity in enemies:
            screen.blit(entity.surf, entity.rect)
        for power_up in power_ups:
            screen.blit(power_up.surf, power_up.rect)
        for debuff in debuffs:
            screen.blit(debuff.surf, debuff.rect)

        # Display score
        score_surface = pygame.font.Font(None, 36).render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        # Refresh the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    end_screen(score)
