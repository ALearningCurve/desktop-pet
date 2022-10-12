from enum import Enum, auto
import tkinter as tk
import random
from itertools import repeat
import pathlib
import os
from os import listdir
from os.path import isfile, join
from typing import Callable, Tuple, Dict
from typing import List
from PIL import Image, ImageTk
from src import logger


class Canvas:
    """Represents information on the tkinter window and label as well as information of the
    desktop's width and height, aka resolution
    """

    window: tk.Tk
    label: tk.Label
    resolution: any

    def __init__(self, window, label, resolution):
        """
        Args:
            window (tkinter.Tk)
            label (tkinter.Label)
            resolution (Dict[str, int]): must have "width" and "height" as keys
        """
        self.window = window
        self.label = label
        self.resolution = resolution

    def __repr__(self):
        return f"<Canvas:c width {self.resolution['width']}px and height {self.resolution['height']}px>"
