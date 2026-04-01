# 🔵 Person 1 — Maze Generator + Package
> **Project:** A-Maze-ing | **Language:** Python 3.10+
>
> **Your job:** Build the core maze *structure* — the generation algorithm, config parsing, and the reusable pip package.
> You do **NOT** write the BFS solver, the output file, or the display. That's Person 2.
> You do **NOT** need Person 2's code at any point.

---

## 📁 Files You Own

```
/
├── config.txt                          ← default config file (YOU create)
├── Makefile                            ← YOU own this
├── .gitignore                          ← YOU create this
├── pyproject.toml                      ← YOU own this
├── mazegen-X.X.X-py3-none-any.whl     ← YOU build and place at root
└── mazegen/
    ├── __init__.py
    ├── generator.py                    ← MazeGenerator class
    └── config.py                       ← config file parser
```

---

## ✅ Task Checklist

### 1. Project Setup

- [ ] Create the folder structure above
- [ ] Create `.gitignore` with at minimum:
  ```
  __pycache__/
  .mypy_cache/
  *.pyc
  venv/
  .env
  dist/
  *.egg-info/
  ```
- [ ] Create default `config.txt` at repo root:
  ```
  # A-Maze-ing default configuration
  WIDTH=20
  HEIGHT=15
  ENTRY=0,0
  EXIT=19,14
  OUTPUT_FILE=maze.txt
  PERFECT=True
  SEED=42
  ```

---

### 2. Configuration File Parser

**File:** `mazegen/config.py`

- [ ] Parse a plain text file with `KEY=VALUE` format (one pair per line)
- [ ] Ignore lines starting with `#` (comments)
- [ ] Support all mandatory keys:

  | Key | Type | Example |
  |-----|------|---------|
  | `WIDTH` | `int` | `WIDTH=20` |
  | `HEIGHT` | `int` | `HEIGHT=15` |
  | `ENTRY` | `tuple[int,int]` | `ENTRY=0,0` |
  | `EXIT` | `tuple[int,int]` | `EXIT=19,14` |
  | `OUTPUT_FILE` | `str` | `OUTPUT_FILE=maze.txt` |
  | `PERFECT` | `bool` | `PERFECT=True` |

- [ ] Support optional keys: `SEED` (int), `ALGORITHM` (str)
- [ ] Return a `dict` with all parsed values
- [ ] Handle all errors gracefully — never crash:
  - File not found → clear message
  - Missing mandatory key → clear message
  - Bad value (e.g. non-int for WIDTH) → clear message

**Function signature:**
```python
def parse_config(filepath: str) -> dict:
    """Parse a KEY=VALUE config file. Returns a dict of settings."""
```

---

### 3. Maze Generator Class

**File:** `mazegen/generator.py`

#### 3.1 Class Interface (Person 2 depends on this — do not change it)

```python
class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int | None = None,
                 perfect: bool = True, entry: tuple[int, int] = (0, 0),
                 exit: tuple[int, int] | None = None) -> None:
        """Initialize the maze generator with given parameters."""

    def generate(self) -> None:
        """Generate the maze. Must be called before accessing any maze data."""

    @property
    def grid(self) -> list[list[int]]:
        """2D grid of hex wall values (0–15). Access as grid[row][col]."""

    @property
    def forty_two_cells(self) -> set[tuple[int, int]]:
        """Set of (col, row) coordinates that form the '42' pattern (impassable)."""

    @property
    def entry(self) -> tuple[int, int]:
        """Entry cell coordinates (col, row)."""

    @property
    def exit(self) -> tuple[int, int]:
        """Exit cell coordinates (col, row)."""

    @property
    def width(self) -> int:
        """Number of columns."""

    @property
    def height(self) -> int:
        """Number of rows."""

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """Return True if the wall in the given direction is closed.
        x = col, y = row. direction: 'N', 'E', 'S', 'W'.
        """
```

> ⚠️ Do **NOT** add a `.solution` property. BFS is Person 2's job.

---

#### 3.2 Wall Encoding

Each cell is stored as one hex digit (0–F). Each bit encodes whether a wall is **closed** (1) or **open** (0):

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 (MSB) | West |

Examples:
- `0x0` = `0000` → all walls open (fully open cell)
- `0xF` = `1111` → all walls closed (fully blocked — used for "42")
- `0x3` = `0011` → North + East walls closed
- `0xA` = `1010` → East + West walls closed

---

#### 3.3 Maze Generation Algorithm

- [ ] Choose **one** algorithm. Recommended: **Recursive Backtracker (DFS)** — easiest to implement, produces nice long winding corridors.
  - Alternative: Prim's or Kruskal's (both valid)
- [ ] Use `random.seed(seed)` at the start of `generate()` so results are reproducible
- [ ] If `perfect=True`: generate a **perfect maze** — exactly one path between any two cells (i.e., a spanning tree). No loops.
- [ ] If `perfect=False`: you may remove additional walls to create loops (optional feature)

**Recursive Backtracker (DFS) in a nutshell:**
1. Start at a random cell, mark it visited
2. Pick a random unvisited neighbor, remove the wall between them, move there
3. Repeat until stuck, then backtrack
4. Continue until all cells are visited

---

#### 3.4 Maze Validity Rules (all mandatory)

