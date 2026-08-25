from mazegen.generator import MazeGenerator

from typing import Any


def writer(
    dictionary: dict[str, Any],
    maze: MazeGenerator,
    path: list[str]
) -> None:
    """
    Write the generated maze and its solution to the output file.

    The maze grid is written as uppercase hexadecimal values, followed
    by the entry coordinates, exit coordinates, and the solution path.

    Args:
        dictionary: Parsed configuration dictionary containing the
            output file path.
        maze: MazeGenerator instance containing the generated maze,
            entry, and exit coordinates.
        path: List of directions ("N", "E", "S", "W") representing
            the solution path from the entry to the exit.
    """
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
