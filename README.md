# 🧩 KenKen Game & Solver (Python)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green?style=flat-square)
![Algorithm](https://img.shields.io/badge/Algorithm-Backtracking-orange?style=flat-square)

A fully functional **KenKen Puzzle Generator and Solver** developed in Python. This project demonstrates the application of **Data Structures and Algorithms** (specifically Backtracking and Recursion) to solve constraint satisfaction problems (CSPs).

Developed as a final project for the **Data Structures & Algorithms II** course at INTEC.

## 🚀 Key Features

* **Dynamic Board Generation:** Creates valid 5x5 or 7x7 puzzles on the fly using randomized Latin Square logic.
* **Smart Solver (AI):** Includes an "Auto-Solve" feature powered by a **Backtracking Algorithm** that solves any valid board in milliseconds.
* **Interactive GUI:** Built with **Tkinter** for a clean, responsive user experience.
* **Real-time Validation:** Prevents invalid inputs and validates mathematical constraints (cages) instantly.
* **Math Logic:** Handles complex grouping logic with operations (+, -, *, /).

## 🧠 Algorithmic Logic

The core of this project is the **Backtracking Algorithm** used in two stages:
1.  **Generation:** To create a valid Latin Square (no repeated numbers in rows/cols) before applying the "cage" constraints.
2.  **Solving:** To recursively find the solution by trying numbers and "backtracking" when a constraint is violated.

```python
# Snippet of the backtracking logic
def solve(row, col):
    if row == n: return True
    # ... logic to check constraints ...
    if valid:
        if solve(next_row, next_col): return True
        grid[row][col] = 0 # Backtrack

==================================================================================================================
## 🛠️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/angemio/KenKen-Solver.git](https://github.com/angemio/KenKen-Solver.git)
   cd KenKen-Solver

2. **Run the game:**
    
    No external libraries required
```bash
python kenken.py
==================================================================================================================
📂 Project Structure

kenken.py: Contains the main logic, UI rendering, and the Backtracking engine.

README.md: Project documentation.
==================================================================================================================
👤 Author 

Angel De la Rosa

Software Engineering Student @ INTEC
==================================================================================================================