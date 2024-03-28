import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ragdoll Simulation")

clock = pygame.time.Clock()

class BodyPart:
    def __init__(self, color, pos, size):
        self.color = color
        self.rect = pygame.Rect(pos, size)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def move_body_part(body_part, dx, dy):
    body_part.rect.x += dx
    body_part.rect.y += dy

# Define body parts
head = BodyPart((255, 0, 0), (400, 100), (50, 50))
torso = BodyPart((0, 255, 0), (400, 150), (20, 100))
left_arm = BodyPart((0, 0, 255), (380, 150), (20, 50))
right_arm = BodyPart((0, 0, 255), (420, 150), (20, 50))
left_leg = BodyPart((255, 255, 0), (390, 250), (20, 50))
right_leg = BodyPart((255, 255, 0), (410, 250), (20, 50))

# Define joint connections
joints = [(head.rect.midbottom, torso.rect.midtop),
          (torso.rect.midbottom, left_leg.rect.midtop),
          (torso.rect.midbottom, right_leg.rect.midtop),
          (torso.rect.midtop, left_arm.rect.midbottom),
          (torso.rect.midtop, right_arm.rect.midbottom)]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_body_part(torso, -1, 0)
    if keys[pygame.K_RIGHT]:
        move_body_part(torso, 1, 0)
    if keys[pygame.K_UP]:
        move_body_part(torso, 0, -1)
    if keys[pygame.K_DOWN]:
        move_body_part(torso, 0, 1)

    # Clear screen
    screen.fill((255, 255, 255))

    # Draw body parts
    head.draw()
    torso.draw()
    left_arm.draw()
    right_arm.draw()
    left_leg.draw()
    right_leg.draw()

    # Draw joints
    for joint in joints:
        pygame.draw.line(screen, (0, 0, 0), joint[0], joint[1], 5)

    pygame.display.flip()
    clock.tick(60)
