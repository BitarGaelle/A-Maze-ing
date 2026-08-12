from mazegen import MazeGenerator


def draw(maze: MazeGenerator, solution_path: list[str],
         show: bool, color: str, logo_color: str) -> None:
    RESET: str = "\033[0m"
    sol_cells: list[tuple[int, int]] = []

    if show:
        sol_cells = maze.solution_cells(solution_path)

    logo = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]

    logo_height = len(logo)
    logo_width = len(logo[0])

    start_x = (maze.height - logo_height) // 2
    start_y = (maze.width - logo_width) // 2

    print(f"{color}█{RESET}" + f"{color}████{RESET}" * maze.width)

    for x in range(maze.height):

        row_top = f"{color}█{RESET}"
        row_bottom = f"{color}█{RESET}"

        for y in range(maze.width):

            cell = maze.grid[x][y]

            logo_x = x - start_x
            logo_y = y - start_y

            is_logo = (
                0 <= logo_x < logo_height
                and 0 <= logo_y < logo_width
            )

            # -------------------------
            # Content
            # -------------------------

            if (x, y) == maze.entry:
                content = "🐭 "

            elif (x, y) == maze.exit:
                content = " 🧀"

            elif is_logo and logo[logo_x][logo_y] == 1:
                content = f"{logo_color}███{RESET}"

            elif show and (x, y) in sol_cells:
                content = " • "

            else:
                content = "   "

            row_top += content

            # -------------------------
            # East wall
            # -------------------------

            if cell & 2:
                row_top += f"{color}█{RESET}"
            else:
                row_top += " "

            # -------------------------
            # South wall
            # -------------------------

            if cell & 4:
                row_bottom += f"{color}████{RESET}"
            else:
                row_bottom += f"{color}   █{RESET}"

        print(row_top)
        print(row_bottom)
