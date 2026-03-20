import sys
from typing import Optional, Any, List, Dict


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
                raise ValueError(f"zone name '{name}' should not contain"
                                 "dashes")
            x = int(data_list[1])
            y = int(data_list[2])
        except ValueError:
            raise ValueError("Coordinqtes x and y should be integers")

        metadata = {
            "zone": "normal",
            "max_drones": 1,
            "color": None
        }
        if len(parts) > 1:
            raw_meta = parts[1].replace(']', '').strip().split()
            for item in raw_meta:
                if '=' not in item:
                    raise ValueError(f"Malformed metadata : {item}")
                key, val = item.split('=')
                if key == "max_drones":
                    metadata[key] = int(val)
                else:
                    metadata[key] = val
        return {"name": name, "x": x, "y": y, "metadata": metadata}


class Connection:
    def __init__(self, zone1_name: str, zone2_name: str,
                 max_link_capacity: int = 1) -> None:
        self.zone1_name = zone1_name
        self.zone2_name = zone2_name
        self.max_link_capacity = max_link_capacity
        self.drones_count = 0

    @staticmethod
    def validate_connection(line_value: str) -> dict[str, Any]:
        parts = line_value.split('[')
        main_data = parts[0].strip()
        zones = main_data.split('-')
        if len(zones) != 2:
            raise ValueError(f"Invalid connection format. Expected: "
                             f"'zone1-zone2'. Received: '{main_data}'")
        zone1_name = zones[0].strip()
        zone2_name = zones[1].strip()
        metadata = {
            "max_link_capacity": 1
        }
        if len(parts) > 1:
            raw_meta = parts[1].replace(']', '').strip().split()
            for item in raw_meta:
                if '=' not in item:
                    raise ValueError(f"Malformed metadata : {item}")
                key, val = item.split('=')
                if key == "max_link_capacity":
                    metadata[key] = int(val)
                else:
                    metadata[key] = val
        return {
            "zone1": zone1_name,
            "zone2": zone2_name,
            "metadata": metadata
        }


class Simulation:
    def __init__(self, config: dict[str, Any]) -> None:
        self.nb_drones = int(config["nb_drones"])
        self.zones: Dict[str, Zone] = {}
        self.connections: List[Connection] = []
        self.create_zone(config["start_hub"])
        self.create_zone(config["end_hub"])
        for hub_line in config["hubs"]:
            self.create_zone(hub_line)
        for conn_line in config["connections"]:
            self.create_connection(conn_line)

    def create_zone(self, line: str) -> None:
        data = Zone.validate_zone(line)
        nouvelle_zone = Zone(
            name=data["name"],
            x=data["x"],
            y=data["y"],
            zone_type=data["metadata"]["zone"],
            max_drones=data["metadata"]["max_drones"],
            color=data["metadata"]["color"]
        )
        if nouvelle_zone.name in self.zones:
            raise ValueError(f"Error : Zone {nouvelle_zone.name} "
                             f"already exist!")
        self.zones[nouvelle_zone.name] = nouvelle_zone

    def create_connection(self, line: str) -> None:
        data = Connection.validate_connection(line)
        if data["zone1"] not in self.zones or data["zone2"] not in self.zones:
            raise ValueError(f"Error: The {line} connection links to an "
                             f"unknown area!")
        nouvelle_connexion = Connection(
            zone1_name=data["zone1"],
            zone2_name=data["zone2"],
            max_link_capacity=data["metadata"]["max_link_capacity"]
        )
        self.connections.append(nouvelle_connexion)

    def find_shortest_path(self, start_name: str, end_name: str) -> list[str]:
        queue = [[start_name]]
        visited = set()
        while queue:
            path = queue.pop(0)
            current_zone = path[-1]
            if current_zone == end_name:
                return path
            if current_zone not in visited:
                visited.add(current_zone)
                voisins = self.get_voisins(current_zone)
                for voisin in voisins:
                    nouveau_chemin = list(path)
                    nouveau_chemin.append(voisin)
                    queue.append(nouveau_chemin)
        return []
