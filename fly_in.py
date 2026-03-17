import sys
from typing import Optional


def parsing(file: str) -> dict:
    config = {
        "nb_drones": "",
        "start_hub": "",
        "end_hub": "",
        "hubs": [],
        "connections": []
    }
    try:
        with open(file, 'r') as file:
            for line in file:
                line = line.strip().split('#')[0].strip()
                if not line:
                    continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key in ["hub", "connection"]:
                        config[key + "s"].append(value)
                    else:
                        config[key] = value
                else:
                    print("Error : Invalid format", line)
                    sys.exit(1)
    except FileNotFoundError:
        print("Error: file not found")
        sys.exit(1)
    except PermissionError:
        print("Error: Permission denied to read")
        sys.exit(1)
    except Exception as e:
        print("UNexpected Error ", e)
        sys.exit(1)
    return config


class Zone:
    def __init__(self, name: str, x: int, y: int, zone_type: str = "normal",
                 max_drones: int = 1, color: Optional[str] = None) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.max_drones = max_drones
        self.color = color
        self.drones_count = 0

    @staticmethod
    def validate_zone(line_value: str):
        parts = line_value.split('[')
        main_data = parts[0].strip()
        data_list = main_data.split()
        if len(data_list) != 3:
            raise ValueError("Missing coordinates")
        try:
            name = data_list[0]
            if "-" in name:
                raise ValueError(f"zine name '{name}' should not contain dashes")
            x = int(data_list[1])
            y = int(data_list[2])
        except ValueError:
            raise ValueError("Les coordonnées x et y doivent être des entiers")

        metadata = {
            "zone": "normal",
            "max_drones": 1,
            "color": None
        }
        if len(parts) > 1:
            raw_meta = parts[1].replace(']', '').strip().split()
            for item in raw_meta:
                if '=' not in item:
                    raise ValueError(f"Métadonnée malformée : {item}")
                key, val = item.split('=')
                if key == "max_drones":
                    metadata[key] = int(val)
                else:
                    metadata[key] = val
        return {"name": name, "x": x, "y": y, "metadata": metadata}
