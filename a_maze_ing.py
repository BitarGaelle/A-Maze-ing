import sys
import mazegen.config
from mazegen.generator import MazeGenerator
from solver import MazeSolver
from typing import Any
from writer import writer
import random
from draw import draw


def a_maze_ing(regen: bool = False, show: bool = True,
               color: str = "\033[0m", logo_color: str = "\033[31m") -> None:
    try:
        av: list[str] = sys.argv
        ac: int = len(av)

        if ac != 2:
            raise ValueError("Usage: python <prog_name> <filename>")
        filename: str = av[1]
        dictionary: dict[str, Any] = mazegen.config.parse_config(filename)
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
        if (choice < 1 and choice > 4):
            raise ValueError("choose a number between 1-4 please")
        if choice == 1:
            a_maze_ing(True, show, color, logo_color)

        if choice == 2:
            a_maze_ing(False, not show, color, logo_color)

        if choice == 3:
            CYAN: str = "\033[36m"
            GREEN: str = "\033[32m"
            RED: str = "\033[31m"
            YELLOW: str = "\033[33m"
            MAGENTA: str = "\033[35m"

            colors = [CYAN, GREEN, RED, YELLOW, MAGENTA]
            color_rand = random.Random()
            color_content = color_rand.choice(colors)
            logo_color = color_rand.choice(colors)
            a_maze_ing(False, show, color_content, logo_color)

        if choice == 4:
            exit()

    except Exception as e:
        print(e)


a_maze_ing()
