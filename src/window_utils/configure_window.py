import tkinter as tk
import pathlib
import os
from .window_visability import show_in_tray, show_window, hide_window
from .canvas import Canvas


def configure_window(
    window: tk.Tk, topmost=True, bg_color="#000", pet_name="Pet", resolution=(100, 100)
):
    # We pick a transparent color here for the background
    # ! This should be different for mac as mac os has alpha channel
    # ! so this is not really needed there
    window.config(highlightbackground=bg_color)
    label = tk.Label(window, bd=0, bg=bg_color)
    window.overrideredirect(True)
    window.update_idletasks()
    window.wm_attributes("-transparentcolor", bg_color)
    label.pack()

    # Set on top attribute to True (at least at first) to bring it to the top
    window.wm_attributes("-topmost", True)
    window.update()
    window.wm_attributes("-topmost", topmost)
    # update name and icon of the window
    window.winfo_toplevel().title("Desktop " + pet_name)
    window.iconbitmap(os.path.join(pathlib.Path().resolve(), "icon.ico"))

    # Remove minimize/close buttuns and titlebar, but
    # keep in the taskbar
    window.overrideredirect(True)
    window.protocol("WM_DELETE_WINDOW", lambda: hide_window(window))

    canvas = Canvas(window, label, resolution)
    return canvas
