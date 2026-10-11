from physics import Body, n_body_simulation

sun = Body(name="Sun", mass=1.989e30, position=[0, 0], velocity=[0, 0])
earth = Body(name="Earth", mass=5.972e24, position=[1.496e11, 0], velocity=[0, 29784.8])

bodies = [sun, earth]

dt = 3600         # Time step size: 3,600 seconds = 1 hour
number_of_steps = 365 * 24  # 365 days * 24 hours = 8,760 hours

print(f"[initial print for test] Earth Position: {earth.position}, Velocity: {earth.velocity}")
print(f"[initial print for test] Sun Position: {sun.position}, Velocity: {sun.velocity}")

for step in range(number_of_steps):
    n_body_simulation(bodies, dt)

    if (step + 1) % (180 * 24) == 0:  # Print every 180 days
        print(f"Day {(step + 1) * dt / 86400:.0f}: Earth Position: {earth.position}, Velocity: {earth.velocity}")
        print(f"Day {(step + 1) * dt / 86400:.0f}: Sun Position: {sun.position}, Velocity: {sun.velocity}")