from typing import Any

import random


class MazeGenerator:
    """
    Generate and manage a maze using a depth-first search algorithm.

    The maze is represented as a grid where each cell stores its walls
    using a 4-bit hexadecimal value. Each bit represents one wall:
    North = 1, East = 2, South = 4, and West = 8.

    The generator can create a perfect maze using DFS and can optionally
    remove additional walls to create an imperfect maze.
    """

    def __init__(self, dictionary: dict[str, Any]):
        """
        Initialize a maze generator from the parsed configuration.

        Args:
            dictionary: Configuration dictionary containing the maze
                dimensions, entry and exit coordinates, output file,
                perfect mode, and optional random seed.
        """
        self.width = dictionary["WIDTH"]
        self.height = dictionary["HEIGHT"]
        self.entry = dictionary["ENTRY"]
        self.exit = dictionary["EXIT"]
        self.output_file = dictionary["OUTPUT_FILE"]
        self.perfect = dictionary["PERFECT"]
        self.seed = dictionary.get("SEED", None)

        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)
        ]

    @staticmethod
    def get_oposite(dir: int) -> int:
        """
        Get the wall bit corresponding to the opposite direction.

        Args:
            dir: Wall direction represented as a bit:
                1 = North, 2 = East, 4 = South, 8 = West.

        Returns:
            The wall bit representing the opposite direction.

        Raises:
            KeyError: If the provided direction is not a valid wall bit.
        """
        return {
            1: 4,
            2: 8,
            4: 1,
            8: 2
        }[dir]

    def get_neighbors(
        self, coord: tuple[int, int]
    ) -> list[tuple[int, int, int]]:
        """
        Get all valid neighboring cells of a given cell.

        Each neighbor is returned as a tuple containing its coordinates
        and the direction of the wall separating it from the current cell.

        Args:
            coord: Coordinates of the current cell as (row, column).

        Returns:
            A list of valid neighboring cells represented as
            (row, column, direction).
        """
        x, y = coord

        valid: list[tuple[int, int, int]] = []
        neighbors: list[tuple[int, int, int]] = []

        neighbors.append((x - 1, y, 1))  # N
        neighbors.append((x, y + 1, 2))  # E
        neighbors.append((x + 1, y, 4))  # S
        neighbors.append((x, y - 1, 8))  # W

        for neigh in neighbors:
            x, y, _ = neigh

            if 0 > x or x >= self.height or 0 > y or y >= self.width:
                continue

            valid.append(neigh)

        return valid

    def get_closed_walls(
        self, coord: tuple[int, int]
    ) -> list[tuple[int, int, int]]:
        """
        Get the closed walls of a cell that lead to unvisited neighbors.

        This is used when creating an imperfect maze to find a wall that
        can be removed between the current cell and one of its neighbors.
        Cells belonging to the 42 logo are excluded.

        Args:
            coord: Coordinates of the current cell as (row, column).

        Returns:
            A list of closed walls represented as
            (neighbor_row, neighbor_column, direction).
        """
        x, y = coord

        closed_walls: list[tuple[int, int, int]] = []
        neighbors: list[tuple[int, int, int]] = []

        visited_logo = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self.add_logo_to_visited(visited_logo)

        cell: int = self.grid[x][y]

        if cell & 1 == 1:
            neighbors.append((x - 1, y, 1))  # N

        if cell & 2 == 2:
            neighbors.append((x, y + 1, 2))  # E

        if cell & 4 == 4:
            neighbors.append((x + 1, y, 4))  # S

        if cell & 8 == 8:
            neighbors.append((x, y - 1, 8))  # W

        for neigh in neighbors:
            x, y, _ = neigh

            if 0 > x or x >= self.height or 0 > y or y >= self.width:
                continue

            if visited_logo[x][y]:
                continue

            closed_walls.append(neigh)

        return closed_walls

    def solution_cells(
        self, solution_path: list[str]
    ) -> list[tuple[int, int]]:
        """
        Convert a solution path into the coordinates of its cells.

        The path starts at the maze entry and each direction moves to
        the corresponding neighboring cell.

        Args:
            solution_path: List of directions ("N", "E", "S", "W")
                representing the solution path from entry to exit.

        Returns:
            A list of cell coordinates visited by the solution path,
            including both the entry and exit cells.
        """
        solution_cells: list[tuple[int, int]] = []

        x, y = self.entry
        solution_cells.append((x, y))

        for direction in solution_path:
            if direction == "N":
                x -= 1
            elif direction == "E":
                y += 1
            elif direction == "S":
                x += 1
            elif direction == "W":
                y -= 1

            solution_cells.append((x, y))

        return solution_cells

    def make_imperfect(self, path: list[str]) -> None:
        """
        Add loops to the maze by removing selected walls along the solution.

        Every few cells on the solution path, a random closed wall leading
        to a non-logo cell is selected and removed from both neighboring
        cells.

        Args:
            path: Solution path represented as a list of directions.
        """
        sol_cells: list[tuple[int, int]] = self.solution_cells(path)
        counter: int = 0

        for x, y in sol_cells:
            if counter > 3:
                counter = 0

            if counter == 0:
                closed_walls: list[tuple[int, int, int]] = (
                    self.get_closed_walls((x, y))
                )

                if len(closed_walls) >= 1:
                    n_x, n_y, dir = random.choice(closed_walls)
                    oposite = self.get_oposite(dir)

                    self.grid[x][y] = self.grid[x][y] - dir
                    self.grid[n_x][n_y] = (
                        self.grid[n_x][n_y] - oposite
                    )

            counter += 1

    def dfs(
        self,
        coord: tuple[int, int],
        visited: list[list[bool]]
    ) -> None:
        """
        Generate maze passages using recursive depth-first search.

        The neighbors are shuffled to create a randomized maze. When an
        unvisited neighbor is found, the wall between the current cell
        and that neighbor is removed, and DFS continues recursively.

        Args:
            coord: Coordinates of the current cell as (row, column).
            visited: 2D matrix tracking cells that have already been
                visited or reserved by the 42 logo.
        """
        cur_x, cur_y = coord
        visited[cur_x][cur_y] = True

        neighbors = self.get_neighbors(coord)
        random.shuffle(neighbors)

        for neighbor in neighbors:
            neig_x, neig_y, direction = neighbor
            oposite: int = self.get_oposite(direction)

            if visited[neig_x][neig_y] is False:
                self.grid[cur_x][cur_y] = (
                    self.grid[cur_x][cur_y] - direction
                )

                self.grid[neig_x][neig_y] = (
                    self.grid[neig_x][neig_y] - oposite
                )

                self.dfs((neig_x, neig_y), visited)

    def add_logo_to_visited(
        self, visited: list[list[bool]]
    ) -> None:
        """
        Mark the 42 logo cells as visited so DFS cannot modify them.

        The logo is centered in the maze and occupies a 7x5 area.
        Only the cells that form the visible 42 shape are marked.

        Args:
            visited: 2D matrix used by DFS to track unavailable cells.
        """
        logo_wid: int = 7
        logo_heigh: int = 5

        logo = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        start_x: int = (self.height - logo_heigh) // 2
        start_y: int = (self.width - logo_wid) // 2

        for i in range(logo_heigh):
            for j in range(logo_wid):
                if logo[i][j] == 1:
                    visited[start_x + i][start_y + j] = True

    def generate(self) -> None:
        """
        Generate the maze starting from the configured entry cell.

        The 42 logo cells are marked as unavailable before DFS begins.
        The random seed is then initialized to ensure reproducible maze
        generation when a seed is provided.

        DFS generates the initial perfect maze. If imperfect mode is
        enabled, additional walls can later be removed using
        make_imperfect().
        """
        visited: list[list[bool]] = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self.add_logo_to_visited(visited)

        random.seed(self.seed)

        self.dfs(self.entry, visited)
