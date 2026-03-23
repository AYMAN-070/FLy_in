import sys
import os
import tkinter as tk
from tkinter import filedialog
from src.parsing import ConfigParser
from src.simulation import Simulation


def choose_file() -> str:
    root = tk.Tk()
    root.withdraw()
    dossier_projet = os.path.dirname(os.path.abspath(__file__))
    dossier_maps = os.path.join(dossier_projet, "maps")
    file_path = filedialog.askopenfilename(
        title="Select Fly_in card",
        initialdir=dossier_maps,
        filetypes=[("Text file", "*.txt"), ("All text files", "*.*")]
    )
    if not file_path:
        print("No card selected !")
        sys.exit(0)
    return file_path


def main() -> None:
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        print("Opening files ...")
        file_path = choose_file()

    print(f"\n Uploading cards: {file_path}...")
    config = ConfigParser.parsing(file_path)
    sim = Simulation(config)
    print(f"Goal : Flying {sim.nb_drones} drones.")


if __name__ == "__main__":
    main()
