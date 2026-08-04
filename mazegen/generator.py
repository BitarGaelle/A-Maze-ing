from typing import Any
import random
# 🐭  mouse (start)
# 🧀  cheese (path)
# 🧱(border) 🏁(goal) ⬜(white space)

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

    def get_neighbors(self, coord: tuple[int, int, int]) -> list[tuple[int, int, int]]:
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
                       
    def generate(self) -> None:
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        self.dfs(self.entry, visited)

    def draw(self) -> None:
        print("+" + "---+" * self.width)

        for x in range(self.height):
            row_top = "|"
            row_bottom = "+"

            for y in range(self.width):
                cell = self.grid[x][y]

                # cell content
                if (x, y) == self.entry:
                    content = " S "
                elif (x, y) == self.exit:
                    content = " E "
                else:
                    content = "   "

                row_top += content

                # East wall
                if cell & 2:
                    row_top += "|"
                else:
                    row_top += " "

                # South wall
                if cell & 4:
                    row_bottom += "---+"
                else:
                    row_bottom += "   +"

            print(row_top)
            print(row_bottom)



        


