from typing import Any

def check_constraints(dictionary: dict[str, Any]) -> None:
    for key, value in dictionary.items():
        if key in ("WIDTH", "HEIGHT"):
            if value <= 2:
                raise ValueError("Width/Height must be greater than 2")
        elif key in ("ENTRY", "EXIT"):
            x, y = value
            if dictionary["ENTRY"] == dictionary["EXIT"]:
                raise ValueError("Entry and Exit's coordinates must be different.")
            if 0 > x or x >= dictionary["HEIGHT"] or 0 > y or y >= dictionary["WIDTH"]:
                raise ValueError("Out of bounds!")

    print("All constraints verified!")

def casting_value(key: str, value: str) -> Any:
    new_value: Any = value
    if key in ("WIDTH", "HEIGHT", "SEED"):
        new_value = int(value)
    elif key in ("ENTRY", "EXIT"):
        val_arr = value.split(",")
        if len(val_arr) == 2:
            new_value = (int(val_arr[0].strip()), int(val_arr[1].strip()))
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
            raise ValueError("The value of 'PERFECT' must be True OR False!")
    return new_value


def parse_config(filename: str) -> dict[str, Any]:
    try:
        with open (filename, "r") as f:
            res_dict = {}
            for line in f:
                if line[0] == '#' or line[0] == '\n':
                    continue
                else:
                    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"]
                    res_arr = line.split("=")
                    if len(res_arr) == 2:
                        key = res_arr[0].strip().upper()
                        value = res_arr[1].strip()
                        if (key in keys and key not in res_dict):
                            res_dict[key] = casting_value(key, value)
                        else:
                            raise ValueError("Invalid/Duplicate key!")
                        
                    else:
                        raise ValueError("Wrong Config Syntax!")
        mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        for item in mandatory:
            if item not in res_dict.keys():
                raise ValueError("Missing mandatory key!")
        check_constraints(res_dict)
        return (res_dict)
    except Exception as e:
        print(e)
    return {}