- [ ] Entry and exit are different cells, both inside the maze bounds
- [ ] **No isolated cells** — every cell must be reachable from entry
- [ ] **Wall coherence** — if cell A has an East wall closed, cell B (immediately East of A) must have its West wall closed too. Both sides of every shared wall must agree.
- [ ] **No large open areas** — no 3×3 (or larger) fully open region. Corridors max 2 cells wide.
- [ ] **Border walls** — the outer border is always closed, except at entry and exit cells

**Wall coherence helper:**
```python
# After generating, verify coherence for every cell:
# If grid[row][col] has East wall open, grid[row][col+1] must have West wall open
# If grid[row][col] has South wall open, grid[row+1][col] must have North wall open
```

---

#### 3.5 The "42" Pattern

- [ ] Before finalizing the maze, place a **"42"** shape made of **fully closed cells** (`0xF`) somewhere inside the maze
- [ ] The shape must be recognizable as "42" when visualized (think pixel font / block letters)
- [ ] Expose the coordinates of these cells via `forty_two_cells` property
- [ ] If the maze is **too small** to fit the pattern (e.g. width < 10 or height < 8), print an error message to console and skip the pattern (`forty_two_cells` returns empty set)

**Example "42" pixel layout (each `X` = a fully closed cell):**
```
X X . X X X . . X X
X X . X . X . . . X
X X . X X X . . . X
X X . X . . . . . X
X X . X X X . . X X
```
You can design your own layout as long as it's clearly readable.

> 🚫 Do **NOT** implement BFS or path-finding. Person 2 does that using your `forty_two_cells` and `has_wall()`.

---

### 4. Makefile

**File:** `Makefile` at repo root

```makefile
install:
	pip install -r requirements.txt

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

> ⚠️ Makefile targets use **tabs**, not spaces.

---

### 5. Python Package (pip-installable)

**File:** `pyproject.toml` at repo root

- [ ] Create `pyproject.toml`:

  ```toml
  [build-system]
  requires = ["setuptools", "wheel"]
  build-backend = "setuptools.backends.legacy:build"

  [project]
  name = "mazegen-yourlogin"
  version = "1.0.0"
  description = "Reusable maze generator Python module"
  requires-python = ">=3.10"
  ```

- [ ] Build the package (run this in a clean virtualenv):
  ```bash
  pip install build
  python -m build
  ```
  This produces:
  - `dist/mazegen-1.0.0-py3-none-any.whl`
  - `dist/mazegen-1.0.0.tar.gz`

- [ ] **Copy** the `.whl` (or `.tar.gz`) file to the **root of your Git repo** (evaluators will install it from there)

- [ ] Make sure all source files needed to rebuild are in the repo (evaluators will run `python -m build` themselves)

---

### 6. Module Documentation

Write a short doc (inside `mazegen/generator.py` docstring, or a separate `mazegen/README_module.md`) explaining:

- How to install the package
- How to instantiate and use `MazeGenerator`
- How to pass parameters (size, seed, perfect)
- How to access the grid and forty_two_cells

**Minimum example to include:**

```python
from mazegen.generator import MazeGenerator

mg = MazeGenerator(width=20, height=15, seed=42, perfect=True,
                   entry=(0, 0), exit=(19, 14))
mg.generate()

# Access raw grid (hex wall values)
grid = mg.grid              # list[list[int]], grid[row][col]

# Check if a wall exists
mg.has_wall(0, 0, 'N')     # True (border wall)
mg.has_wall(0, 0, 'E')     # True or False depending on generated maze

# Get "42" blocked cells
blocked = mg.forty_two_cells   # set of (col, row) tuples
```

---

### 7. Code Quality (applies to ALL your files)

- [ ] Every function and method has **type hints** for all parameters and return type
- [ ] Every class and function has a **docstring** (Google or NumPy style — PEP 257)
- [ ] Code passes `flake8 .` with no errors
- [ ] Code passes `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs` with no errors
- [ ] Use `try/except` for file operations and resource access
- [ ] Use `with open(...)` (context manager) for all file reads/writes

---

## 📦 Final Deliverables Checklist

- [ ] `mazegen/generator.py` — `MazeGenerator` class, fully implemented
- [ ] `mazegen/config.py` — `parse_config()` function
- [ ] `mazegen/__init__.py` — (can be empty or re-export key names)
- [ ] `config.txt` — default config at repo root
- [ ] `Makefile` — all 5 mandatory rules + optional lint-strict
- [ ] `.gitignore`
- [ ] `pyproject.toml`
- [ ] `mazegen-X.X.X-py3-none-any.whl` (or `.tar.gz`) at repo root
- [ ] Module documentation (with usage example)
- [ ] All code: type hints + docstrings + flake8 clean + mypy clean

---

## 🔗 What You Expose to Person 2

Person 2 needs exactly this from you — nothing more, nothing less:

```python
from mazegen.config import parse_config
# parse_config(filepath: str) -> dict

from mazegen.generator import MazeGenerator
# MazeGenerator(width, height, seed, perfect, entry, exit)
# .generate()           -> None
# .grid                 -> list[list[int]]       (grid[row][col], values 0–15)
# .forty_two_cells      -> set[tuple[int,int]]   ((col, row) of blocked cells)
# .entry                -> tuple[int,int]
# .exit                 -> tuple[int,int]
# .width                -> int
# .height               -> int
# .has_wall(x, y, dir)  -> bool                  (dir: 'N'/'E'/'S'/'W')
```

> ✅ Once you push `mazegen/` and these APIs work, Person 2 can fully integrate without any further coordination.
