import tkinter as tk
from tkinter import filedialog
from typing import Tuple, List

from classes.city import City


def get_file_path(file_types: Tuple[str, str] = []) -> str or None:
    """Open file explorer to select a file"""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile(filetypes=file_types)
    if file_path is not None:
        return file_path.name
    return None


def print_progress(progress_amount: int, total: int, percent_increments: int) -> None:
    """Print a progress bar animation to the console"""
    percentage: float = progress_amount / total * 100
    fill_length: str = '=' * int(percentage // percent_increments)
    empty_length: str = ' ' * (100 // percent_increments - len(fill_length))
    print(f'[{fill_length}{empty_length}] {percentage:.2f}% complete', end='\r')


def calc_distance(city_a: City, city_b: City) -> float:
    return ((float(city_b.x) - float(city_a.x)) ** 2 + (float(city_b.y) - float(city_a.y)) ** 2) ** (1 / 2)


def calc_total_distance(city_path: List[City]) -> float:
    total_distance: float = 0
    for i in range(len(city_path) - 1):
        total_distance += calc_distance(city_path[i], city_path[i + 1])
    return total_distance
