
import math
import pygame
import simulation
from physics import G

# Colors
SPACE_BLACK = (5, 8, 20)
YELLOW = (255, 255, 80)
BLUE = (40, 122, 184)
TRAIL_BLUE = (90, 150, 210)

# Camera settings
ZOOM_FACTOR = 1.15
MIN_ZOOM = 0.1
MAX_ZOOM = 10.0

# Trail settings
TRAIL_ORBITS = 1.5
SECONDS_PER_DAY = 86400
SECONDS_PER_YEAR = 365.25 * SECONDS_PER_DAY


def get_orbital_period():
    """Estimate the orbital period for a bound two-body orbit."""
    r_vector = simulation.earth.position - simulation.sun.position
    v_vector = simulation.earth.velocity - simulation.sun.velocity

    r = math.sqrt(float(r_vector @ r_vector))
    v_squared = float(v_vector @ v_vector)

    if r == 0:
        return SECONDS_PER_YEAR

    mu = G * (simulation.sun.mass + simulation.earth.mass)
    specific_energy = v_squared / 2 - mu / r

    # Unbound trajectories do not have a closed orbital period.
    if specific_energy >= 0:
        return SECONDS_PER_YEAR

    semi_major_axis = -mu / (2 * specific_energy)
    period = 2 * math.pi * math.sqrt(semi_major_axis**3 / mu)

    return period


def world_to_screen(position, center, offset, scale, zoom):
    return (
        round(center[0] + offset.x + position[0] * scale * zoom),
        round(center[1] + offset.y - position[1] * scale * zoom)
    )


def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Orbital Lab - Amr")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 26)

    sun_center = (500, 350)
    pixels_per_metre = 150 / 1.496e11

    zoom = 1.0
    camera_offset = pygame.Vector2(0, 0)
    dragging = False

    # Each trail entry stores (physics position, simulated time).
    trail = []
    simulation_time = 0.0
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
                    simulation.change_earth_speed(2000)

                    # Clear the previous orbit and restart simulated time.
                    trail.clear()
                    simulation_time = 0.0
                    frame_counter = 0

                elif event.key == pygame.K_DOWN:
                    simulation.change_earth_speed(-2000)

                    # Clear the previous orbit and restart simulated time.
                    trail.clear()
                    simulation_time = 0.0
                    frame_counter = 0

                elif event.key == pygame.K_r:
                    simulation.reset_simulation()
                    trail.clear()
                    simulation_time = 0.0
                    frame_counter = 0

                elif event.key == pygame.K_c:
                    zoom = 1.0
                    camera_offset = pygame.Vector2(0, 0)

                elif event.key == pygame.K_SPACE:
                    paused = not paused

            elif event.type == pygame.MOUSEWHEEL:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                old_zoom = zoom

                if event.y > 0:
                    zoom = min(zoom * ZOOM_FACTOR, MAX_ZOOM)
                elif event.y < 0:
                    zoom = max(zoom / ZOOM_FACTOR, MIN_ZOOM)

                if zoom != old_zoom:
                    ratio = zoom / old_zoom

                    camera_offset.x = (
                        mouse_x - sun_center[0]
                        - (mouse_x - sun_center[0] - camera_offset.x)
                        * ratio
                    )

                    camera_offset.y = (
                        mouse_y - sun_center[1]
                        - (mouse_y - sun_center[1] - camera_offset.y)
                        * ratio
                    )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    camera_offset.x += event.rel[0]
                    camera_offset.y += event.rel[1]

        # Advance physics and simulated time.
        if not paused:
            simulation.advance()
            simulation_time += (
                simulation.dt * simulation.STEPS_PER_FRAME
            )

        # Calculate the current orbital period.
        orbital_period = get_orbital_period()
        trail_lifetime = TRAIL_ORBITS * orbital_period

        # Record a trail point periodically.
        if not paused:
            frame_counter += 1

            if frame_counter >= trail_interval:
                trail.append(
                    (simulation.earth.position.copy(), simulation_time)
                )
                frame_counter = 0

        # Remove trail points older than 1.5 orbital periods.
        while trail and simulation_time - trail[0][1] > trail_lifetime:
            trail.pop(0)

        screen.fill(SPACE_BLACK)

        # Draw the trail using the current camera.
        trail_radius = max(1, round(2 * min(zoom, 2)))

        for position, timestamp in trail:
            screen_pos = world_to_screen(
                position,
                sun_center,
                camera_offset,
                pixels_per_metre,
                zoom
            )

            pygame.draw.circle(
                screen, TRAIL_BLUE, screen_pos, trail_radius
            )

        # Draw Sun and Earth.
        sun_pos = world_to_screen(
            simulation.sun.position,
            sun_center,
            camera_offset,
            pixels_per_metre,
            zoom
        )

        earth_pos = world_to_screen(
            simulation.earth.position,
            sun_center,
            camera_offset,
            pixels_per_metre,
            zoom
        )

        sun_radius = max(2, round(20 * zoom))
        earth_radius = max(2, round(10 * zoom))

        pygame.draw.circle(screen, YELLOW, sun_pos, sun_radius)
        pygame.draw.circle(screen, BLUE, earth_pos, earth_radius)

        # Display current speed relative to the Sun.
        relative_velocity = (
            simulation.earth.velocity - simulation.sun.velocity
        )
        current_speed = math.sqrt(
            float(relative_velocity @ relative_velocity)
        )

        speed_text = font.render(
            f"Earth speed: {current_speed / 1000:.2f} km/s",
            True,
            (230, 230, 230)
        )
        screen.blit(speed_text, (20, 20))

        if paused:
            pause_text = font.render(
                "PAUSED", True, (255, 255, 255)
            )
            screen.blit(pause_text, (20, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
