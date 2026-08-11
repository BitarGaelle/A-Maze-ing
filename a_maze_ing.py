import sys
import mazegen.config
from mazegen.generator import MazeGenerator
from solver import MazeSolver
from typing import Any
from writer import writer
import random


def a_maze_ing(regen: bool = False, show: bool = True):
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
        gen.draw(path, show)

        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice: int = int(input("Choice?(1-4)"))
        if (choice < 1 and choice > 4):
            raise ValueError("choose a number between 1-4 please")
        if choice == 1:
            a_maze_ing(True, show)
            
        if choice == 2:
            a_maze_ing(False, not show)

        # if choice == 3:

        if choice == 4:
            exit()   

    except Exception as e:
        print(e)

a_maze_ing()