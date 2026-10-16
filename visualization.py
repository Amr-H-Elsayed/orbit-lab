
import math
import pygame
import simulation
from physics import G

# Colors
SPACE_BLACK = (5, 8, 20)
YELLOW = (255, 255, 80)

PLANET_COLORS = {
    "Mercury": (170, 165, 155),
    "Venus": (235, 190, 110),
    "Earth": (40, 122, 220),
    "Mars": (220, 85, 55),
    "Jupiter": (210, 165, 125),
    "Saturn": (220, 205, 155),
    "Uranus": (125, 220, 220),
    "Neptune": (65, 95, 235),
}

PLANET_RADII = {
    "Mercury": 2,
    "Venus": 3,
    "Earth": 3,
    "Mars": 2,
    "Jupiter": 6,
    "Saturn": 5,
    "Uranus": 4,
    "Neptune": 4,
}

# Camera settings
ZOOM_FACTOR = 1.15
MIN_ZOOM = 0.1
MAX_ZOOM = 10.0

# Display settings
AU = 1.496e11
PIXELS_PER_AU = 15
TRAIL_ORBITS = 1.5

# Trail appearance
TRAIL_INTERVAL = 10
TRAIL_RADIUS = 1

# Simulation speed limits
MIN_STEPS_PER_FRAME = 1
MAX_STEPS_PER_FRAME = 100
SPEED_STEP_CHANGE = 2

SECONDS_PER_YEAR = 365.25 * 86400


def get_orbital_period(body):
    """Estimate a body's orbital period from its current state."""
    r_vector = body.position - simulation.sun.position
    v_vector = body.velocity - simulation.sun.velocity

    r = float(math.sqrt(r_vector @ r_vector))
    v_squared = float(v_vector @ v_vector)

    if r == 0:
        return SECONDS_PER_YEAR

    mu = G * (simulation.sun.mass + body.mass)
    specific_energy = v_squared / 2 - mu / r

    # Unbound trajectories have no closed orbital period.
    if specific_energy >= 0:
        return SECONDS_PER_YEAR

    semi_major_axis = -mu / (2 * specific_energy)
    return 2 * math.pi * math.sqrt(semi_major_axis**3 / mu)


def world_to_screen(position, center, offset, scale, zoom):
    return (
        round(center[0] + offset.x + position[0] * scale * zoom),
        round(center[1] + offset.y - position[1] * scale * zoom)
    )


def fade_color(color, age_fraction):
    """Fade old trail points toward the background color."""
    brightness = max(0.08, 1.0 - age_fraction)

    return tuple(
        round(SPACE_BLACK[i] + (color[i] - SPACE_BLACK[i]) * brightness)
        for i in range(3)
    )


