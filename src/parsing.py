import sys
from typing import Dict, Any


class ConfigParser:
    @staticmethod
    def parsing(file: str) -> Dict[str, Any]:
        config: Dict[str, Any] = {
            "nb_drones": None,
            "start_hub": None,
            "end_hub": None,
            "hubs": [],
            "connections": []
        }
        try:
            with open(file, 'r') as f:
                for line in f:
                    line = line.strip().split('#')[0].strip()
                    if not line:
                        continue
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if config["nb_drones"] is None:
                            if key != "nb_drones":
                                print("Error: First line must be nb_drones")
                                sys.exit(1)
                            try:
                                config[key] = int(value)
                                if int(value) <= 0:
                                    raise ValueError("nb_drones "
                                                     "should be >= 0")
                            except ValueError as e:
                                print("Error : ", e)
                                sys.exit(1)
                        elif key in ["start_hub", "end_hub"]:
                            if config[key] is not None:
                                print(f"Error: duplicate {key}")
                                sys.exit(1)
                            config[key] = value
                        elif key in ["hub", "connection"]:
                            config[key + "s"].append(value)
                        else:
                            config[key] = value
                    else:
                        print("Error : Invalid format", line)
                        sys.exit(1)
            if not config["start_hub"] or not config["end_hub"]:
                print("Error: missing start_hub or end_hub")
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
