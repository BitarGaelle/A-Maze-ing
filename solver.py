from mazegen.generator import MazeGenerator


class MazeSolver:
    def __init__(self, maze: MazeGenerator):
        self.maze = maze
        self.queue: list[tuple[int, int]] = []
        self.visited: list[list[bool]] = [[False for _ in range(maze.width)]
                                          for _ in range(maze.height)]
        self.parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
        self.start = maze.entry
        self.exit = maze.exit
        self.height = maze.height
        self.width = maze.width

    def get_neighbors(self,
                      coord: tuple[int, int]) -> list[tuple[int, int, str]]:
        """this is a docstring"""
        x, y = coord
        valid: list[tuple[int, int, str]] = []
        neighbors: list[tuple[int, int, str]] = []
        cell: int = self.maze.grid[x][y]
        if cell & 1 == 0:
            neighbors.append((x-1, y, "N"))  # N
        if cell & 2 == 0:
            neighbors.append((x, y+1, "E"))  # E
        if cell & 4 == 0:
            neighbors.append((x+1, y, "S"))  # S
        if cell & 8 == 0:
            neighbors.append((x, y-1, "W"))  # W

        for neigh in neighbors:
            x, y, _ = neigh
            if 0 > x or x >= self.height or 0 > y or y >= self.width:
                continue
            if self.visited[x][y]:
                continue
            valid.append(neigh)
        return valid

    def solver(self) -> list[str]:

        self.queue.append(self.start)
        self.visited[self.start[0]][self.start[1]] = True

        while self.queue:
            cur: tuple[int, int] = self.queue.pop(0)
            if cur == self.exit:
                path: list[str] = []
                while cur in self.parent.keys():
                    path.append(self.parent[cur][1])
                    cur = self.parent[cur][0]
                path.reverse()
                return path

            neighbors: list[tuple[int, int, str]] = self.get_neighbors(cur)
            for neigh in neighbors:
                x, y, dir = neigh
                coord = (x, y)
                self.queue.append(coord)
                self.visited[x][y] = True
                self.parent[coord] = (cur, dir)
        return []
