from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from typing import Any, Dict


class Visualizer(QMainWindow):
    def __init__(self, simulation_engine: Any) -> None:
        super().__init__()
        self.sim = simulation_engine
        self.setWindowTitle("Fly_In Simulation - Mode")
        self.resize(1000, 800)
        """History so I can do replay using 'Q' """
        self.history: list[dict[str, Any]] = []
        self.current_index = 0
        self.simulation_generator = self.sim.run_simulation()
        self.is_finished = False
        """2D scene"""
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        """Shoow turn number"""
        self.turn_counter_item = QGraphicsTextItem("Tour : 0")
        self.turn_counter_item.setDefaultTextColor(QColor("black"))
        font = self.turn_counter_item.font()
        font.setPointSize(16)
        font.setBold(True)
        self.turn_counter_item.setFont(font)
        self.turn_counter_item.setPos(20, 20)
        self.scene.addItem(self.turn_counter_item)
        """Dict to stock graphic objects"""
        self.zone_items: dict[str, Any] = {}
        self.drone_items: dict[int, Any] = {}
        self.draw_map()
        self.advance_simulation()
        self.update_display(self.history[0])

    def get_screen_coords(self, x: float, y: float) -> tuple[float, float]:
        return (x * 150) + 100, (y * 150) + 100

    def draw_map(self) -> None:
        """For roads we make gray thikness 2"""
        self.zone_stats_items = {}
        pen = QPen(QColor("gray"), 2)
        for conn in self.sim.connections:
            z1 = self.sim.zones[conn.zone1_name]
            z2 = self.sim.zones[conn.zone2_name]
            x1, y1 = self.get_screen_coords(z1.x, z1.y)
            x2, y2 = self.get_screen_coords(z2.x, z2.y)
            line = QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(pen)
            self.scene.addItem(line)
        for zone in self.sim.zones.values():
            x, y = self.get_screen_coords(zone.x, zone.y)
            final_color = QColor(zone.color) if zone.color else QColor()
            if not final_color.isValid():
                if zone.zone_type == "restricted":
                    final_color = QColor("red")
                elif zone.zone_type == "priority":
                    final_color = QColor("orange")
                elif zone.zone_type == "blocked":
                    final_color = QColor("black")
                else:
                    final_color = QColor("skyblue")
            ellipse = QGraphicsEllipseItem(x - 15, y - 15, 30, 30)
            ellipse.setBrush(QBrush(final_color))
            ellipse.setPen(QPen(QColor("black")))
            self.scene.addItem(ellipse)
            text = QGraphicsTextItem(zone.name)
            text.setPos(x - 15, y - 40)
            self.scene.addItem(text)
            stats_text = QGraphicsTextItem("")
            stats_text.setDefaultTextColor(QColor("darkblue"))
            stats_text.setPos(x + 20, y - 15)
            self.scene.addItem(stats_text)
            self.zone_stats_items[zone.name] = stats_text
        start_zone_name = list(self.sim.zones.values())[0].name
        start_zone = self.sim.zones[start_zone_name]
        start_x, start_y = self.get_screen_coords(start_zone.x, start_zone.y)

        for i in range(1, self.sim.nb_drones + 1):
            drone_rect = QGraphicsRectItem(0, 0, 12, 12)
            drone_rect.setBrush(QBrush(QColor("pink")))
            drone_rect.setPos(start_x - 6, start_y - 6)
            self.drone_items[i] = drone_rect
            self.scene.addItem(drone_rect)

    def update_display(self, data: Dict[str, Any]) -> None:
        """Updqte visual position of drones"""
        if not data:
            return
        current_turn = data.get("turn", 0)
        self.turn_counter_item.setPlainText(f"Turn : {current_turn}")
        states = data["drones_states"]
        counts: Dict[str, list[str]] = {name: [] for name
                                        in self.sim.zones.keys()}
        for drone_id, zone_name in states.items():
            if drone_id in self.drone_items:
                zone = self.sim.zones[zone_name]
                nx, ny = self.get_screen_coords(zone.x, zone.y)
                self.drone_items[drone_id].setPos(nx - 6, ny - 6)
                counts[zone_name].append(str(drone_id))
        for zone_name, drone_ids in counts.items():
            nb = len(drone_ids)
            label = self.zone_stats_items[zone_name]
            if nb > 0:
                label.setPlainText(f"Drones: {nb}\n({', '.join(drone_ids)})")
            else:
                label.setPlainText("")

    def keyPressEvent(self, event: Any) -> None:
        if event.key() == Qt.Key.Key_D:
            self.advance_simulation()
        elif event.key() == Qt.Key.Key_Q:
            self.rewind_simulation()

    def advance_simulation(self) -> None:
        """REPLAY fi we already have the program in history"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.update_display(self.history[self.current_index])
            return
        else:
            """We calculat the tour"""
            if self.is_finished is False:
                try:
                    new_data = next(self.simulation_generator)
                    self.history.append(new_data)
                    self.current_index += 1
                    self.update_display(new_data)
                except StopIteration:
                    self.is_finished = True
                    print("All the drones have arrived !")

    def rewind_simulation(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display(self.history[self.current_index])
