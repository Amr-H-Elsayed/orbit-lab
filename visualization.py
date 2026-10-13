import math
import pygame

# colors:
SPACE_BLACK = (5, 8, 20)
YELLOW = (255, 255, 80)
BLUE = (40, 122, 184)

def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Orbital Lab - Amr")

    clock = pygame.time.Clock()

    orbit_angle = 0.0
    orbit_radius = 150  # Distance from the sun in pixels
    sun_center = (500, 350)

    running = True

    prev_pos = [(sun_center[0], sun_center[1])] * 300  # Store previous positions for the trail

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the orbit angle
        orbit_angle += 0.02  # Adjust the speed of orbiting here
        earth_x = sun_center[0] + orbit_radius * math.cos(orbit_angle)
        earth_y = sun_center[1] + orbit_radius * math.sin(orbit_angle)

        screen.fill(SPACE_BLACK)
        # The Sun
        pygame.draw.circle(surface=screen, color=YELLOW, center=(500, 350), radius=20)
        # The Earth
        pygame.draw.circle(surface=screen, color=BLUE, center=(earth_x, earth_y), radius=10)

        # Draw the trail
        prev_pos.append((earth_x, earth_y))
        if len(prev_pos) > 300:
            prev_pos.pop(0)
        for i in range(1, len(prev_pos)):
            pygame.draw.circle(surface=screen, color=(255,255,255), center=prev_pos[i], radius=1)

        pygame.display.flip()

        clock.tick(60)  # Limit to 60 fps

    pygame.quit()

if __name__ == "__main__":
    main()