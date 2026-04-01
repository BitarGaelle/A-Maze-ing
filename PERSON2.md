# 🟠 Person 2 — Solver + Output File + Display + README
> **Project:** A-Maze-ing | **Language:** Python 3.10+
>
> **Your job:** Everything after the maze is generated — solve it (BFS), write the output file, display it visually, and document the project.
> You do **NOT** need Person 1's final code to start — use the mock stub below while they work.

---

## 📁 Files You Own

```
/
├── a_maze_ing.py       ← main entry point (EXACT name required)
├── solver.py           ← BFS MazeSolver class
├── writer.py           ← output file writer
├── display.py          ← terminal ASCII display
└── README.md           ← project documentation
```

---

## 🧪 Mock Stub — Use While Person 1 Is Working

Create this file at repo root. It mimics Person 1's `MazeGenerator` so you can build and test everything independently.

**File:** `mock_generator.py` — **DELETE before final submission**

```python
class MazeGenerator:
    """Stub for MazeGenerator — replace with real import when ready."""

    def __init__(self, width: int, height: int, **kwargs) -> None:
        self.width = width
        self.height = height
        # Simple open corridors: North+South open (bits 0,2 = 0), East+West closed (bits 1,3 = 1)
        self._grid = [[0b0101] * width for _ in range(height)]
        self._entry = (0, 0)
        self._exit = (width - 1, height - 1)
        self._forty_two_cells: set[tuple[int, int]] = set()

    def generate(self) -> None:
        pass

    @property
    def grid(self) -> list[list[int]]:
        return self._grid

    @property
    def forty_two_cells(self) -> set[tuple[int, int]]:
        return self._forty_two_cells

    @property
    def entry(self) -> tuple[int, int]:
        return self._entry

    @property
    def exit(self) -> tuple[int, int]:
        return self._exit

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        bit = {'N': 0, 'E': 1, 'S': 2, 'W': 3}[direction]
        return bool((self._grid[y][x] >> bit) & 1)
```

In all your files, import like this while testing:
```python
from mock_generator import MazeGenerator   # ← temporary
# from mazegen.generator import MazeGenerator  # ← switch to this for final
```

---

## ✅ Task Checklist

---

### 1. BFS Maze Solver

**File:** `solver.py`

This is your most algorithmic task. You implement BFS from entry to exit on Person 1's maze grid.

#### Class Structure

```python
from collections import deque
from mazegen.generator import MazeGenerator


class MazeSolver:
    """Finds the shortest path in a generated maze using BFS."""

    def __init__(self, maze: MazeGenerator) -> None:
        """Takes a fully generated MazeGenerator instance."""
        self.maze = maze

    def solve(self) -> list[str]:
        """
        BFS from maze.entry to maze.exit.

        Returns:
            Shortest path as a list of direction strings e.g. ['E','E','S','N',...].

        Raises:
            ValueError: If no path exists between entry and exit.
        """
        ...
```

#### BFS Step-by-Step

1. Initialize a `deque` with the entry cell: `deque([(entry_x, entry_y)])`
2. Keep a `visited` set: `{(entry_x, entry_y)}`
3. Keep a `parent` dict to reconstruct the path: `{cell: (parent_cell, direction_taken)}`
4. Direction offsets:
   - `'N'` → `(0, -1)` (row decreases)
   - `'E'` → `(1, 0)` (col increases)
   - `'S'` → `(0, 1)` (row increases)
   - `'W'` → `(-1, 0)` (col decreases)
5. For each cell popped from the queue, try all 4 directions:
   - Skip if `maze.has_wall(x, y, direction)` is True
   - Skip if neighbor `(nx, ny)` is in `visited`
   - Skip if neighbor `(nx, ny)` is in `maze.forty_two_cells`
   - Skip if out of bounds
6. When you reach `maze.exit`, backtrack through `parent` to reconstruct the path
7. If the queue empties with no path found → raise `ValueError("No path found between entry and exit")`

#### Path reconstruction

