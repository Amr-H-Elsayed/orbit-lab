from physics import Body, n_body_simulation

INITIAL_EARTH_SPEED = 29784.8

sun = Body(name="Sun", mass=1.989e30, position=[0, 0], velocity=[0, 0])
earth = Body(name="Earth", mass=5.972e24, position=[1.496e11, 0], velocity=[0, INITIAL_EARTH_SPEED])

bodies = [sun, earth]

dt = 21600         # Time step size: 21,600 seconds = 6 hours
SPEED_MULTIPLIER = 10

def advance():
    for _ in range(SPEED_MULTIPLIER):
        n_body_simulation(bodies, dt)

def reset_simulation():
    global sun, earth, bodies

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

    bodies = [sun, earth]

def change_earth_speed(amount):
    global INITIAL_EARTH_SPEED

    INITIAL_EARTH_SPEED += amount
    reset_simulation()

