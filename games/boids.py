import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 1000, 1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bird Flock Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constants
num_birds = 20
bird_size = 20
max_speed = 6
separation_distance = 40
alignment_distance = 40
cohesion_distance = 40
radius = min(width, height) // 2

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(bird_size, width - bird_size)
        self.y = random.randint(bird_size, height - bird_size)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.max_speed = max_speed * (0.8 + 0.4 * random.random())
        self.turning_factor = 0.8 + 0.4 * random.random()

    def move(self, birds):
        separation_vector = self.get_separation_vector(birds)
        alignment_vector = self.get_alignment_vector(birds)
        cohesion_vector = self.get_cohesion_vector(birds)
        attraction_vector = self.get_attraction_vector(pygame.mouse.get_pos())

        self.vx += (separation_vector[0] + alignment_vector[0] + cohesion_vector[0] + attraction_vector[0]) * self.turning_factor
        self.vy += (separation_vector[1] + alignment_vector[1] + cohesion_vector[1] + attraction_vector[1]) * self.turning_factor

        self.limit_speed()

        self.x += self.vx
        self.y += self.vy

        self.handle_boundaries()

    def get_separation_vector(self, birds):
        separation_vector = [0, 0]
        count = 0

        for other_bird in birds:
            if other_bird != self:
                distance = ((self.x - other_bird.x) ** 2 + (self.y - other_bird.y) ** 2) ** 0.5
                if distance < separation_distance:
                    dx = self.x - other_bird.x
                    dy = self.y - other_bird.y
                    separation_vector[0] += 50 * dx / (distance ** 2)
                    separation_vector[1] += 50 * dy / (distance ** 2)
                    count += 1

        if count > 0:
            separation_vector[0] /= count
            separation_vector[1] /= count

        return separation_vector

    def get_alignment_vector(self, birds):
        alignment_vector = [0, 0]
        count = 0

        for other_bird in birds:
            if other_bird != self:
                distance = ((self.x - other_bird.x) ** 2 + (self.y - other_bird.y) ** 2) ** 0.5
                if distance < alignment_distance:
                    alignment_vector[0] += other_bird.vx
                    alignment_vector[1] += other_bird.vy
                    count += 1

        if count > 0:
            alignment_vector[0] /= count
            alignment_vector[1] /= count
            alignment_vector[0] = (alignment_vector[0] - self.vx) / 10
            alignment_vector[1] = (alignment_vector[1] - self.vy) / 10

        return alignment_vector

    def get_cohesion_vector(self, birds):
        cohesion_vector = [0, 0]
        count = 0

        for other_bird in birds:
            if other_bird != self:
                distance = ((self.x - other_bird.x) ** 2 + (self.y - other_bird.y) ** 2) ** 0.5
                if distance < cohesion_distance:
                    cohesion_vector[0] += other_bird.x
                    cohesion_vector[1] += other_bird.y
                    count += 1

        if count > 0:
            cohesion_vector[0] /= count
            cohesion_vector[1] /= count
            cohesion_vector[0] = (cohesion_vector[0] - self.x) / 80
            cohesion_vector[1] = (cohesion_vector[1] - self.y) / 80

        return cohesion_vector

    def get_attraction_vector(self, mouse_pos):
        attraction_vector = [0, 0]
        distance = ((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) ** 0.5
        if distance > 100:
            attraction_vector[0] = (mouse_pos[0] - self.x) / (distance * 2)
            attraction_vector[1] = (mouse_pos[1] - self.y) / (distance * 2)
        return attraction_vector

    def limit_speed(self):
        speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed

    def handle_boundaries(self):
        distance_from_center = ((self.x - width // 2) ** 2 + (self.y - height // 2) ** 2) ** 0.5
        if distance_from_center > radius - bird_size:
            angle = math.atan2(self.y - height // 2, self.x - width // 2)
            self.x = width // 2 + (radius - bird_size) * math.cos(angle)
            self.y = height // 2 + (radius - bird_size) * math.sin(angle)

    def draw(self):
        pygame.draw.circle(window, WHITE, (int(self.x), int(self.y)), bird_size // 2)

# Create bird objects
birds = [Bird() for _ in range(num_birds)]

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # Limit the frame rate to 60 FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill(BLACK)

    # Begin clipping path
    pygame.draw.circle(window, BLACK, (width // 2, height // 2), radius)
    pygame.draw.circle(window, WHITE, (width // 2, height // 2), radius, 1)

    # Move and draw birds
    for bird in birds:
        bird.move(birds)
        bird.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()