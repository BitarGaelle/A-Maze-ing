from mazegen.generator import MazeGenerator
from typing import Any

def writer(dictionary: dict[str, Any], maze: MazeGenerator, 
           path: list[str]) -> None:
    filename: str = dictionary["OUTPUT_FILE"]
    grid: list[list[int]] = maze.grid
    entry: tuple[int, int] = maze.entry
    exit: tuple[int, int] = maze.exit

    with open(filename, "w") as f:
        for row in grid:
            for cell in row:
                val: str = format(cell, "x")
                f.write(val.upper())
            f.write("\n")

        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit[0]},{exit[1]}\n")
        for dir in path:
            f.write(dir)
        f.write("\n")
