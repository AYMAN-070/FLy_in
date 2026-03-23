from typing import Dict, List, Any
from .models import Zone, Connection, Drone


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

    def get_voisins(self, zone_name: str) -> list[str]:
        voisins = []
        for conn in self.connections:
            if conn.zone1_name == zone_name:
                voisins.append(conn.zone2_name)
            elif conn.zone2_name == zone_name:
                voisins.append(conn.zone1_name)
        return voisins
