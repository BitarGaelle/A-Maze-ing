from typing import Any
import random


class MazeGenerator:
    def __init__(self, dictionary: dict[str, Any]):
        self.width = dictionary["WIDTH"]
        self.height = dictionary["HEIGHT"]
        self.entry = dictionary["ENTRY"]
        self.exit = dictionary["EXIT"]
        self.output_file = dictionary["OUTPUT_FILE"]
        self.perfect = dictionary["PERFECT"]
        self.seed = dictionary.get("SEED", None)
        self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]

    def get_oposite(self, dir: int) -> int:
        if dir == 2:
            return (8)
        if dir == 8:
            return (2)
        if dir == 1:
            return (4)
        if dir == 4:
            return (1)

    def get_neighbors(self, coord: tuple[int, int]) -> list[tuple[int, int, int]]:
        x, y = coord
        valid: list[tuple[int, int, int]] = []
        neighbors: list[tuple[int, int, int]] = []
        neighbors.append((x-1, y, 1)) # N
        neighbors.append((x, y+1, 2)) # E
        neighbors.append((x+1, y, 4)) # S
        neighbors.append((x, y-1, 8)) # W

        for neigh in neighbors:
            x, y, _ = neigh
            if 0 > x or x >= self.height or 0 > y or y >= self.width:
                continue
            valid.append(neigh)
        return valid

    def get_closed_walls(self, coord: tuple[int, int]) -> list[tuple[int, int, int]]:
        """this is a docstring"""
        x, y = coord
        closed_walls: list[tuple[int, int, int]] = []
        neighbors: list[tuple[int, int, int]] = []
        visited_logo = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.add_logo_to_visited(visited_logo)

        cell: int = self.grid[x][y]
        if cell & 1 == 1:
            neighbors.append((x-1, y, 1)) # N
        if cell & 2 == 2:
            neighbors.append((x, y+1, 2)) # E
        if cell & 4 == 4:
            neighbors.append((x+1, y, 4)) # S
        if cell & 8 == 8:
            neighbors.append((x, y-1, 8)) # W

        for neigh in neighbors:
            x, y, _ = neigh
            if 0 > x or x >= self.height or 0 > y or y >= self.width:
                continue
            if visited_logo[x][y]:
                continue
            closed_walls.append(neigh)
        return closed_walls

    def solution_cells(self, solution_path: list[tuple[str]]) -> list[tuple[int, int]]:
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
        sol_cells: list[tuple[int, int]] = self.solution_cells(path)
        counter: int = 0
        for x, y in sol_cells:
            if counter > 3:
                counter = 0
            if counter == 0:
                closed_walls: tuple[int, int, int] = self.get_closed_walls((x,y))
                if len(closed_walls) >= 1:
                    neigh_x, neigh_y, dir = random.choice(closed_walls)
                    self.grid[x][y] = self.grid[x][y] - dir
                    self.grid[neigh_x][neigh_y] = self.grid[neigh_x][neigh_y] - self.get_oposite(dir)
            counter += 1

    def dfs(self, coord: tuple[int, int], visited: list[list[bool]]) -> None:
        cur_x, cur_y = coord
        visited[cur_x][cur_y] = True
        neighbors = self.get_neighbors(coord)

        random.shuffle(neighbors)

        for neighbor in neighbors:
            neig_x, neig_y, direction = neighbor
            if visited[neig_x][neig_y] is False:
                self.grid[cur_x][cur_y] = self.grid[cur_x][cur_y] - direction
                self.grid[neig_x][neig_y] = self.grid[neig_x][neig_y] - self.get_oposite(direction)
                self.dfs((neig_x, neig_y), visited)

    def add_logo_to_visited(self, visited: list[list[bool]]) -> None:
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
        visited: list[list[bool]] = [[False for _ in range(self.width)] for _ in range(self.height)]

        self.add_logo_to_visited(visited)
        random.seed(self.seed)
        self.dfs(self.entry, visited)