```python
path = []
cell = maze.exit
while cell in parent:
    cell, direction = parent[cell]   # actually: prev_cell, direction = parent[current]
    path.append(direction)
path.reverse()
return path
```

Implement this step carefully — it's easy to get the reconstruction backwards.

- [ ] BFS correctly finds shortest path
- [ ] "42" cells are treated as impassable
- [ ] Raises `ValueError` if no path exists
- [ ] Has type hints and docstring
- [ ] Passes `flake8` and `mypy`

---

### 2. Output File Writer

**File:** `writer.py`

You own this because the output file requires the solution path, which only you compute.

#### Function Signature

```python
def write_maze(maze: MazeGenerator, solution: list[str], output_path: str) -> None:
    """Write the maze grid, entry, exit, and solution path to a file.

    Args:
        maze: A fully generated MazeGenerator instance.
        solution: Shortest path as a list of direction strings.
        output_path: Path to the output file to write.
    """
```

#### Output Format (exact, do not deviate)

```
[hex grid — one row per line, no spaces, uppercase or lowercase]

[entry col,row]
[exit col,row]
[path directions space-separated]
```

**Concrete example (5×3 maze):**
```
FE3AC7
B24F1D
C7B2E3

0,0
4,2
E E S S E N E
```

- [ ] Write each row of `maze.grid` as hex digits on one line, no spaces (use `format(val, 'X')` or `hex(val)[2:].upper()`)
- [ ] Write an **empty line** after the grid
- [ ] Write entry: `f"{maze.entry[0]},{maze.entry[1]}\n"`
- [ ] Write exit: `f"{maze.exit[0]},{maze.exit[1]}\n"`
- [ ] Write solution: `" ".join(solution) + "\n"`
- [ ] Use `with open(output_path, 'w') as f:` (context manager)
- [ ] Handle `IOError`/`OSError` gracefully — print a clear error, don't crash
- [ ] Has type hints and docstring
- [ ] Passes `flake8` and `mypy`

---

### 3. Main Entry Point

**File:** `a_maze_ing.py` ← **this exact filename is required by the subject**

- [ ] Accept **exactly one argument**: `python3 a_maze_ing.py config.txt`
- [ ] If wrong number of args → print usage and exit cleanly
- [ ] Load config via Person 1's `parse_config()`
- [ ] Instantiate `MazeGenerator` and call `.generate()`
- [ ] Run `MazeSolver` to get the solution
- [ ] Call `write_maze()` to write the output file
- [ ] Launch the display
- [ ] Never crash — wrap everything in try/except with clear error messages

```python
#!/usr/bin/env python3
"""A-Maze-ing: Maze generator, solver, and visualizer."""

import sys
from mazegen.config import parse_config
from mazegen.generator import MazeGenerator
from solver import MazeSolver
from writer import write_maze
from display import MazeDisplay


def main() -> None:
    """Main entry point for a_maze_ing."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        mg = MazeGenerator(**config)
        mg.generate()
        solver = MazeSolver(mg)
        solution = solver.solve()
        write_maze(mg, solution, config['OUTPUT_FILE'])
        display = MazeDisplay(mg, solution)
        display.run()
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

### 4. Terminal ASCII Display

**File:** `display.py`

#### 4.1 Class Structure

```python
class MazeDisplay:
    """Terminal ASCII renderer for a generated maze."""

    def __init__(self, maze: MazeGenerator, solution: list[str]) -> None:
        self.maze = maze
        self.solution = solution
        self.show_path: bool = False
        self.color_scheme: int = 0

    def render(self) -> None:
        """Clear screen and draw the full maze."""

    def run(self) -> None:
        """Main interaction loop — wait for keypresses and act."""

    def _draw_cell(self, x: int, y: int) -> str:
        """Return ASCII wall characters for cell at (x, y)."""

    def _change_color(self) -> None:
        """Cycle to the next wall color scheme."""

    def _path_cells(self) -> set[tuple[int, int]]:
        """Convert the solution direction list into a set of (col, row) coordinates."""
