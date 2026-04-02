import sys
from src.parsing import ConfigParser
from src.simulation import Simulation
from PyQt6.QtWidgets import QApplication, QFileDialog
from src.visualizer import Visualizer


def choose_file() -> str:
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select Map File",
        "./maps",
        "Text Files (*.txt);;All Files (*)"
    )
    if not file_path:
        print("No file selected. Exiting.")
        sys.exit(0)
    return file_path


def main() -> None:
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        print("Opening files ...")
        file_path = choose_file()

    print(f"Uploading cards: {file_path}...")
    config = ConfigParser.parsing(file_path)
    try:
        sim = Simulation(config)
        print(f"Goal : Flying {sim.nb_drones} drones.")
        app = QApplication(sys.argv)
        gui = Visualizer(sim)
        gui.show()
        sys.exit(app.exec())
    except ValueError as e:
        print(f"Parsing Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
