from typing import Optional, Any


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
    def validate_zone(line_value: str) -> dict:
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
                    try:
                        m_val = int(val)
                        if m_val <= 0:
                            raise ValueError()
                        metadata[key] = m_val
                    except ValueError:
                        raise ValueError(f"max_drones for zone '{name}' must "
                                         f" be a positive integer")
                elif key == "zone":
                    if val not in ["normal", "blocked", "restricted",
                                   "priority"]:
                        raise ValueError(f"Invalid zone type '{val}'")
                    metadata[key] = val
                else:
                    metadata[key] = val
        return {"name": name, "x": x, "y": y, "metadata": metadata}


class Connection:

    def __init__(self, zone1_name: str, zone2_name: str,
                 max_link_capacity: int = 1) -> None:
        self.zone1_name = zone1_name
        self.zone2_name = zone2_name
        self.max_link_capacity = max_link_capacity
        self.used_capacity_turn = 0
        self.drones_count = 0

    @staticmethod
    def validate_connection(line_value: str) -> dict[str, Any]:
        parts = line_value.split('[')
        main_data = parts[0].strip()
        zones = main_data.split('-')
        if len(zones) != 2:
            raise ValueError("Invalid format. Expected: zone1-zone2 ")
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
                    try:
                        c_val = int(val)
                        if c_val <= 0:
                            raise ValueError()
                        metadata[key] = c_val
                    except ValueError:
                        raise ValueError("max_link_capacity must be positive")
                else:
                    metadata[key] = val
        return {
            "zone1": zone1_name,
            "zone2": zone2_name,
            "metadata": metadata
        }


class Drone:
    def __init__(self, drone_id: int, start_zone: str) -> None:
        self.id = drone_id
        self.current_zone = start_zone
        self.path: list[str] = []
        self.is_finished = False
        self.wait_time = 0