def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Orbital Lab - Amr")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 23)
    small_font = pygame.font.Font(None, 18)

    sun_center = (500, 350)
    pixels_per_metre = PIXELS_PER_AU / AU

    zoom = 1.0
    camera_offset = pygame.Vector2(0, 0)
    dragging = False

    # Each trail entry stores (position, simulated time).
    trails = {
        body.name: [] for body in simulation.planets
    }

    simulation_time = 0.0
    frame_counter = 0
    paused = False
    running = True

    def clear_trails():
        nonlocal simulation_time, frame_counter

        for points in trails.values():
            points.clear()

        simulation_time = 0.0
        frame_counter = 0

    def draw_text(text, x, y, color=(230, 230, 230)):
        surface = font.render(text, True, color)
        screen.blit(surface, (x, y))

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # Change Earth's initial orbital speed.
                if event.key == pygame.K_UP:
                    simulation.change_earth_speed(2000)
                    clear_trails()

                elif event.key == pygame.K_DOWN:
                    simulation.change_earth_speed(-2000)
                    clear_trails()

                # Reset the Solar System.
                elif event.key == pygame.K_r:
                    simulation.reset_simulation()
                    clear_trails()

                # Adjust simulation speed without changing planet velocities.
                elif event.key == pygame.K_RIGHTBRACKET:
                    simulation.STEPS_PER_FRAME = min(
                        simulation.STEPS_PER_FRAME + SPEED_STEP_CHANGE,
                        MAX_STEPS_PER_FRAME
                    )

                elif event.key == pygame.K_LEFTBRACKET:
                    simulation.STEPS_PER_FRAME = max(
                        simulation.STEPS_PER_FRAME - SPEED_STEP_CHANGE,
                        MIN_STEPS_PER_FRAME
                    )

                # Reset camera.
                elif event.key == pygame.K_c:
                    zoom = 1.0
                    camera_offset = pygame.Vector2(0, 0)

                # Pause / resume.
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

        # Advance physics.
        if not paused:
            simulation.advance()

            simulation_time += (
                simulation.dt * simulation.STEPS_PER_FRAME
            )

        # Record trail points less frequently for a dotted appearance.
        if not paused:
            frame_counter += 1

            if frame_counter >= TRAIL_INTERVAL:
                for body in simulation.planets:
                    trails[body.name].append(
                        (body.position.copy(), simulation_time)
                    )

                frame_counter = 0

        # Remove points older than approximately 1.5 orbital periods.
        for body in simulation.planets:
            lifetime = TRAIL_ORBITS * get_orbital_period(body)
            points = trails[body.name]

            while (
                points
                and simulation_time - points[0][1] > lifetime
            ):
                points.pop(0)

        screen.fill(SPACE_BLACK)

        # Draw thinner, fading trails.
        for body in simulation.planets:
            lifetime = TRAIL_ORBITS * get_orbital_period(body)
            color = PLANET_COLORS[body.name]

            for position, timestamp in trails[body.name]:
                age_fraction = (
                    (simulation_time - timestamp) / lifetime
                    if lifetime > 0 else 0
                )

                trail_color = fade_color(
                    color, min(1.0, max(0.0, age_fraction))
                )

                screen_pos = world_to_screen(
                    position,
                    sun_center,
                    camera_offset,
                    pixels_per_metre,
                    zoom
                )

                pygame.draw.circle(
                    screen, trail_color, screen_pos, TRAIL_RADIUS
                )

        # Draw the Sun.
        sun_pos = world_to_screen(
            simulation.sun.position,
            sun_center,
            camera_offset,
            pixels_per_metre,
            zoom
        )

        pygame.draw.circle(
            screen, YELLOW, sun_pos,
            max(4, round(8 * min(zoom, 2)))
        )

        # Draw planets and labels.
        for body in simulation.planets:
            planet_pos = world_to_screen(
                body.position,
                sun_center,
                camera_offset,
                pixels_per_metre,
                zoom
            )

            radius = max(
                2,
                round(PLANET_RADII[body.name] * min(zoom, 2))
            )

            pygame.draw.circle(
                screen,
                PLANET_COLORS[body.name],
                planet_pos,
                radius
            )

            label = small_font.render(
                body.name,
                True,
                PLANET_COLORS[body.name]
            )

            screen.blit(
                label,
                (planet_pos[0] + radius + 3, planet_pos[1] - 8)
            )

        # Earth speed relative to the Sun.
        relative_velocity = (
            simulation.earth.velocity - simulation.sun.velocity
        )

        current_speed = math.sqrt(
            float(relative_velocity @ relative_velocity)
        )

        draw_text(
            f"Earth speed: {current_speed / 1000:.2f} km/s",
            20, 18
        )

        # Simulation clock and current speed setting.
        years_elapsed = simulation_time / SECONDS_PER_YEAR

        draw_text(
            f"Simulated time: {years_elapsed:.3f} years",
            20, 43
        )

        simulated_days_per_second = (
            simulation.dt
            * simulation.STEPS_PER_FRAME
            * 60
            / 86400
        )

        draw_text(
            f"Simulation rate: {simulation.STEPS_PER_FRAME} steps/frame",
            20, 68
        )

        draw_text(
            f"Approx. {simulated_days_per_second:.1f} simulated days/sec",
            20, 93
        )

        # Measure Earth-Jupiter separation to verify close encounters.
        jupiter = next(
            body for body in simulation.planets
            if body.name == "Jupiter"
        )

        draw_text(
            "[ / ]: simulation speed   Up / Down: Earth speed",
            20, 143
        )

        draw_text(
            "R: reset   Space: pause   C: reset camera",
            20, 166
        )

        if paused:
            draw_text("PAUSED", 20, 191, (255, 255, 255))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
