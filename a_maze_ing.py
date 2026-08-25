import sys

import mazegen.config

from mazegen.generator import MazeGenerator

from mazegen.solver import MazeSolver

from typing import Any

from mazegen.writer import writer

import random

from mazegen.draw import draw


def a_maze_ing(
    regen: bool = False,
    show: bool = True,
    color: str = "\033[0m",
    logo_color: str = "\033[31m"
) -> None:
    """
    Run the A-Maze-ing application.

    Reads the maze configuration, generates the maze, solves it using
    BFS, optionally creates an imperfect maze, writes the result to
    the configured output file, and displays the maze in the terminal.

    After displaying the maze, an interactive menu allows the user to
    regenerate the maze, show or hide the solution path, change maze
    colors, or quit the application.

    Args:
        regen: If True, generate a new maze using a randomly generated
            seed instead of the configured seed.
        show: If True, display the solution path on the maze.
        color: ANSI color code used to display the maze walls.
        logo_color: ANSI color code used to display the 42 logo.

    Raises:
        ValueError: If the command-line arguments or menu choice are
            invalid.
    """
    try:
        av: list[str] = sys.argv
        ac: int = len(av)

        if ac != 2:
            raise ValueError(
                "Usage: python <prog_name> <filename>"
            )

        filename: str = av[1]

        dictionary: dict[str, Any] = (
            mazegen.config.parse_config(filename)
        )

        if dictionary is None:
            return

        gen: MazeGenerator = MazeGenerator(dictionary)
        solv: MazeSolver = MazeSolver(gen)

        if regen:
            gen.seed = random.randint(0, 2**32 - 1)

        gen.generate()

        path: list[str] = solv.solver()

        if not gen.perfect:
            gen.make_imperfect(path)

            solv2: MazeSolver = MazeSolver(gen)
            path = solv2.solver()

        writer(dictionary, gen, path)
        draw(gen, path, show, color, logo_color)

        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        choice: int = int(input("Choice?(1-4)"))

        if choice < 1 or choice > 4:
            raise ValueError(
                "choose a number between 1-4 please"
            )

        if choice == 1:
            a_maze_ing(
                True,
                show,
                color,
                logo_color
            )

        if choice == 2:
            a_maze_ing(
                False,
                not show,
                color,
                logo_color
            )

        if choice == 3:
            CYAN: str = "\033[36m"
            GREEN: str = "\033[32m"
            RED: str = "\033[31m"
            YELLOW: str = "\033[33m"
            MAGENTA: str = "\033[35m"

            colors = [
                CYAN,
                GREEN,
                RED,
                YELLOW,
                MAGENTA
            ]

            color_rand = random.Random()
            color_content = color_rand.choice(colors)
            logo_color = color_rand.choice(colors)

            a_maze_ing(
                False,
                show,
                color_content,
                logo_color
            )

        if choice == 4:
            exit()

    except Exception as e:
        print(e)


a_maze_ing()
