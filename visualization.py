import math
import pygame
import simulation

# Colors
SPACE_BLACK = (5, 8, 20)
YELLOW = (255, 255, 80)
BLUE = (40, 122, 184)
TRAIL_BLUE = (90, 150, 210)


def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Orbital Lab - Amr")

    clock = pygame.time.Clock()

    sun_center = (500, 350)
    pixels_per_metre = 150 / 1.496e11

    prev_pos = []
    frame_counter = 0
    trail_interval = 5

    paused = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    simulation.change_earth_speed(500)

            elif event.key == pygame.K_DOWN:
                simulation.change_earth_speed(-500)

            elif event.key == pygame.K_r:
                simulation.reset_simulation()

            elif event.key == pygame.K_SPACE:
                paused = not paused
                
        if not paused:
            simulation.advance()

        sun_pos = (
            round(sun_center[0] + sun.position[0] * pixels_per_metre),
            round(sun_center[1] - sun.position[1] * pixels_per_metre)
        )

        earth_pos = (
            round(sun_center[0] + earth.position[0] * pixels_per_metre),
            round(sun_center[1] - earth.position[1] * pixels_per_metre)
        )

        # Record a position every few frames
        frame_counter += 1
        if frame_counter >= trail_interval:
            prev_pos.append(earth_pos)
            frame_counter = 0

        # Keep the trail a manageable size
        if len(prev_pos) > 300:
            prev_pos.pop(0)

        screen.fill(SPACE_BLACK)

        # Draw the orbital trail
        for pos in prev_pos:
            pygame.draw.circle(screen, (255, 255, 255), pos, 2)
        

        # Draw the Sun and Earth
        pygame.draw.circle(screen, YELLOW, sun_pos, 20)
        pygame.draw.circle(screen, BLUE, earth_pos, 10)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
