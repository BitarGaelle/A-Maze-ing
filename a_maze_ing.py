import sys
import mazegen.config
from mazegen.generator import MazeGenerator
from solver import MazeSolver
from typing import Any
from writer import writer

def a_maze_ing():
    try:
        av: list[str] = sys.argv
        ac: int = len(av)

        if ac != 2:
            raise ValueError("Usage: python <prog_name> <filename>")
        filename: str = av[1]
        dictionary: dict[str, Any] = mazegen.config.parse_config(filename)
        gen: MazeGenerator = MazeGenerator(dictionary)
        solv: MazeSolver = MazeSolver(gen)
        gen.generate()
        gen.draw()
        path: list[str] = solv.solver()
        writer(dictionary, gen, path)

    except Exception as e:
        print(e)

a_maze_ing()