from typing import Any


def check_constraints(dictionary: dict[str, Any]) -> None:
    """
    Validate the configuration values against the maze constraints.

    Checks that WIDTH and HEIGHT are large enough for the 42 logo
    and do not exceed the maximum maze size. It also verifies that
    ENTRY and EXIT are different, within the maze boundaries, and
    do not overlap the 42 logo.

    Args:
        dictionary: Parsed configuration containing the maze settings.

    Raises:
        ValueError: If any configuration value violates a maze constraint.
    """
    for key, value in dictionary.items():

        if key in ("WIDTH", "HEIGHT"):

            if value <= 8:
                raise ValueError("Width/Height must be greater\n"
                                 "than 9 for the logo to fit")
            elif value > 30:
                raise ValueError("Width/Height must be \n"
                                 "less or equal than 30")

        elif key in ("ENTRY", "EXIT"):

            start_x = (dictionary["HEIGHT"] - 5) // 2
            start_y = (dictionary["WIDTH"] - 7) // 2

            x, y = value

            if dictionary["ENTRY"] == dictionary["EXIT"]:
                raise ValueError("Entry and Exit's coordinates\n"
                                 "must be different.")

            if (
                0 > x or x >= dictionary["HEIGHT"]
                or 0 > y or y >= dictionary["WIDTH"]
            ):
                raise ValueError("Out of bounds!")

            if (
                start_x <= x < start_x + 5
                and start_y <= y < start_y + 7
            ):
                raise ValueError("Entry/Exit coordinates cannot\n"
                                 "be inside the 42 logo.")


def casting_value(key: str, value: str) -> Any:
    """
    Convert a configuration value from a string to its appropriate type.

    Integer values such as WIDTH, HEIGHT, and SEED are converted to int.
    ENTRY and EXIT are converted to coordinate tuples. PERFECT is
    converted to a boolean, while OUTPUT_FILE is validated as a
    non-empty string.

    Args:
        key: Configuration key associated with the value.
        value: Raw string value read from the configuration file.

    Returns:
        The value converted to its appropriate Python type.

    Raises:
        ValueError: If ENTRY/EXIT has an invalid format, OUTPUT_FILE
            is empty, or PERFECT is not True or False.
    """
    new_value: Any = value

    if key in ("WIDTH", "HEIGHT", "SEED"):
        new_value = int(value)

    elif key in ("ENTRY", "EXIT"):
        val_arr = value.split(",")

        if len(val_arr) == 2:
            new_value = (
                int(val_arr[0].strip()),
                int(val_arr[1].strip())
            )
        else:
            raise ValueError("Invalid format for ENTRY/EXIT keys")

    elif key == "OUTPUT_FILE":

        if not new_value.strip():
            raise ValueError("OUTPUT_FILE cannot be empty!")

    elif key == "PERFECT":

        if value == "True":
            new_value = True
        elif value == "False":
            new_value = False
        else:
            raise ValueError(
                "The value of 'PERFECT' must be True OR False!"
            )

    return new_value


def parse_config(filename: str) -> dict[str, Any]:
    """
    Read and validate a maze configuration file.

    The configuration file must contain KEY=VALUE pairs. Supported keys
    are WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, and SEED.
    Lines beginning with '#' and empty lines are ignored.

    Mandatory keys are WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, and
    PERFECT. Values are converted to their appropriate Python types
    before the complete configuration is validated.

    Args:
        filename: Path to the configuration file.

    Returns:
        A dictionary containing the parsed and validated configuration.
        Returns an empty dictionary if the file does not exist.

    Raises:
        ValueError: If the configuration contains an invalid or duplicate
            key, has incorrect syntax, is missing a mandatory key, or
            contains invalid values.
    """
    try:
        with open(filename, "r") as f:
            res_dict = {}

            for line in f:
                if line[0] == '#' or line[0] == '\n':
                    continue
                else:
                    keys = [
                        "WIDTH", "HEIGHT", "ENTRY", "EXIT",
                        "OUTPUT_FILE", "PERFECT", "SEED"
                    ]

                    res_arr = line.split("=")

                    if len(res_arr) == 2:
                        key = res_arr[0].strip().upper()
                        value = res_arr[1].strip()

                        if key in keys and key not in res_dict:
                            res_dict[key] = casting_value(key, value)
                        else:
                            raise ValueError("Invalid/Duplicate key!")
                    else:
                        raise ValueError("Wrong Config Syntax!")

        mandatory = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
        ]

        for item in mandatory:
            if item not in res_dict.keys():
                raise ValueError("Missing mandatory key!")

        check_constraints(res_dict)
        return res_dict

    except FileNotFoundError:
        print(f"Error-File {filename} not found")

    return {}
