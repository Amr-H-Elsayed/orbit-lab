
from physics import Body, n_body_simulation, G
import math

# Simulation settings
AU = 1.496e11
INITIAL_EARTH_SPEED = 29784.8

dt = 3600
STEPS_PER_FRAME = 10

SUN_MASS = 1.989e30

# name, mass (kg), orbital radius (AU), starting angle (degrees)
PLANET_DATA = [
    ("Mercury", 3.3011e23, 0.3871, 15),
    ("Venus",   4.8675e24, 0.7233, 70),
    ("Earth",   5.9722e24, 1.0000, 130),
    ("Mars",    6.4171e23, 1.5237, 185),
    ("Jupiter", 1.8982e27, 5.2028, 230),
    ("Saturn",  5.6834e26, 9.5388, 275),
    ("Uranus",  8.6810e25, 19.191, 320),
    ("Neptune", 1.0241e26, 30.061, 345),
]


def create_bodies():
    sun = Body(
        name="Sun",
        mass=SUN_MASS,
        position=[0, 0],
        velocity=[0, 0]
    )

    planets = []

    for name, mass, radius_au, angle_degrees in PLANET_DATA:
        radius = radius_au * AU
        angle = math.radians(angle_degrees)

        # Approximate circular orbital speed around the Sun.
        speed = math.sqrt(G * SUN_MASS / radius)

        if name == "Earth":
            speed = INITIAL_EARTH_SPEED

        # Place each planet at a different orbital angle.
        position = [
            radius * math.cos(angle),
            radius * math.sin(angle)
        ]

        # Tangential velocity, perpendicular to the radius.
        velocity = [
            -speed * math.sin(angle),
            speed * math.cos(angle)
        ]

        planet = Body(
            name=name,
            mass=mass,
            position=position,
            velocity=velocity
        )

        planets.append(planet)

    bodies = [sun] + planets
    earth = next(body for body in planets if body.name == "Earth")

    return sun, earth, planets, bodies


sun, earth, planets, bodies = create_bodies()


def advance():
    for _ in range(STEPS_PER_FRAME):
        n_body_simulation(bodies, dt)


def reset_simulation():
    global sun, earth, planets, bodies
    sun, earth, planets, bodies = create_bodies()


def change_earth_speed(amount):
    global INITIAL_EARTH_SPEED

    INITIAL_EARTH_SPEED = max(
        0,
        INITIAL_EARTH_SPEED + amount
    )

    reset_simulation()
