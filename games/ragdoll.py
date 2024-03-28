import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
GRAVITY = 0.2
TENSION = 10  # Strong tension force
REPULSION_FORCE = 1  # Force applied to overlapping body parts

# Ragdoll body parts
ragdoll = {
    "head": {"position": [400, 100], "radius": 20, "connected_to": ["torso1"], "velocity": [0, 0]},
    "torso1": {"position": [400, 150], "size": [30, 40], "connected_to": ["head", "torso2", "arm_left", "arm_right"], "velocity": [0, 0]},
    "torso2": {"position": [400, 200], "size": [30, 40], "connected_to": ["torso1", "leg_left", "leg_right"], "velocity": [0, 0]},
    "arm_left": {"position": [370, 160], "size": [20, 60], "connected_to": ["torso1"], "velocity": [0, 0]},
    "arm_right": {"position": [430, 160], "size": [20, 60], "connected_to": ["torso1"], "velocity": [0, 0]},
    "leg_left": {"position": [390, 240], "size": [20, 70], "connected_to": ["torso2"], "velocity": [0, 0]},
    "leg_right": {"position": [410, 240], "size": [20, 70], "connected_to": ["torso2"], "velocity": [0, 0]}
}

# Skeleton connections
skeleton = [
    ("head", "torso1"),
    ("torso1", "torso2"),
    ("torso1", "arm_left"),
    ("torso1", "arm_right"),
    ("torso2", "leg_left"),
    ("torso2", "leg_right")
]

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ragdoll Simulation")
clock = pygame.time.Clock()

selected_part = None
mouse_offset = [0, 0]

def draw_ragdoll():
    for part, data in ragdoll.items():
        if part == "head":
            pygame.draw.circle(screen, BLACK, data["position"], data["radius"])
        else:
            pygame.draw.ellipse(screen, BLACK, (data["position"], data["size"]))

def draw_skeleton():
    for connection in skeleton:
        start_pos = ragdoll[connection[0]]["position"]
        end_pos = ragdoll[connection[1]]["position"]
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 3)

def apply_repulsion():
    for part1, data1 in ragdoll.items():
        for part2, data2 in ragdoll.items():
            if part1 != part2:
                if isinstance(data1.get("radius"), int) and isinstance(data2.get("radius"), int):
                    distance = pygame.math.Vector2(data1["position"]).distance_to(data2["position"])
                    if distance < data1["radius"] + data2["radius"]:
                        repulsion_vector = pygame.math.Vector2(data2["position"]) - pygame.math.Vector2(data1["position"])
                        repulsion_vector.scale_to_length(REPULSION_FORCE)
                        data1["position"] -= repulsion_vector / 2
                        data2["position"] += repulsion_vector / 2

def move_connected_parts(part, offset):
    # Stack to keep track of body parts to move
    stack = [part]

    while stack:
        current_part = stack.pop()
        current_offset = ragdoll[current_part]["position"][0] - ragdoll[part]["position"][0], ragdoll[current_part]["position"][1] - ragdoll[part]["position"][1]
        current_offset = current_offset[0] - offset[0], current_offset[1] - offset[1]

        ragdoll[current_part]["position"][0] += current_offset[0]
        ragdoll[current_part]["position"][1] += current_offset[1]

        stack.extend(ragdoll[current_part]["connected_to"])


def main():
    global selected_part, mouse_offset

    while True:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for part, data in ragdoll.items():
                    if part == "head":
                        distance = pygame.math.Vector2(data["position"]).distance_to(mouse_pos)
                        if distance <= data["radius"]:
                            selected_part = part
                            mouse_offset = [data["position"][0] - mouse_pos[0], data["position"][1] - mouse_pos[1]]
                            break
                    else:
                        if data["position"][0] <= mouse_pos[0] <= data["position"][0] + data["size"][0] \
                            and data["position"][1] <= mouse_pos[1] <= data["position"][1] + data["size"][1]:
                            selected_part = part
                            mouse_offset = [data["position"][0] - mouse_pos[0], data["position"][1] - mouse_pos[1]]
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_part = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_part:
                    mouse_pos = pygame.mouse.get_pos()
                    ragdoll[selected_part]["position"] = [mouse_pos[0] + mouse_offset[0], mouse_pos[1] + mouse_offset[1]]
                    move_connected_parts(selected_part, mouse_offset)

        # Apply gravity
        for part, data in ragdoll.items():
            data["velocity"][1] += GRAVITY
            data["position"][1] += data["velocity"][1]  
            # Check if the body part has hit the bottom of the screen
            if data["position"][1] >= SCREEN_HEIGHT:
                data["velocity"] = [0, 0]
                data["position"][1] = SCREEN_HEIGHT

        # Apply repulsion
        apply_repulsion()

        # Draw skeleton and ragdoll
        draw_skeleton()
        draw_ragdoll()

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
