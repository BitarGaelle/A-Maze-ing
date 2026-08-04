import sys
import mazegen.config
import mazegen.generator

def a_maze_ing():
    try:
        av = sys.argv
        ac = len(av)

        if ac != 2:
            raise ValueError("Usage: python <prog_name> <filename>")
        filename = av[1]
        dictionary = mazegen.config.parse_config(filename)
        gen = mazegen.generator.MazeGenerator(dictionary)
        gen.generate()
        gen.draw()

    except Exception as e:
        print(e)

a_maze_ing()