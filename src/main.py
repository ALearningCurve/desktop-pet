import tkinter as tk
from src.animations import AnimationStates, Animator, Canvas, get_animations
from src.pets import Pet
from screeninfo import get_monitors
from xml.dom import minidom
import distutils.util
from src import logger
import pathlib
import os
from pystray import MenuItem as item
import pystray
from PIL import Image
import time

def show_in_taskbar(root):
    """Make it so window appears in the task bar. This only works for windows
    https://stackoverflow.com/questions/31123663/make-tkinter-window-appear-in-the-taskbar

    Args:
        root (tk.Tk): root window
    """

    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

def hide_window(window):

    def exit_action(icon):
        # icon.visible = False
        icon.stop()
        window.destroy()
        
    def show():
        window.deiconify()
        window.mainloop()

    window.withdraw()
    icon = pystray.Icon("DesktopPet")
    icon.menu = (item('exit', lambda: exit_action(icon)), item('show', show))
    icon.icon = Image.open(os.path.join(pathlib.Path().resolve(), "icon.ico"))
    icon.title = "DesktopPet"
    icon.run()

def xml_bool(val):
    return bool(distutils.util.strtobool(val))

def create_pet(current_pet: str = None) -> Pet:
    """Creates a window and pet from the configuration xml and then shows that pet

    Args:
        current_pet (str, optional): [description]. Defaults to None.

    Raises:
        Exception: [description]

    Returns:
        Pet: [description]
    """
    logger.debug('Loading general configuration from XML')
    ### General Configuration
    config_location = os.path.join(pathlib.Path().resolve(), "config.xml")
    dom = minidom.parse(config_location)
    current_pet =  dom.getElementsByTagName('defualt_pet')[0].firstChild.nodeValue if current_pet is None else current_pet
    topmost = xml_bool(dom.getElementsByTagName('force_topmost')[0].firstChild.nodeValue)
    should_run_preprocessing = xml_bool(dom.getElementsByTagName('should_run_preprocessing')[0].firstChild.nodeValue)

    ### Animation Specific Configuration
    # Find the desired pet
    logger.debug('Finding "current_pet" configurations from the XML')
    pets = dom.getElementsByTagName('pet')
    pet_config = None
    for i in range(len(pets)):
        if pets[i].getAttribute('name') == current_pet:
            pet_config = pets[i]
    if pet_config is None:
        raise Exception("Could not find the current pet as one of \
            the supported pets in the config.xml. 'current_pet' must \
            match one of the 'pet' element's 'name' attribute")     
    # Find the config for that pet
    offset = int(pet_config.getElementsByTagName('offset')[0].firstChild.nodeValue)
     # ! this color will need to change for each of the different background color in order for it to be transparent
    bg_color = pet_config.getElementsByTagName('bg_color')[0].firstChild.nodeValue
    tmp = pet_config.getElementsByTagName('resolution')[0]
    target_resolution = (
        int(tmp.getElementsByTagName("x")[0].firstChild.nodeValue),
        int(tmp.getElementsByTagName("y")[0].firstChild.nodeValue)
    )

    logger.debug('Creating tkinter window/config')
    ### Window Configuration
    # Get info on the primary monitor (that is where the pet will be)
    monitor = get_monitors()[0]
    resolution = {"width": int(monitor.width), "height": int(monitor.height - offset)}
    window = tk.Tk()

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
    window.wm_attributes('-topmost', True)
    window.update()
    window.wm_attributes('-topmost', topmost)
    # update name and icon of the window
    window.winfo_toplevel().title("Desktop " + current_pet[0].upper() + current_pet[1:])
    window.iconbitmap(os.path.join(pathlib.Path().resolve(), "icon.ico"))
    # Remove minimize/close buttuns and titlebar, but 
    # keep in the taskbar
    window.overrideredirect(True)
    window.after(10, lambda: show_in_taskbar(window))
    canvas = Canvas(window, label, resolution)
    # But also show in the system tray
    window.protocol('WM_DELETE_WINDOW', lambda: hide_window(window))
    
    ## Load the animations. 
    # ! NOTE, this has to be done after setting up the tikinter window
    logger.debug('Starting to load animations')
    animations = get_animations(current_pet, target_resolution, should_run_preprocessing)
    animator = Animator(state=AnimationStates.IDLE, frame_number=0, animations=animations)
    # We esentially only need to run preprocessing once as it is really expensive to do
    # so make it false for the next time the program runs
    dom.getElementsByTagName('should_run_preprocessing')[0].firstChild.replaceWholeText("false")
    
    ## Initialize pet
    # Create the desktop pet
    logger.debug('Create pet')
    x = int(canvas.resolution["width"] / 2)
    y = int(canvas.resolution["height"])
    pet = Pet(x, y, canvas=canvas, animator=animator)
    # bind key events to the pet and start the app
    label.bind("<ButtonPress-1>", pet.start_move)
    label.bind("<ButtonRelease-1>", pet.stop_move)
    label.bind("<B1-Motion>", pet.do_move)
    logger.info(pet.__repr__())

    # Save any changes in the configuration 
    # that happened during initialization
    with open(config_location, "w") as f:
        f.write(dom.toxml())

    # Begin the main loop
    window.after(1, pet.on_tick)
    window.mainloop()
    return pet