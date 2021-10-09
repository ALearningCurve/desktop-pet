import pyautogui
import random
import tkinter as tk
from animations import AnimationStates, Canvas, Animator, get_animations
from pets import Pet
from screeninfo import get_monitors

# Configuration
impath = 'C:\\Users\\willw\\Documents\\GitHub\Personal\\desktop-pet\\demo-gifs\\'
offset = 400

monitor = get_monitors()[0]
resolution = {
    "width": int(monitor.width),
    "height": int(monitor.height - offset)
}

window = tk.Tk()
#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
label.pack()#loop the program
canvas = Canvas(window, label, resolution)

ANIMATIONS = get_animations(impath)

animator = Animator(state = AnimationStates.IDLE, 
 frame_number = 0,
 animations=ANIMATIONS)

x=int(canvas.resolution["width"]/2)
y=int(canvas.resolution["height"])
print(x, y)
pet = Pet(x, y, canvas=canvas, animator=animator)


window.after(1,pet.on_tick)


label.bind("<ButtonPress-1>", pet.start_move)
label.bind("<ButtonRelease-1>", pet.stop_move)
label.bind("<B1-Motion>", pet.do_move)

window.mainloop()



    # self.label = tk.Label(self, text="Click on the grip to move")
    # self.grip = tk.Label(self, bitmap="gray25")
    # self.grip.pack(side="left", fill="y")
    # self.label.pack(side="right", fill="both", expand=True)

