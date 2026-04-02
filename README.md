# Fly-In

This project has been developed as part of the **42 curriculum** by **ayhammou**.

---

## Description

**Fly-In** is a logistics and traffic management simulation designed to coordinate the movement of multiple drones across a network of interconnected zones.

The main objective is to **transport all drones from a starting hub to a destination zone**, while strictly respecting several environmental constraints:

- **Zone Capacities** → Maximum number of drones allowed in a zone at the same time  
- **Link Capacities** → Limited number of drones that can traverse a connection per turn  
- **Zone Types**:
  - 🔶 **Priority Zones** → Grant movement priority to drones  
  - 🔴 **Restricted Zones** → Impose mandatory waiting time upon entry  

The project is composed of three main components:

- A **robust parsing engine**
- A **discrete-time simulation engine**
- An **interactive graphical interface (GUI)**

---

## Instructions

### Prerequisites

- Python **3.10+**
- **PyQt6** (for the graphical interface)

---

### Installation

Clone the repository:

git clone <repository_url>
cd fly_in

To ensure a clean and isolated environment, it is recommended to use a virtual environment.

### Create a Virtual Environment

python3 -m venv test-env
source test-env/bin/activate

### Algorithm & Implementation Strategy

Movement & Constraint Logic
At each discrete time step (turn), the engine performs the following:

Priority Sorting: Drones located in Priority Zones are moved to the front of the processing queue to simulate "right-of-way."

Validation: Before any move, the engine checks both the target zone capacity and the link throughput for the current turn.

Wait States: When entering a Restricted Zone, a wait_time is applied to the drone, forcing it to remain idle for one turn to simulate bottleneck management.

Deadlock Resilience: The engine is designed to "yield" its state even when drones are blocked, allowing the user to observe the congestion in the GUI instead of the program crashing.

### Visual Representation Features

The PyQt6 Graphical Interface was developed to transform raw data into an interactive mission control dashboard:

Real-time Statistics: Each zone displays a dynamic text overlay showing the number of drones present and their specific IDs.

History Replay:
Press 'D' to advance to the next turn.
Press 'Q' to go back in time and review previous moves.

HUD (Heads-Up Display): A permanent turn counter is displayed in the top-left corner to track simulation progress.

## Resources & AI Disclosure

References
PyQt6 Documentation: For building the graphics scene and event handling.

Python Generators: Used to implement the turn-by-turn communication between the engine and the GUI. https://www.google.com/search?q=https://docs.python.org/3/howto/functional.html%23generators

BFS Algorithm - Wikipedia: For pathfinding logic.

### AI Usage Disclosure

Artificial Intelligence (Gemini) was used as a technical collaborator during the development of this project for the following tasks:

GUI Mathematics: Assisting in the formulas for automatic map scaling and coordinate centering.

Architecture: Guidance on decoupling the simulation logic from the PyQt6 rendering loop.

Refactoring: Optimizing the update_display method to handle real-time ID tracking and history management.

Debugging: Identifying the logic error that caused simulation "deadlocks" in circular map files.

### Controls Summary

Key, Action

D, Forward - Advance the simulation by one turn.

Q, Backward - Return to the previous state in history.





