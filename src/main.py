import tkinter as tk
from src.animations import AnimationStates, Canvas, Animator, get_animations, run_preprocessing
from src.pets import Pet
from screeninfo import get_monitors
from xml.dom import minidom

def create_pet(should_run_preprocessing = False) -> Pet:
    """Creates a pet from the configuration object

    Returns:
        Pet
    """
    ### General Configuration
    dom = minidom.parse('config.xml')
    animation_set = current_pet = dom.getElementsByTagName('defualt_pet')[0].firstChild.nodeValue
    topmost = bool(dom.getElementsByTagName('force_topmost')[0].firstChild.nodeValue)

    ### Animation Specific Configuration
    # Find the desired pet
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
    # Load the animations. 
    # ! NOTE, this has to be done after setting up the tikinter window
    if should_run_preprocessing:
        ANIMATIONS = run_preprocessing(animation_set, target_resolution)
    else:
        ANIMATIONS = get_animations(animation_set, target_resolution)

    # Create the desktop pet
    animator = Animator(state=AnimationStates.SLEEP, frame_number=0, animations=ANIMATIONS)
    x = int(canvas.resolution["width"] / 2)
    y = int(canvas.resolution["height"])
    pet = Pet(x, y, canvas=canvas, animator=animator)
    print(pet)

    # bind key events to the pet and start the app
    window.after(1, pet.on_tick)
    label.bind("<ButtonPress-1>", pet.start_move)
    label.bind("<ButtonRelease-1>", pet.stop_move)
    label.bind("<B1-Motion>", pet.do_move)

    window.mainloop()

    return pet