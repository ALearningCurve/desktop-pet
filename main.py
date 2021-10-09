import pyautogui
import random
import tkinter as tk
from animations import AnimationStates, Canvas, Animator, get_animations
from pets import Pet
impath = 'C:\\Users\\willw\\Documents\\GitHub\Personal\\desktop-pet\\demo-gifs\\'

window = tk.Tk()
#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
label.pack()#loop the program
canvas = Canvas(window, label)

ANIMATIONS = get_animations(impath)

animator = Animator(state = AnimationStates.IDLE_TO_SLEEP, 
 event_number = random.randrange(1,3,1), 
 frame_number = 0,
 animations=ANIMATIONS)

pet = Pet(x=1400, y=1050, canvas=canvas, animator=animator)


window.after(1,pet.on_tick)
window.mainloop()