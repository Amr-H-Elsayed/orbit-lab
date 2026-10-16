
from physics import Body, n_body_simulation

# Simulation settings
INITIAL_EARTH_SPEED = 29784.8
dt = 21600
STEPS_PER_FRAME = 10


def create_bodies():
    sun = Body(
        name="Sun",
        mass=1.989e30,
        position=[0, 0],
        velocity=[0, 0]
    )

    earth = Body(
        name="Earth",
        mass=5.972e24,
        position=[1.496e11, 0],
        velocity=[0, INITIAL_EARTH_SPEED]
    )

    return sun, earth, [sun, earth]


sun, earth, bodies = create_bodies()


def advance():
    for _ in range(STEPS_PER_FRAME):
        n_body_simulation(bodies, dt)


def reset_simulation():
    global sun, earth, bodies
    sun, earth, bodies = create_bodies()


def change_earth_speed(amount):
    global INITIAL_EARTH_SPEED
    INITIAL_EARTH_SPEED += amount
    reset_simulation()
