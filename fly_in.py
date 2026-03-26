import sys
import os
import tkinter as tk
from tkinter import filedialog
from src.parsing import ConfigParser
from src.simulation import Simulation


def choose_file() -> str:
    """creat a window Tkinter"""
    root = tk.Tk()
    """Hide the window"""
    root.withdraw()
    """os.path.abspath..: gives the full path to the current Python file
    os.path.dirname(...): take the folder containing this file"""
    dossier_projet = os.path.dirname(os.path.abspath(__file__))
    """add 'maps' to the path"""
    dossier_maps = os.path.join(dossier_projet, "maps")
    file_path = filedialog.askopenfilename(
        title="Select Fly_in card",
        # Open the selector in maps folder
        initialdir=dossier_maps,
        # Show only .txt files
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
