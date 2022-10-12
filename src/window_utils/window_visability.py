from pystray import MenuItem as item, Menu
import pystray
from PIL import Image
from pathlib import Path
import os
import tkinter as tk


def hide_window(window: tk.Tk):
    # remove window from taskbar
    window.withdraw()
    show_in_tray(window)


def show_window(window: tk.Tk):
    """Make it so window appears in the task bar. This only works for windows
    https://stackoverflow.com/questions/31123663/make-tkinter-window-appear-in-the-taskbar

    Args:
        root (tk.Tk): root window
    """
    window.withdraw()
    window.wm_deiconify()


def show_in_tray(window: tk.Tk) -> pystray.Icon:
    def exit_action(icon: pystray.Icon):
        # kills the pet
        icon.stop()
        window.destroy()

    def show_action():
        # reactivates the pet
        show_window(window)
        window.mainloop()

    icon = pystray.Icon("DesktopPet")
    icon.menu = Menu(
        item("exit", lambda: exit_action(icon)), item("show", show_action, default=True)
    )
    icon.icon = Image.open(os.path.join(Path().resolve(), "icon.ico"))
    icon.title = "DesktopPet"
    icon.run()
    return icon
