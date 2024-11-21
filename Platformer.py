import pygame
import sys
import random

pygame.init()

# Screen dimensions.
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer with Levels and Treasure")

# Clock and FPS settings.
clock = pygame.time.Clock()
FPS = 60

# Colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Lava color.
GREEN = (0, 255, 0)  # Power-up color.
BLUE = (0, 0, 255)  # Debuff color.
GOLD = (255, 215, 0)  # Treasure chest color.

# Player properties.
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 50
player_vel_x = 0
player_vel_y = 0
player_speed = 5
jump_speed = 15
gravity = 0.8  # Base gravity.

# Player stats.
lives = 3
has_lava_immunity = False
scroll_x = 0

# Timers for power-ups and debuffs.
power_up_duration = 5000  # 5 seconds
debuff_duration = 5000  # 5 seconds
power_up_timer = 0
debuff_timer = 0

# Current level.
level = 1

# Platforms and lava platforms.
def generate_level():
    platforms = []
    lava_platforms = []
    treasure = None

    # Generate normal platforms.
    for i in range(30):
        y = HEIGHT - random.randint(100, 400)  # Lowering platforms to be more reachable
        x = 200 + i * 300
        # Ensure first few platforms are reachable without power-ups.
        if i < 5:
            y += 0  # Keeping the first few platforms at the normal height
        platforms.append(pygame.Rect(x, y, 200, 20))

    # Generate lava platforms ensuring they are not too close to normal platforms.
    for i in range(10):
        while True:
            y = HEIGHT - random.randint(300, 400)  # Raise lava platforms higher.
            x = 600 + i * 600
            
            # Check for distance from normal platforms.
            if all(abs(x - plat.x) > 200 or abs(y - plat.y) > 20 for plat in platforms):
                lava_platforms.append(pygame.Rect(x, y, 200, 20))
                break

    # Place the treasure chest on the last platform.
    treasure = pygame.Rect(platforms[-1].x + 50, platforms[-1].y - 40, 40, 40)

    # Create power-ups and debuffs at random platform locations.
    power_ups = []
    debuffs = []

    for plat in platforms:
        power_up_chance = max(0.2 - 0.02 * (level - 1), 0.05)  # Decrease power-up probability with each level, min 5%.
        debuff_chance = 0.2 + 0.02 * (level - 1)  # Increase debuff probability with each level.

        # Ensure sufficient distance between power-ups and debuffs.
        if random.random() < power_up_chance:  # Adjusting the probability based on level.
            if len(power_ups) == 0 or abs(plat.x - power_ups[-1].x) > 200:
                power_ups.append(pygame.Rect(plat.x + 50, plat.y - 30, 30, 30))
        
        if random.random() < debuff_chance:  # Increase debuff probability with each level.
            if len(debuffs) == 0 or abs(plat.x - debuffs[-1].x) > 200:
                debuffs.append(pygame.Rect(plat.x + 50, plat.y - 30, 30, 30))

    return platforms, lava_platforms, power_ups, debuffs, treasure

platforms, lava_platforms, power_ups, debuffs, treasure = generate_level()

