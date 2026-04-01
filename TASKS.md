# A-Maze-ing — Team Task Distribution
> **Project:** A-Maze-ing | **Version:** 1.3 | **Language:** Python 3.10+
> **Goal:** Build a maze generator that reads a config file, generates a maze, writes it in hex format, and displays it visually.

---

## ⚙️ Shared Before You Start (Both do this together — 15 min)

1. Agree on the **MazeGenerator interface** (method names, return types) — see the Interface Contract section below.
2. Create the Git repo and push the initial structure.
3. Each person works in their own branch and merges when ready.

---

## 🔵 Person 1 — Maze Generator + Package

> **Your job:** The core maze *structure* — the generation algorithm, config parsing, and the reusable pip package. You do NOT produce the solution path or the output file — that's Person 2.
> **You do NOT need Person 2's code to do your work.**

---

### 1. Project Setup
- [ ] Create the following file/folder structure:
  ```
  /
  ├── a_maze_ing.py          ← (Person 2 owns this)
  ├── config.txt             ← YOU create the default one
  ├── Makefile               ← YOU own this
  ├── .gitignore             ← YOU create this
  ├── mazegen/
  │   ├── __init__.py
  │   ├── generator.py       ← YOUR main module
  │   └── config.py          ← YOUR config parser
  ├── pyproject.toml         ← YOU own this (for pip package)
  └── mazegen-X.X.X-py3-none-any.whl  ← YOU build this
  ```
- [ ] Create `.gitignore` excluding: `__pycache__/`, `.mypy_cache/`, `*.pyc`, `venv/`, `.env`, `dist/`, `*.egg-info/`

---

### 2. Configuration File Parser

**File:** `mazegen/config.py` (or inside `generator.py`)

- [ ] Parse a plain text config file with `KEY=VALUE` format
- [ ] Ignore lines starting with `#`
- [ ] Support these **mandatory keys**:

