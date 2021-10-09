import pathlib
import os
def create_pet():    
    import tkinter as tk
    from src.animations import AnimationStates, Canvas, Animator, get_animations
    from src.pets import Pet
    from screeninfo import get_monitors

    # Configuration

    offset = 400

    # Get info on the monitor
    monitor = get_monitors()[0]
    resolution = {"width": int(monitor.width), "height": int(monitor.height - offset)}

    # window configuration
    window = tk.Tk()
    window.config(highlightbackground="black")
    label = tk.Label(window, bd=0, bg="black")
    window.overrideredirect(True)
    window.wm_attributes("-transparentcolor", "black")
    label.pack()  # loop the program
    canvas = Canvas(window, label, resolution)

    # Load the animations. 
    # ! NOTE, this has to be done after setting up the tikinter window
    ANIMATIONS = get_animations()

    # Create the desktop pet
    animator = Animator(state=AnimationStates.IDLE, frame_number=0, animations=ANIMATIONS)
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