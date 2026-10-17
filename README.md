# Orbital Lab

A small 2D solar system simulator built with Python. It simulates the Sun and eight planets interacting through gravity, with an interactive view of their orbits.

I built this project to explore gravitational physics and numerical simulation while making something I could actually see and interact with.

## Features

- Simulates the Sun and eight planets using Newtonian gravity
- Uses N-body calculations, so planets can influence each other's motion
- Uses kick-drift-kick leapfrog integration to update the simulation
- Displays orbital trails
- Lets you change Earth's initial orbital speed and see how its trajectory changes
- Includes camera controls, zooming, pausing, and simulation speed adjustment

## Built with

- Python
- NumPy
- Pygame

## Getting started

You'll need Python and Git installed.

**1. Clone the repository**

```bash
git clone YOUR_REPOSITORY_URL
cd orbital-lab
```

Replace `YOUR_REPOSITORY_URL` with the URL of this repository. If your folder has a different name, use that instead.

**2. Install the dependencies**

```bash
pip install numpy pygame
```

**3. Run the simulation**

```bash
python visualization.py
```

## Controls

| Key | Action |
|---|---|
| `Space` | Pause / resume |
| `[` / `]` | Decrease / increase simulation speed |
| `Up` / `Down` | Increase / decrease Earth's initial orbital speed |
| `R` | Reset the simulation |
| `C` | Reset the camera |
| Mouse wheel | Zoom in / out |
| Middle mouse button + drag | Move the camera |

## How it works

Each body has a mass, position, and velocity. The simulation calculates the gravitational acceleration acting on each body from the others, then updates their velocities and positions over time.

The simulation uses leapfrog integration, which is generally better suited to long-term orbital simulations than basic Euler integration.

The model is simplified: it uses a 2D plane, idealized initial conditions, and a fixed timestep. It isn't intended to reproduce the solar system's exact positions at a given date.

## Project structure

- `physics.py` — Body class, gravitational calculations, and integration
- `simulation.py` — Planet data, initial conditions, and simulation controls
- `visualization.py` — Pygame window, rendering, trails, and user input

## Video


https://github.com/user-attachments/assets/064afbea-9b61-419e-a3e6-1b8c8f055147



---

Built as a personal project while learning Python and computer science.
