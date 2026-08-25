_This project has been created as part of the 42 curriculum by pabdalla and gbitar_

# A-Maze-ing - Maze Generator

## Description

A Python maze generator that reads a configuration file, builds a valid randomly generated maze, and writes it to an output file using a hexadecimal wall encoding. The project also provides a visual representation of the maze via terminal ASCII art  with interactive controls for re-generation, path show/hide, and color changes. The maze always embeds a visible "42" pattern made of fully closed cells.

---

## Instructions

### Running the program
```bash
python3 a_maze_ing.py config.txt
```

### Makefile targets
```bash
make install      # Install project dependencies
make run          # Run the main script
make debug        # Run with Python's built-in debugger (pdb)
make clean        # Remove __pycache__, .mypy_cache, and other temp files
make lint         # Run flake8 and mypy with strict-ish flags
make lint-strict  # Run flake8 and mypy --strict
```

### Checking code standards
```bash
flake8 .    # style linter
mypy .      # type checker
```

---

## Configuration File Format

The configuration file uses one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Generate a perfect maze (one unique path) | `PERFECT=True` |

Optional key `SEED` may also be added for reproducibilit.

A default `config.txt` is provided at the root of the repository.

---

## Output File Format

Each cell is written as a single hexadecimal digit encoding which of its 4 walls are closed:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A closed wall sets its bit to `1`; open means `0`. Example: `A` (binary `1010`) means East and West walls are closed.

---

## Visual Representation

The program displays the maze interactively. At minimum the following user interactions are available:

- **Re-generate** a new maze
- **Show/Hide** the shortest path from entry to exit
- **Change** maze wall colours
- **Quit**

---

## Maze Generation Algorithm

**Algorithm chosen:** Recursive Backtracker (DFS-based)

**Why:** The recursive backtracker works by starting from the entry cell and carving passages into unvisited neighbours, backtracking when it hits a dead end. This naturally produces mazes with long, winding corridors and relatively few short dead ends — which makes the "42" pattern easier to embed cleanly without disrupting connectivity. It also guarantees full connectivity by construction, making the PERFECT=True mode trivial to satisfy: the carving process itself is a depth-first spanning tree traversal, so every generated maze is perfect by default. Disabling perfect mode just requires adding a post-processing step to knock down a controlled number of extra walls.

---

## Reusable Module (`mazegen`)

The maze generation logic is encapsulated in a standalone `MazeGenerator` class, packaged as an installable Python wheel at the root of the repository (`mazegen-*.whl` / `mazegen-*.tar.gz`).

### Installing the package
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage
```python
from mazegen import MazeGenerator

config: dict[str, Any] = {
    "WIDTH": 30,
    "HEIGHT": 20,
    "SEED": 1337,
    "PERFECT": False,
    "ENTRY": (0, 0),
    "EXIT": (19, 29),
}
gen = MazeGenerator(config)
gen.generate()
```

To rebuild the package from source:
```bash
pip install build
python -m build
```

---

## Concepts Covered

- Maze generation as a practical application of **graph theory** and **spanning trees**
- **Recursive backtracking** / DFS for perfect maze generation
- **Bitmask wall encoding** using hexadecimal digits (N/E/S/W per cell)
- **BFS** for computing the shortest path between entry and exit
- **Configuration file parsing** with graceful error handling
- **Terminal ASCII rendering**
- **Reusable Python packaging** with `pyproject.toml` and pip-installable wheels
- **Type hints**, **docstrings** (PEP 257), and **flake8 / mypy** compliance

---

## Key Python Concepts

### Cell Wall Encoding
Each cell is stored as an integer 0–15. Individual walls are tested and set via bitwise operations — e.g., `cell & 1` checks the North wall. This compact representation maps directly to the hex output format.

### Graph Connectivity
A valid maze has no isolated cells: every cell is reachable from every other cell. This is equivalent to the generated structure being a spanning tree (for perfect mazes) or a connected graph (for imperfect ones). Coherence between neighbours is enforced — if cell A has an East wall, cell B to its right must have a West wall.

### Pathfinding
The shortest path is found with BFS (unweighted grid) and encoded as a sequence of cardinal moves (`N`, `E`, `S`, `W`) appended to the output file.

### Packaging
The `MazeGenerator` class lives in a standalone module with a `pyproject.toml`. Running `python -m build` produces a `.whl` and a `.tar.gz` that can be installed via `pip install` in any virtualenv.

---

**AI usage:** Claude was used to help draft this README and to clarify the bitmask encoding scheme. All code was written and reviewed manually.

---

## Team & Project Management

| Member | Role |
|--------|------|
| pabdalla | full implementation |
| gbitar | full implementation |

---