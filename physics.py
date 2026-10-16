
import numpy as np

G = 6.67430e-11


class Body:
    def __init__(
        self,
        name: str,
        mass: float,
        position: list,
        velocity: list
    ):
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)


def distance_between(body_a, body_b):
    difference = body_b.position - body_a.position
    return np.linalg.norm(difference)


def acceleration_from(source, target, G=G):
    """Calculate the gravitational acceleration on target from source."""
    r_vector = target.position - source.position
    distance = np.linalg.norm(r_vector)

    if distance == 0:
        return np.zeros_like(target.position)

    return -G * source.mass * r_vector / distance**3


def calculate_accelerations(bodies, G=G):
    """Calculate every body's acceleration from the current positions."""
    accelerations = []

    for i, body in enumerate(bodies):
        total_acceleration = np.zeros_like(body.position)

        for j, other in enumerate(bodies):
            if i != j:
                total_acceleration += acceleration_from(
                    other, body, G=G
                )

        accelerations.append(total_acceleration)

    return accelerations


def n_body_simulation(bodies, dt, G=G):
    """
    Advance an N-body gravitational simulation by dt seconds
    using kick-drift-kick leapfrog integration.
    """
    if dt <= 0:
        raise ValueError("dt must be positive.")

    if len(bodies) < 2:
        return

    # 1. Calculate acceleration at the beginning of the timestep.
    accelerations = calculate_accelerations(bodies, G)

    # 2. First half-kick: advance velocities by half a timestep.
    for i, body in enumerate(bodies):
        body.velocity += 0.5 * accelerations[i] * dt

    # 3. Drift: update all positions using half-step velocities.
    for body in bodies:
        body.position += body.velocity * dt

    # 4. Calculate acceleration at the new positions.
    new_accelerations = calculate_accelerations(bodies, G)

    # 5. Second half-kick: complete the velocity update.
    for i, body in enumerate(bodies):
        body.velocity += 0.5 * new_accelerations[i] * dt