| Key | Type | Example |
|-----|------|---------|
| `WIDTH` | int | `WIDTH=20` |
| `HEIGHT` | int | `HEIGHT=15` |
| `ENTRY` | tuple (x,y) | `ENTRY=0,0` |
| `EXIT` | tuple (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | str | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | `PERFECT=True` |

- [ ] Optional keys you should support: `SEED` (int), `ALGORITHM` (str)
- [ ] Handle all errors gracefully: file not found, bad syntax, missing keys, invalid values → print a clear error message, never crash
- [ ] Create the default `config.txt` at the repo root

---

### 3. Maze Generator Class

**File:** `mazegen/generator.py`

This is the **core of the project**. Implement a `MazeGenerator` class.

#### 3.1 Class Interface (stick to this so Person 2 can use it)

```python
class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int | None = None,
                 perfect: bool = True, entry: tuple[int,int] = (0,0),
                 exit: tuple[int,int] | None = None) -> None: ...

    def generate(self) -> None:
        """Generate the maze. Call before accessing any maze data."""

    @property
    def grid(self) -> list[list[int]]:
        """2D grid of hex wall values (0–15). grid[row][col]."""

    @property
    def forty_two_cells(self) -> set[tuple[int, int]]:
        """Set of (col, row) coordinates occupied by the '42' pattern."""

    @property
    def entry(self) -> tuple[int, int]: ...

    @property
    def exit(self) -> tuple[int, int]: ...

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """direction: 'N', 'E', 'S', 'W'. Returns True if wall is closed."""
```

> ⚠️ Note: `MazeGenerator` does **NOT** compute the solution path. That is Person 2's job (`solver.py`). Person 1 only exposes the raw grid and the set of blocked '42' cells.

#### 3.2 Wall Encoding (hex per cell)

Each cell is one hex digit (0–F) encoding which walls are **closed** (bit = 1):

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

Example: `0x3` = `0011b` → North and East walls closed. `0xA` = `1010b` → East and West closed.

#### 3.3 Maze Generation Algorithm

- [ ] Choose **one** algorithm (recommended: **Recursive Backtracker / DFS** — easiest, produces nice mazes). Prim's or Kruskal's also accepted.
- [ ] The algorithm must use the provided **seed** (`random.seed(seed)`) for reproducibility
- [ ] If `PERFECT=True`, ensure exactly **one path** between any two cells (spanning tree = perfect maze)
- [ ] If `PERFECT=False`, you can remove extra walls to create loops

#### 3.4 Maze Validity Rules (all mandatory)

- [ ] Entry and exit are different, inside bounds
- [ ] **No isolated cells** — every cell is reachable from entry
- [ ] **Wall coherence:** if cell A has an East wall, cell B (to its East) must have a West wall — they must agree
- [ ] **No large open areas:** corridors cannot be wider than 2 cells. No 3×3 (or larger) fully open area allowed
- [ ] External border walls must always be closed (except at entry/exit)

#### 3.5 The "42" Pattern

- [ ] Embed a visible **"42"** shape in the maze made of **fully closed cells** (all 4 walls = `0xF`)
- [ ] The pattern must be recognizable when the maze is visualized
- [ ] If the maze is too small to fit "42", print an error message and skip the pattern
- [ ] Expose the coordinates of these cells via the `forty_two_cells` property so Person 2's solver can treat them as impassable

> 🚫 **Do NOT implement BFS or path-finding here.** That belongs to Person 2's `solver.py`.

---

> 🚫 **Output file writing is Person 2's responsibility** (they own the solution path, so they assemble the complete output). See Person 2 → Section 3.

---

### 5. Makefile

**File:** `Makefile` at repo root

```makefile
install:
    pip install -r requirements.txt   # or: uv pip install .

run:
    python3 a_maze_ing.py config.txt

debug:
    python3 -m pdb a_maze_ing.py config.txt

clean:
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type d -name .mypy_cache -exec rm -rf {} +
    find . -name "*.pyc" -delete

lint:
    flake8 .
    mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
           --disallow-untyped-defs --check-untyped-defs

lint-strict:
    flake8 .
    mypy . --strict
```

---

### 6. Python Package (mazegen pip package)

**File:** `pyproject.toml` at repo root

- [ ] Create a proper `pyproject.toml`:
  ```toml
  [build-system]
  requires = ["setuptools", "wheel"]
  build-backend = "setuptools.backends.legacy:build"

  [project]
  name = "mazegen-yourlogin"
  version = "1.0.0"
  description = "Reusable maze generator module"
  requires-python = ">=3.10"
  ```
- [ ] Build the package:
  ```bash
  pip install build
  python -m build
  ```
  This generates: `dist/mazegen-1.0.0-py3-none-any.whl` and `dist/mazegen-1.0.0.tar.gz`
- [ ] **Copy** the `.whl` (or `.tar.gz`) to the **root of the repo** (evaluators will install it)
- [ ] Write a short **module documentation** (can be in `mazegen/README_module.md`):
  - How to instantiate and use `MazeGenerator` with a basic example
  - How to pass custom parameters (size, seed, perfect)
  - How to access the grid and solution

#### Module doc example to include:
```python
from mazegen.generator import MazeGenerator

mg = MazeGenerator(width=20, height=15, seed=42, perfect=True,
                   entry=(0,0), exit=(19,14))
mg.generate()

grid = mg.grid          # list[list[int]]
path = mg.solution      # list[str] e.g. ['E','E','S',...]
print(mg.has_wall(0, 0, 'N'))  # True
```

---

### 7. Type Hints & Code Quality

- [ ] All functions/methods must have **type hints** for parameters and return types
- [ ] All classes and functions must have **docstrings** (PEP 257 / Google style)
- [ ] Code must pass `flake8` with no errors
- [ ] Code must pass `mypy` with the flags in the Makefile lint rule

---

### ✅ Person 1 Deliverables Checklist

- [ ] `mazegen/generator.py` — MazeGenerator class with full generation algorithm
- [ ] `mazegen/config.py` — Config file parser
- [ ] `config.txt` — Default config file
- [ ] `Makefile`
- [ ] `.gitignore`
- [ ] `pyproject.toml` + built `.whl` at repo root
- [ ] Module documentation (with example code)
- [ ] All code: type hints + docstrings + flake8/mypy clean

---
---

## 🟠 Person 2 — Solver + Output File + Display + Main Entry + README

> **Your job:** Everything that happens *after* the maze is generated — solving it (BFS), writing the output file, displaying it visually, and documenting the project.
> **You do NOT need Person 1's final code** — use the interface contract below to mock the generator while developing.

---

### Interface Contract (mock this while Person 1 finishes)

While waiting for Person 1, create a simple **stub** to develop against:

```python
# mock_generator.py — DELETE before final submission
class MazeGenerator:
    def __init__(self, width: int, height: int, **kwargs) -> None:
        self.width = width
        self.height = height
        self._grid = [[0b0101] * width for _ in range(height)]  # basic corridors
        self._entry = (0, 0)
        self._exit = (width - 1, height - 1)
        self._forty_two_cells: set = set()

    def generate(self) -> None: pass

    @property
    def grid(self) -> list[list[int]]: return self._grid

    @property
    def forty_two_cells(self) -> set: return self._forty_two_cells

    @property
    def entry(self) -> tuple[int, int]: return self._entry

    @property
    def exit(self) -> tuple[int, int]: return self._exit

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        bit = {'N': 0, 'E': 1, 'S': 2, 'W': 3}[direction]
        return bool((self._grid[y][x] >> bit) & 1)
```

Replace `from mock_generator import MazeGenerator` with `from mazegen.generator import MazeGenerator` when Person 1 is ready.

---

### 1. Main Entry Point

**File:** `a_maze_ing.py` ← **you must use this exact name**

- [ ] Accept exactly **one argument**: `python3 a_maze_ing.py config.txt`
- [ ] Show a clear usage message if no argument or wrong number of args
- [ ] Call Person 1's config parser to load the config
- [ ] Instantiate `MazeGenerator` with the config values and call `generate()`
- [ ] Call **your own** `MazeSolver` to compute the shortest path
- [ ] Call **your own** `write_maze()` to save the output file
- [ ] Launch the visual display
- [ ] Handle all errors gracefully — never crash, always show a clear message

```python
# Skeleton
import sys
from mazegen.config import parse_config
from mazegen.generator import MazeGenerator
from solver import MazeSolver       # YOUR file
from writer import write_maze       # YOUR file
from display import MazeDisplay     # YOUR file

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    config = parse_config(sys.argv[1])
    mg = MazeGenerator(**config)
    mg.generate()
    solver = MazeSolver(mg)
    solution = solver.solve()         # list[str] of directions
    write_maze(mg, solution, config['OUTPUT_FILE'])
    display = MazeDisplay(mg, solution)
    display.run()

if __name__ == '__main__':
    main()
```

---

### 2. Terminal ASCII Display

**File:** `display.py` (or `mazegen_display/terminal.py`)

This is the **main display mode**. Render the maze using ASCII characters in the terminal.

#### 2.1 Rendering Logic

Standard ASCII maze rendering uses a grid of characters. A common approach:

- Each cell = a 2×2 or 3×3 block of characters
- Walls rendered as `█`, `|`, `-`, `+` or similar
- Passage (open wall) = space

**Recommended simple approach** (cell = 3×3 block):
```
+--+--+
|     |
+  +--+
|  |
+--+
```
- `+` at corners
- `--` (or `  `) for top/bottom wall (closed/open)
- `|` (or ` `) for left/right wall (closed/open)

- [ ] Render the full maze to terminal on startup
- [ ] Show the **entry** cell visually (e.g., label `S` or `⬛` or colored)
- [ ] Show the **exit** cell visually (e.g., label `E`)
- [ ] The "42" pattern cells should be visually distinct (e.g., filled `█`)

#### 2.2 Shortest Path Display (show/hide)

- [ ] The path can be **toggled on/off** by user input (key press)
- [ ] When shown, the path cells are highlighted (e.g., with `.` or `*` or a different color using ANSI codes)
- [ ] When hidden, the maze is displayed normally

**ANSI colors for terminal** (no extra library needed):
```python
RED   = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'
print(f"{GREEN}*{RESET}")
```

#### 2.3 User Interactions (mandatory)

Implement a simple input loop. After drawing the maze, wait for a key and act:

| Key | Action |
|-----|--------|
| `r` | Re-generate a new maze (new random seed), re-solve, and redraw |
| `p` | Toggle show/hide shortest path |
| `c` | Cycle through wall color schemes |
| `q` | Quit |

- [ ] `r` — Re-generate: create a new `MazeGenerator` with a new random seed, call `generate()`, then re-run `MazeSolver`, then redraw
- [ ] `p` — Toggle path visibility
- [ ] `c` — Change wall colors (at least 3 different color schemes using ANSI codes)
- [ ] `q` — Exit the program cleanly

#### 2.4 Optional: "42" pattern color

- [ ] If you want a bonus point: add a key (e.g., `4`) to toggle a specific color for the "42" pattern cells (use `mg.forty_two_cells` to know which cells to color)

---

### 3. Maze Solver

**File:** `solver.py`

This is your own BFS implementation. It takes the generator's output and finds the shortest path.

```python
from collections import deque

class MazeSolver:
    def __init__(self, maze: MazeGenerator) -> None:
        """Takes a generated MazeGenerator instance."""
        self.maze = maze

    def solve(self) -> list[str]:
        """
        BFS from maze.entry to maze.exit.
        Returns shortest path as list of directions: ['N','E','S','W',...].
        Raises ValueError if no path exists.
        Treats forty_two_cells as impassable.
        """
        ...
```

#### BFS implementation guide:
- Use `collections.deque` for the queue
- Track visited cells with a `set`
- Skip cells in `maze.forty_two_cells`
- Use `maze.has_wall(x, y, direction)` to check if you can move in a direction
- Reconstruct path by tracking parent cell + direction taken
- Direction offsets: `N=(0,-1)`, `E=(1,0)`, `S=(0,1)`, `W=(-1,0)`
- If no path found, raise a clear `ValueError` with a message

---

### 4. Output File Writer

**File:** `writer.py`

You own this because the output requires the solution path (which you compute).

```python
def write_maze(maze: MazeGenerator, solution: list[str], output_path: str) -> None:
    """Write the maze grid + entry + exit + path to output_path."""
```

- [ ] Write hex grid row by row (one row per line, digits with no spaces, lowercase or uppercase)
- [ ] After the grid, write an **empty line**
- [ ] Then write entry coordinates: `0,0`
- [ ] Then write exit coordinates: `19,14`
- [ ] Then write the path: `E E S S N E ...` (space-separated directions)
- [ ] All lines end with `\n`
- [ ] Handle file write errors gracefully

**Full format example:**
```
FE3A2B...
C7B24F...
...

0,0
19,14
E E S S E N E
```

---

### 5. Display Class Structure

```python
class MazeDisplay:
    def __init__(self, maze: MazeGenerator, solution: list[str]) -> None:
        self.maze = maze
        self.solution = solution
        self.show_path = False
        self.color_scheme = 0

    def render(self) -> None:
        """Clear screen and draw the maze."""

    def run(self) -> None:
        """Main interaction loop."""

    def _draw_cell(self, x: int, y: int) -> str:
        """Return ASCII representation for one cell."""

    def _change_color(self) -> None:
        """Cycle to next color scheme."""

    def _path_cells(self) -> set[tuple[int, int]]:
        """Convert solution directions into a set of (x,y) coordinates."""
```

- [ ] All methods have type hints and docstrings
- [ ] Code passes `flake8` and `mypy`

---

### 6. README.md

**File:** `README.md` at repo root

This is the **project-facing documentation**. It must contain:

#### 4.1 Required First Line
```markdown
*This project has been created as part of the 42 curriculum by <login1>, <login2>.*
```

#### 4.2 Description Section
- What the project does
- Its goal (maze generation, visualization)
- Brief technical overview

#### 4.3 Instructions Section
```markdown
## Instructions

### Installation
make install

### Run
make run
# or
python3 a_maze_ing.py config.txt

### Debug
make debug

### Lint
make lint
```

- Include how to install the mazegen package:
  ```bash
  pip install mazegen-X.X.X-py3-none-any.whl
  ```

#### 4.4 Config File Format (mandatory in README)
Document the full config file format:
```
# This is a comment
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```
Explain each key.

#### 4.5 Algorithm Section (mandatory in README)
- Name of the algorithm used
- Why it was chosen
- Brief description of how it works

#### 4.6 Reusable Module Section (mandatory in README)
Copy/paste the module documentation from Person 1's doc (or write it together):
- How to install the package
- How to use `MazeGenerator`
- Code example

#### 4.7 Team & Project Management Section (mandatory in README)
```markdown
## Team & Project Management

### Roles
- **login1**: [Person 1 role — core engine, package]
- **login2**: [Person 2 role — display, main, README]

### Planning
- Week 1: ...
- Week 2: ...

### What worked well
- ...

### What could be improved
- ...

### Tools used
- VS Code, Git, mypy, flake8, ...
```

#### 4.8 Resources Section (mandatory in README)
Include links to:
- Maze generation algorithms (e.g., Wikipedia — Maze generation algorithm)
- Recursive backtracker explanation
- Python `random` module docs
- `mypy` docs
- How AI was used (which tasks, which parts)

---

### ✅ Person 2 Deliverables Checklist

- [ ] `solver.py` — BFS maze solver (`MazeSolver` class)
- [ ] `writer.py` — Output file writer (`write_maze` function)
- [ ] `a_maze_ing.py` — Main entry point with arg handling + orchestration
- [ ] `display.py` — Full terminal ASCII display with all interactions
- [ ] `README.md` — Complete with all mandatory sections
- [ ] Type hints on all functions
- [ ] Docstrings on all classes/functions
- [ ] Code passes `flake8` and `mypy`

---

## 🟢 Bonus Tasks (either person can do these)

| Bonus | Who |
|-------|-----|
| Support multiple algorithms (Prim's, Kruskal's, DFS) | Person 1 |
| Animation during maze generation (step-by-step rendering) | Person 2 |
| MLX graphical display (instead of or alongside terminal) | Person 2 |
| `SEED` key in config for reproducibility | Person 1 (already in core) |
| Color for "42" pattern toggle | Person 2 |

---

## 🔗 Interface Contract (the bridge between both)

> This is what Person 1 **must expose** and Person 2 **must consume**. Agree on this on day 1.

| What | Owner | Exposed as |
|------|-------|------------|
| Config parser | Person 1 | `from mazegen.config import parse_config` → `dict` |
| Maze generation | Person 1 | `MazeGenerator` class in `mazegen.generator` |
| Raw grid | Person 1 | `mg.grid` → `list[list[int]]` |
| Wall query | Person 1 | `mg.has_wall(x, y, direction)` → `bool` |
| "42" cell coords | Person 1 | `mg.forty_two_cells` → `set[tuple[int,int]]` |
| BFS solver | **Person 2** | `solver.py` → `MazeSolver(mg).solve()` → `list[str]` |
| Output file | **Person 2** | `writer.py` → `write_maze(mg, solution, path)` |
| Display | **Person 2** | `display.py` → `MazeDisplay(mg, solution).run()` |

```python
# Full API summary:

# --- Person 1 provides ---
from mazegen.config import parse_config      # parse_config(filepath) -> dict
from mazegen.generator import MazeGenerator

# MazeGenerator(width, height, seed, perfect, entry, exit)
# .generate() -> None
# .grid -> list[list[int]]          (row-major: grid[row][col])
# .forty_two_cells -> set[tuple]    (set of (col, row) blocked cells)
# .entry -> tuple[int,int]
# .exit  -> tuple[int,int]
# .width -> int
# .height -> int
# .has_wall(x, y, direction) -> bool   ('N'/'E'/'S'/'W')

# --- Person 2 provides ---
from solver import MazeSolver                # MazeSolver(mg).solve() -> list[str]
from writer import write_maze                # write_maze(mg, solution, output_path) -> None
from display import MazeDisplay              # MazeDisplay(mg, solution).run() -> None
```

---

## 📋 Final Submission Checklist (both review together)

- [ ] `a_maze_ing.py` runs with `python3 a_maze_ing.py config.txt`
- [ ] Default `config.txt` is present in the repo
- [ ] Output file is generated with correct hex format + path + entry/exit
- [ ] Maze validates: coherent walls, no isolated cells, no 3×3 open areas
- [ ] "42" pattern visible in terminal rendering
- [ ] Perfect maze works (single path between entry and exit when `PERFECT=True`)
- [ ] All 4 user interactions work: `r`, `p`, `c`, `q`
- [ ] `make install`, `make run`, `make lint`, `make clean`, `make debug` all work
- [ ] `.whl` or `.tar.gz` package is at repo root and installable
- [ ] `README.md` has all mandatory sections
- [ ] All code: type hints + docstrings + flake8 clean + mypy clean
- [ ] Git repo has clean history with meaningful commits