```

#### 4.2 Rendering Logic

Use a corner-based approach. For each cell, draw:
- Top-left corner: always `+`
- Top wall: `--` if `has_wall(x, y, 'N')` else `  `
- Left wall: `|` if `has_wall(x, y, 'W')` else ` `
- Cell interior: space (or path marker, or "42" fill)

Build the grid row by row:

```
+--+--+  ←  top walls of row 0
|  |  |  ←  left walls + interior of row 0
+--+  +  ←  top walls of row 1 (= bottom walls of row 0)
|     |
+--+--+
```

- [ ] Show **entry** cell with `S` inside
- [ ] Show **exit** cell with `E` inside
- [ ] "42" cells shown as `██` or `##` (visually filled blocks)
- [ ] Path cells (when shown) use `··` or `**` with a different ANSI color
- [ ] Clear screen before each redraw: `print("\033[2J\033[H", end="")`

#### 4.3 ANSI Colors (no extra library needed)

```python
COLORS = {
    'reset': '\033[0m',
    'wall_white': '\033[37m',
    'wall_cyan': '\033[36m',
    'wall_yellow': '\033[33m',
    'path': '\033[32m',      # green
    'entry': '\033[34m',     # blue
    'exit': '\033[31m',      # red
    'forty_two': '\033[35m', # magenta
}
```

#### 4.4 `_path_cells()` — Converting directions to coordinates

```python
def _path_cells(self) -> set[tuple[int, int]]:
    """Walk the solution from entry and collect all (col, row) visited."""
    offsets = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
    x, y = self.maze.entry
    cells = {(x, y)}
    for direction in self.solution:
        dx, dy = offsets[direction]
        x, y = x + dx, y + dy
        cells.add((x, y))
    return cells
```

#### 4.5 Mandatory User Interactions

Implement a simple `input()` loop after rendering:

| Key | Action |
|-----|--------|
| `r` | Re-generate maze (new random seed), re-solve, redraw |
| `p` | Toggle show/hide shortest path |
| `c` | Cycle through wall color schemes (at least 3) |
| `q` | Quit the program |

```python
def run(self) -> None:
    self.render()
    while True:
        key = input("Command [r/p/c/q]: ").strip().lower()
        if key == 'q':
            break
        elif key == 'r':
            import random
            new_seed = random.randint(0, 999999)
            self.maze = MazeGenerator(
                width=self.maze.width, height=self.maze.height,
                seed=new_seed, perfect=True,
                entry=self.maze.entry, exit=self.maze.exit
            )
            self.maze.generate()
            from solver import MazeSolver
            self.solution = MazeSolver(self.maze).solve()
            self.show_path = False
        elif key == 'p':
            self.show_path = not self.show_path
        elif key == 'c':
            self._change_color()
        self.render()
```

- [ ] `r` — Re-generate + re-solve + redraw
- [ ] `p` — Toggle path
- [ ] `c` — Cycle colors (min 3 schemes)
- [ ] `q` — Exit cleanly

#### 4.6 Optional bonus

- [ ] Add key `4` to toggle a special color for "42" pattern cells
  (use `self.maze.forty_two_cells` to know which cells to color differently)

---

### 5. README.md

**File:** `README.md` at repo root

#### Required Sections (all mandatory)

**Line 1 (exactly this format, italicized):**
```markdown
*This project has been created as part of the 42 curriculum by <login1>, <login2>.*
```

---

**## Description**
- What the project does
- Its goal (maze generation, solving, visualization)
- Brief technical overview (Python, BFS, hex encoding, etc.)

---

**## Instructions**
```markdown
### Installation
make install

### Run
make run
# or directly:
python3 a_maze_ing.py config.txt

### Debug
make debug

### Lint
make lint

### Install the reusable package
pip install mazegen-X.X.X-py3-none-any.whl
```

---

