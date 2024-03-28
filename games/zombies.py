import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player
player_size = 30
player_x = WINDOW_WIDTH // 2 - player_size // 2
player_y = WINDOW_HEIGHT - player_size * 2
player_speed = 5
player_angle = 0

# Bullets
bullet_list = []
bullet_speed = 10
bullet_size = (5, 10)

# Zombies
zombie_size = 30
zombie_list = []
zombie_spawn_rate = 1  # Seconds between zombie spawns
ZOMBIE_SPAWN_ACCELERATION = 0.99 # Zombies spawn faster as time goes on

# Game variables
zombies_killed = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()
last_zombie_spawn = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet_angle = math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))
            bullet_x = player_x + player_size // 2
            bullet_y = player_y + player_size // 2
            bullet_list.append({"x": bullet_x, "y": bullet_y, "angle": bullet_angle})

        # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x = (player_x - player_speed) % WINDOW_WIDTH
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x = (player_x + player_speed) % WINDOW_WIDTH
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y = (player_y - player_speed) % WINDOW_HEIGHT
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y = (player_y + player_speed) % WINDOW_HEIGHT
    

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_angle = (180 / math.pi) * (-math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2)))

    # Spawn zombies
    current_time = time.time()
    if current_time - last_zombie_spawn > zombie_spawn_rate:
        last_zombie_spawn = current_time
        zombie_side = random.randint(0, 3)
        if zombie_side == 0:  # Left side
            zombie_x = 0
            zombie_y = random.randint(0, WINDOW_HEIGHT - zombie_size)
        elif zombie_side == 1:  # Right side
            zombie_x = WINDOW_WIDTH - zombie_size
            zombie_y = random.randint(0, WINDOW_HEIGHT - zombie_size)
        elif zombie_side == 2:  # Top side
            zombie_x = random.randint(0, WINDOW_WIDTH - zombie_size)
            zombie_y = 0
        else:  # Bottom side
            zombie_x = random.randint(0, WINDOW_WIDTH - zombie_size)
            zombie_y = WINDOW_HEIGHT - zombie_size
        zombie_list.append({"x": zombie_x, "y": zombie_y})
        zombie_spawn_rate *= ZOMBIE_SPAWN_ACCELERATION

    # Move zombies with their x and y coords approaching the players
    for zombie in zombie_list:
        if zombie["x"] < player_x:
            zombie["x"] += 1
        elif zombie["x"] > player_x:
            zombie["x"] -= 1
        if zombie["y"] < player_y:
            zombie["y"] += 1
        elif zombie["y"] > player_y:
            zombie["y"] -= 1

    # Move bullets
    for bullet in bullet_list:
        bullet["x"] += bullet_speed * math.cos(bullet["angle"])
        bullet["y"] += bullet_speed * math.sin(bullet["angle"])
        if (
            bullet["x"] < -bullet_size[0]
            or bullet["x"] > WINDOW_WIDTH + bullet_size[0]
            or bullet["y"] < -bullet_size[1]
            or bullet["y"] > WINDOW_HEIGHT + bullet_size[1]
        ):
            if bullet in bullet_list: bullet_list.remove(bullet)

    # Check for collisions
    for bullet in bullet_list:
        for zombie in zombie_list:
            if (
                zombie["x"] < bullet["x"] < zombie["x"] + zombie_size
                and zombie["y"] < bullet["y"] < zombie["y"] + zombie_size
            ):
                if bullet in bullet_list: bullet_list.remove(bullet)
                zombie_list.remove(zombie)
                zombies_killed += 1
                
    for zombie in zombie_list:
        if (
            player_x < zombie["x"] + zombie_size/2 < player_x + player_size
            and player_y < zombie["y"] + zombie_size/2 < player_y + player_size
        ):
            font = pygame.font.Font(None, 36)
            game_over_text = font.render("Game Over", True, (0, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect)
            pygame.display.flip()
            # Wait for a few seconds
            pygame.time.wait(2000)
            # Quit the game
            pygame.quit()
            quit()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    player_rotated = pygame.transform.rotate(pygame.Surface((player_size, player_size)), player_angle)
    player_rect = player_rotated.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
    screen.blit(player_rotated, player_rect)
    pygame.draw.rect(screen, GREEN, player_rect, 2)  # Draw a green outline for visibility

    # Draw the zombies
    for zombie in zombie_list:
        pygame.draw.rect(
            screen, RED, (zombie["x"], zombie["y"], zombie_size, zombie_size)
        )

    # Draw the bullets
    for bullet in bullet_list:
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], bullet_size[0], bullet_size[1])
        pygame.draw.rect(screen, BLUE, bullet_rect)

    # Draw the score
    score_text = font.render(f"Zombies Killed: {zombies_killed}", True, BLACK)
    spawn_rate = font.render(f"Zombie Spawn Rate: {zombie_spawn_rate}", True, BLACK)
    screen.blit(score_text, (WINDOW_WIDTH - 400, 10))
    screen.blit(spawn_rate, (WINDOW_WIDTH - 400, 30))


    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate

# Quit Pygame
pygame.quit()