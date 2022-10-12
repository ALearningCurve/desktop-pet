import tkinter as tk
from PIL import Image
from .animation import AnimationStates, Animator, get_animations
from src.pets import Pet
from screeninfo import get_monitors
from xml.dom import minidom
import distutils.util
from src import logger
import pathlib
import os
from .window_utils import configure_window, show_window
from .config_reader import XMLReader


def start_program(current_pet: str = None):
    """Creates a window and pet from the configuration xml and then shows that pet

    Args:
        current_pet (str, optional): [description]. Defaults to None.

    Raises:
        Exception: [description]
    """
    logger.debug("Loading general configuration from XML")
    ### General Configuration
    config = XMLReader()
    current_pet = config.getDefaultPet() if current_pet is None else current_pet
    topmost = config.getForceTopMostWindow()
    should_run_preprocessing = config.getShouldRunAnimationPreprocessing()

    ### Animation Specific Configuration
    # Find the desired pet
    logger.debug('Finding "current_pet" configurations from the XML')
    pet_config = config.getMatchingPetConfigurationClean(current_pet)

    ### Window Configuration
    logger.debug("Creating tkinter window/config")
    # Get info on the primary monitor (that is where the pet will be)
    monitor = get_monitors()[0]
    resolution = {
        "width": int(monitor.width),
        "height": int(monitor.height - pet_config.offset),
    }
    window = tk.Tk()
    canvas = configure_window(
        window, topmost=topmost, bg_color=pet_config.bg_color, resolution=resolution
    )

    ## Load the animations.
    logger.debug("Starting to load animations")
    animations = get_animations(
        current_pet, pet_config.target_resolution, should_run_preprocessing
    )

    animator = Animator(
        state=AnimationStates.IDLE, frame_number=0, animations=animations
    )

    # We esentially only need to run preprocessing once as it is really expensive to do
    # so make it false for the next time the program runs
    if should_run_preprocessing:
        config.setFirstTagValue("should_run_preprocessing", "false")
        config.save()

    ## Initialize pet
    # Create the desktop pet
    logger.debug("Create pet")
    x = int(canvas.resolution["width"] / 2)
    y = int(canvas.resolution["height"])
    pet = Pet(x, y, canvas=canvas, animator=animator)
    # bind key events to the pet and start the app
    canvas.label.bind("<ButtonPress-1>", pet.start_move)
    canvas.label.bind("<ButtonRelease-1>", pet.stop_move)
    canvas.label.bind("<B1-Motion>", pet.do_move)
    logger.info(pet.__repr__())

    # Begin the main loop
    window.after(1, pet.on_tick)
    show_window(window)
    window.mainloop()
    return pet
