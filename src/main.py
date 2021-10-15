import tkinter as tk
from tkinter.constants import FALSE
from src.animations import AnimationStates, Animator, Canvas, get_animations
from src.pets import Pet
from screeninfo import get_monitors
from xml.dom import minidom
import distutils.util
from src import logger

def xml_bool(val):
    return bool(distutils.util.strtobool(val))
def create_pet(should_run_preprocessing = None, current_pet = None) -> Pet:
    """Creates a pet from the configuration object

    Returns:
        Pet
    """
    logger.debug('Loading general configuration from XML')
    ### General Configuration
    dom = minidom.parse('config.xml')
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

    ## We pick a transparent color here for the background
    # ! This should be different for mac as mac os has alpha channel
    # ! so this is not really needed there
    window.config(highlightbackground=bg_color)
    label = tk.Label(window, bd=0, bg=bg_color)
    window.overrideredirect(True)
    window.wm_attributes("-transparentcolor", bg_color)
    label.pack()
    ## Set on top attribute to True (at least at first) to bring it to the top
    window.wm_attributes('-topmost', True)
    window.update()
    window.wm_attributes('-topmost', topmost)
    canvas = Canvas(window, label, resolution)
    
    ## Load the animations. 
    # ! NOTE, this has to be done after setting up the tikinter window
    logger.debug('Starting to load animations')
    animations = get_animations(current_pet, target_resolution, should_run_preprocessing)
    animator = Animator(state=AnimationStates.SLEEP, frame_number=0, animations=animations)
    # We esentially only need to run preprocessing once per animation
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
    with open("config.xml", "w") as f:
        f.write(dom.toxml())

    # Begin the main loop
    window.after(1, pet.on_tick)
    window.mainloop()
    return pet