# Main game loop.
running = True
while running:
    clock.tick(FPS)

    # Event handling.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Increase gravity slightly with each level.
    gravity = 0.8 + 0.05 * (level - 1)  # Base gravity + 0.05 per level.

    # Apply gravity.
    player_vel_y += gravity

    # Update player position.
    player_x += player_vel_x
    player_y += player_vel_y

    # Ensure player stays within screen bounds.
    if player_x < 0:
        player_x = 0

    # Assume the player is not on the ground or a platform.
    on_ground_or_platform = False

    # Collision detection with the ground.
    if player_y + player_height >= HEIGHT - 50:
        player_y = HEIGHT - 50 - player_height
        player_vel_y = 0
        on_ground_or_platform = True

    # Collision detection with platforms.
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for platform in platforms:
        if player_rect.colliderect(platform) and player_vel_y >= 0:
            player_y = platform.y - player_height
            player_vel_y = 0
            on_ground_or_platform = True

    # Collision detection with lava platforms.
    for lava in lava_platforms:
        if player_rect.colliderect(lava):
            if not has_lava_immunity:
                lives -= 1
                player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 50
                if lives == 0:
                    running = False
                    print("Game Over!")
            else:
                player_vel_y = 0

    # Collision detection with power-ups and debuffs.
    for power_up in power_ups[:]:
        if player_rect.colliderect(power_up):
            jump_speed = 20 + (level - 1) * 5  # Increase jump height with each level.
            player_speed = 7 + (level - 1)  # Increase movement speed with each level.
            has_lava_immunity = True  # Grant lava immunity.
            power_up_timer = pygame.time.get_ticks()  # Start power-up timer.
            power_ups.remove(power_up)

    for debuff in debuffs[:]:
        if player_rect.colliderect(debuff):
            jump_speed = 10 - (level - 1) * 2  # Decrease jump height with each level.
            player_speed = 3 - (level - 1)  # Decrease movement speed with each level.
            has_lava_immunity = False  # Remove lava immunity.
            debuff_timer = pygame.time.get_ticks()  # Start debuff timer.
            debuffs.remove(debuff)

    # Power-up timer logic: Reset stats after 5 seconds.
    if power_up_timer and pygame.time.get_ticks() - power_up_timer > power_up_duration:
        jump_speed = 15  # Reset jump height.
        player_speed = 5  # Reset movement speed.
        has_lava_immunity = False  # Remove lava immunity.
        power_up_timer = 0  # Reset power-up timer.

    # Debuff timer logic: Reset stats after 5 seconds.
    if debuff_timer and pygame.time.get_ticks() - debuff_timer > debuff_duration:
        jump_speed = 15  # Reset jump height.
        player_speed = 5  # Reset movement speed.
        debuff_timer = 0  # Reset debuff timer.

    # Player input.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_vel_x = -player_speed
    elif keys[pygame.K_RIGHT]:
        player_vel_x = player_speed
    else:
        player_vel_x = 0

    if keys[pygame.K_SPACE] and on_ground_or_platform:
        player_vel_y = -jump_speed

    # Scrolling logic.
    if player_x > WIDTH / 2:
        scroll_x = player_x - WIDTH / 2
    else:
        scroll_x = 0

    # Check if the player reaches the treasure chest.
    if player_rect.colliderect(treasure):
        print(f"Level {level} complete!")
        level += 1  # Go to the next level.
        player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 50  # Reset player position.
        platforms, lava_platforms, power_ups, debuffs, treasure = generate_level()  # Generate new level.

    # Drawing.
    SCREEN.fill(WHITE)

    # Ground.
    pygame.draw.rect(SCREEN, BLACK, (0, HEIGHT - 50, WIDTH, 50))

    # Platforms.
    for platform in platforms:
        pygame.draw.rect(SCREEN, BLACK, (platform.x - scroll_x, platform.y, platform.width, platform.height))

    # Lava platforms.
    for lava in lava_platforms:
        pygame.draw.rect(SCREEN, RED, (lava.x - scroll_x, lava.y, lava.width, lava.height))

    # Treasure chest.
    pygame.draw.rect(SCREEN, GOLD, (treasure.x - scroll_x, treasure.y, treasure.width, treasure.height))

    # Power-ups.
    for power_up in power_ups:
        pygame.draw.rect(SCREEN, GREEN, (power_up.x - scroll_x, power_up.y, power_up.width, power_up.height))

    # Debuffs.
    for debuff in debuffs:
        pygame.draw.rect(SCREEN, BLUE, (debuff.x - scroll_x, debuff.y, debuff.width, debuff.height))

    # Player.
    pygame.draw.rect(SCREEN, BLACK, (player_x - scroll_x, player_y, player_width, player_height))

    # Draw lives and level.
    font = pygame.font.SysFont("Arial", 24)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    SCREEN.blit(lives_text, (10, 10))
    SCREEN.blit(level_text, (WIDTH - 100, 10))

    # Progress bar based on distance to treasure chest.
    start_position = 0  # Starting position of the player.
    distance_to_treasure = treasure.x - start_position
    progress_ratio = (player_x - start_position) / distance_to_treasure if distance_to_treasure > 0 else 1
    pygame.draw.rect(SCREEN, BLACK, (10, 40, WIDTH - 20, 20))  # Background of progress bar.
    pygame.draw.rect(SCREEN, GOLD, (10, 40, (WIDTH - 20) * progress_ratio, 20))  # Progress based on player position.

    # Update display.
    pygame.display.flip()

pygame.quit()
sys.exit()
