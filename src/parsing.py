import sys


class ConfigParser:
    @staticmethod
    def parsing(file: str) -> dict:
        config: dict = {
            "nb_drones": "",
            "start_hub": "",
            "end_hub": "",
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
