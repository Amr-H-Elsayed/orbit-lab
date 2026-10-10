import numpy as np

G = 6.67430e-11

class Body:
    def __init__(self, name: str,mass: float, position: list, velocity: list):
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype = float)
        self.velocity = np.array(velocity, dtype = float)

def distance_between(body_a, body_b):
    difference = body_b.position - body_a.position
    distance = np.linalg.norm(difference)
    return distance

def acceleration_from(source, target, G = G):
    # vector from source to target
    r_vector = target.position - source.position
    r = np.linalg.norm(r_vector)
    if r == 0:
        return np.array([0.00, 0.00])
    
    # a = -G * M * (r_vector / r^3)
    acceleration = -G * source.mass * (r_vector/r**3)
    return acceleration

# N-Body simulation
def n_body_simulation(bodies, dt, G=G):
    # dt is delta time btw 
    accelerations = []
    for i, body_a in enumerate(bodies):
        total_acceleration = np.array([0.0, 0.0])
        for j, body_b in enumerate(bodies):
            if i != j:
                total_acceleration += acceleration_from(body_b, body_a, G=G)
        accelerations.append(total_acceleration)
    
    # Update velocities and positions
    for i, body in enumerate(bodies):
        body.velocity += accelerations[i] * dt
        body.position += body.velocity * dt
