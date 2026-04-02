from typing import Dict, List, Any, Optional, Generator
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
        z1 = data["zone1"]
        z2 = data["zone2"]
        for conn in self.connections:
            if (conn.zone1_name == z1 and conn.zone2_name == z2) or \
               (conn.zone1_name == z2 and conn.zone2_name == z1):
                raise ValueError(f"Error: Connection between {z1} and {z2} "
                                 f"already exists!")
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
                """We make priority zones at the top of the list"""
                voisins.sort(key=lambda v: 0 if self.zones[v].zone_type == "priority" else 1)
                for voisin in voisins:
                    nouveau_chemin = list(path)
                    nouveau_chemin.append(voisin)
                    queue.append(nouveau_chemin)
        return []

    def get_voisins(self, zone_name: str) -> list[str]:
        """find neighbors and Skip Blocked Zone"""
        voisins = []
        v_zone = ""
        for conn in self.connections:
            if conn.zone1_name == zone_name:
                v_zone = conn.zone2_name
            elif conn.zone2_name == zone_name:
                v_zone = conn.zone1_name
            if v_zone and self.zones[v_zone].zone_type != "blocked":
                voisins.append(v_zone)
        return voisins

    def get_connection(self, zone1_name: str,
                       zone2_name: str) -> Optional[Connection]:
        """Find the path that connects two zones,"""
        for conn in self.connections:
            if (conn.zone1_name == zone1_name and
                conn.zone2_name == zone2_name) or \
               (conn.zone1_name == zone2_name and
                    conn.zone2_name == zone1_name):
                return conn
        return None

    def run_simulation(self) -> Generator[Dict[str, Any], None, None]:
        start_name = list(self.zones.values())[0].name
        end_name = list(self.zones.values())[1].name
        shortest_path = self.find_shortest_path(start_name, end_name)
        if not shortest_path:
            print("Error: Can't find the shortest path")
            return
        drones = [Drone(i + 1, start_name) for i in range(self.nb_drones)]
        for drone in drones:
            drone.path = list(shortest_path)
            """We place all the drones at the starting zone"""
        self.zones[start_name].drones_count = self.nb_drones
        """Time engine"""
        turn = 1
        yield {
                    "turn": 0,
                    "movements": 0,
                    "drones_states": {d.id: d.current_zone for d in drones}
                }
        """Check is there at least one drone that hasn't arrived yet"""
        while any(not drone.is_finished for drone in drones):
            for conn in self.connections:
                conn.used_capacity_turn = 0
            movement_tour = []
            """if Drone in zone 'priority' we place it at the first of list """
            drones.sort(key=lambda d: 0 if
                        self.zones[d.current_zone].zone_type ==
                        "priority" else 1)
            for drone in drones:
                if drone.is_finished:
                    continue
                if drone.wait_time > 0:
                    drone.wait_time -= 1
                    continue
                index_now = drone.path.index(drone.current_zone)
                next_zone_name = drone.path[index_now + 1]
                actual_zone = self.zones[drone.current_zone]
                next_zone = self.zones[next_zone_name]
                road = self.get_connection(actual_zone.name, next_zone.name)
                if not road:
                    continue
                """Is there enough space in the arrival zone"""
                place_dispo = (
                    next_zone.drones_count < next_zone.max_drones
                    or next_zone.name == end_name
                    )
                """Is road has the capacity for this tour"""
                free_road = road.used_capacity_turn < road.max_link_capacity
                if place_dispo and free_road:
                    actual_zone.drones_count -= 1
                    next_zone.drones_count += 1
                    road.used_capacity_turn += 1
                    drone.current_zone = next_zone_name
                    if drone.current_zone == end_name:
                        drone.is_finished = True
                    else:
                        if next_zone.zone_type == "restricted":
                            drone.wait_time = 1
                    movement_tour.append(f"D{drone.id}-{drone.current_zone}")
            if movement_tour:
                """We sort the final text by Drone number,
                because we change the order before to check priority zone"""
                movement_tour.sort(key=lambda x:
                                   int(x.split('-')[0].replace('D', '')))
                yield {
                    "turn": turn,
                    "movements": movement_tour,
                    "drones_states": {d.id: d.current_zone for d in drones}
                }
                print(" ".join(movement_tour))
            else:
                print("Waiting... (Drones are waiting or blocked)")
                yield {
                    "turn": turn,
                    "movements": movement_tour,
                    "drones_states": {d.id: d.current_zone for d in drones}
                }
            turn += 1
            if turn > 500:
                print("Simulation too long - Stop it for security")
                break