**## Configuration File Format** ← mandatory per subject
```
# A-Maze-ing configuration file
# Lines starting with # are comments

WIDTH=20          # maze width (number of cells)
HEIGHT=15         # maze height
ENTRY=0,0         # entry cell coordinates (col,row)
EXIT=19,14        # exit cell coordinates (col,row)
OUTPUT_FILE=maze.txt  # output file name
PERFECT=True      # True = perfect maze (single path), False = loops allowed
SEED=42           # optional: seed for reproducibility
```
Explain each key in a table.

---

**## Algorithm** ← mandatory per subject
- Name of the algorithm Person 1 used (e.g., Recursive Backtracker / DFS)
- Why it was chosen
- Brief description of how it works
- (Ask Person 1 to fill this in or fill it in together)

---

**## Reusable Module** ← mandatory per subject (copy from Person 1's module doc)

How to install:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

How to use:
```python
from mazegen.generator import MazeGenerator

mg = MazeGenerator(width=20, height=15, seed=42, perfect=True,
                   entry=(0, 0), exit=(19, 14))
mg.generate()

grid = mg.grid                  # list[list[int]]
blocked = mg.forty_two_cells    # set of (col, row)
mg.has_wall(0, 0, 'N')         # True
```

---

**## Team & Project Management** ← mandatory per subject
```markdown
### Roles
- **login1**: Maze generation algorithm, config parser, pip package
- **login2**: BFS solver, output file writer, display, README

### Planning
- Week 1: Setup, interface agreement, parallel development starts
- Week 2: Integration, testing, README

### What worked well
- ...

### What could be improved
- ...

### Tools used
- VS Code, Git, mypy, flake8, pytest, ...
```

---

**## Resources** ← mandatory per subject
Include links to:
- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Python `collections.deque` docs](https://docs.python.org/3/library/collections.html#collections.deque)
- [BFS explanation](https://en.wikipedia.org/wiki/Breadth-first_search)
- [mypy docs](https://mypy.readthedocs.io/)
- **How AI was used**: which parts, which tasks, what prompts were useful

---

### 6. Code Quality (applies to ALL your files)

- [ ] Every function and method has **type hints** for all parameters and return type
- [ ] Every class and function has a **docstring** (Google or NumPy style — PEP 257)
- [ ] Code passes `flake8 .` with no errors
- [ ] Code passes `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs` with no errors
- [ ] Use `try/except` for file operations and resource access
- [ ] Use `with open(...)` for all file reads/writes

---

## 📦 Final Deliverables Checklist

- [ ] `solver.py` — `MazeSolver` class with `solve() -> list[str]`
- [ ] `writer.py` — `write_maze(maze, solution, output_path)` function
- [ ] `a_maze_ing.py` — main entry point (`python3 a_maze_ing.py config.txt`)
- [ ] `display.py` — `MazeDisplay` class with all 4 interactions
- [ ] `README.md` — all 6 mandatory sections filled in
- [ ] `mock_generator.py` **deleted** before submission
- [ ] All code: type hints + docstrings + flake8 clean + mypy clean

---

## 🔗 What You Get From Person 1

This is the full API Person 1 gives you — everything you need:

```python
from mazegen.config import parse_config
# parse_config(filepath: str) -> dict
# Keys: 'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT', optionally 'SEED'

from mazegen.generator import MazeGenerator
# MazeGenerator(width, height, seed, perfect, entry, exit)
# .generate()            -> None                  call this first!
# .grid                  -> list[list[int]]        grid[row][col], values 0–15
# .forty_two_cells       -> set[tuple[int,int]]    (col, row) of blocked "42" cells
# .entry                 -> tuple[int,int]         (col, row)
# .exit                  -> tuple[int,int]         (col, row)
# .width                 -> int
# .height                -> int
# .has_wall(x, y, dir)   -> bool                   'N'/'E'/'S'/'W'
```

> ✅ Once Person 1 pushes `mazegen/`, swap `from mock_generator import MazeGenerator` with `from mazegen.generator import MazeGenerator` everywhere — and you're done integrating.
