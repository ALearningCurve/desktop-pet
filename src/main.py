import tkinter as tk
from src.animations import AnimationStates, Canvas, Animator, get_animations, run_preprocessing
from src.pets import Pet
from screeninfo import get_monitors

def create_pet(should_run_preprocessing = False) -> Pet:
    """Creates a pet from the configuration object

    Returns:
        Pet
    """
    # Configuration
    # TODO Move this into the conifg.json or .xml idc
    offset = 100
    bg_color = "#ff0000" # ! this color will need to change for each of the different background color in order for it to be transparent
    # Get info on the primary monitor (that is where the pet will be)
    monitor = get_monitors()[0]
    resolution = {"width": int(monitor.width), "height": int(monitor.height - offset)}
    # Stuff for the animation
    target_resolution = (300,300)
    animation_type = "horse"


    # window configuration
    window = tk.Tk()

    # ! We pick a transparent color here for the background
    # ! This can be different for mac as mac os has alpha channel
    if True:
        window.config(highlightbackground=bg_color)
        label = tk.Label(window, bd=0, bg=bg_color)
        window.overrideredirect(True)
        window.wm_attributes("-transparentcolor", bg_color)
    label.pack()  # loop the program
    canvas = Canvas(window, label, resolution)

    # Load the animations. 
    # ! NOTE, this has to be done after setting up the tikinter window
    if should_run_preprocessing:
        ANIMATIONS = run_preprocessing(animation_type, target_resolution)
    else:
        ANIMATIONS = get_animations(animation_type, target_resolution)

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