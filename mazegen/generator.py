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

        start_x: int = (self.height - logo_heigh) // 2
        start_y: int = (self.width - logo_wid) // 2
        for i in range(logo_heigh):
            for j in range(logo_wid):
                visited[start_x + i][start_y + j] = True

    def generate(self) -> None:
        visited: list[list[bool]] = [[False for _ in range(self.width)] for _ in range(self.height)]

        self.add_logo_to_visited(visited)
        random.seed(self.seed)
        self.dfs(self.entry, visited)

    def draw(self, solution_path: list[str]) -> None:
        # Convert directions into coordinates
        solution_cells: set[tuple[int, int]] = set()

        x, y = self.entry
        solution_cells.add((x, y))

        for direction in solution_path:
            if direction == "N":
                x -= 1
            elif direction == "E":
                y += 1
            elif direction == "S":
                x += 1
            elif direction == "W":
                y -= 1

            solution_cells.add((x, y))

        logo = [
            [1,0,1,0,1,1,1],
            [1,0,1,0,0,0,1],
            [1,1,1,0,1,1,1],
            [0,0,1,0,1,0,0],
            [0,0,1,0,1,1,1]
        ]

        logo_height = len(logo)
        logo_width = len(logo[0])

        start_x = (self.height - logo_height) // 2
        start_y = (self.width - logo_width) // 2

        print("+" + "---+" * self.width)

        for x in range(self.height):
            row_top = "|"
            row_bottom = "+"

            for y in range(self.width):
                cell = self.grid[x][y]

                logo_x = x - start_x
                logo_y = y - start_y

                is_logo = (
                    logo_x >= 0 and logo_x < logo_height and
                    logo_y >= 0 and logo_y < logo_width
                )

                # content
                if (x, y) == self.entry:
                    content = " S "

                elif (x, y) == self.exit:
                    content = " E "

                elif is_logo == True and logo[logo_x][logo_y] == 1:
                    content = " █ "
                
                elif (x, y) in solution_cells:
                    content = " • "

                else:
                    content = "   "

                row_top += content

                # East wall
                if is_logo == True:
                    if logo_y == logo_width - 1:
                        row_top += "|"
                    else:
                        row_top += " "

                elif cell & 2:
                    row_top += "|"

                else:
                    row_top += " "

                # South wall
                if is_logo == True:
                    row_bottom += "...+"

                elif cell & 4:
                    row_bottom += "---+"

                else:
                    row_bottom += "   +"

            print(row_top)
            print(row_bottom)
