import pyautogui
import random
import tkinter as tk
from animations import AnimationStates, Animation, get_animations

impath = 'C:\\Users\\willw\\Documents\\GitHub\Personal\\desktop-pet\\demo-gifs\\'

class Canvas:
 window: tk.Tk
 label: tk.Label

 def __init__(self, window, label):
  self.window = window
  self.label = label


class Pet:
 state: AnimationStates 
 frame_number: int
 x: int
 y: int
 event_number: int
 canvas: Canvas

 def __init__(self, state, frame_number, event_number, x, y, canvas):
  self.x = x
  self.y = y
  self.state = state
  self.frame_number = frame_number
  self.event_number = event_number
  self.canvas = canvas

 def update(self):
  animation = self.get_current_animation()
  x, y = animation.get_velocity()
  self.x += x
  self.y += y  
  self.progress_animation()

 def draw(self):
  animation = self.get_current_animation()
  return animation.frames[self.frame_number]

 def on_tick(self):
  """Draw the current animation
  """
  self.update()
  frame = self.draw()
  self.canvas.window.geometry('100x100+'+str(self.x)+'+'+str(self.y))
  self.canvas.label.configure(image=frame)
  self.canvas.window.after(1,self.handle_event)

 #transfer random no. to event
 def handle_event(self):
  """Handle a change in the event_number variable
  and then apply the appropiate animation state

  Raises:
      Exception: [description]
  """
  animations = ANIMATIONS
  for key in animations.keys():
   if self.event_number in animations[key].event_numbers:
    self.state = key
    window.after(animations[key].frame_timer,self.on_tick)
    return
  raise Exception("Current event number does not belong to any animation!")
  
 #making gif work 
 def progress_animation(self):
  animation = self.get_current_animation()
  if self.frame_number < len(animation.frames) -1:
   self.frame_number+=1
  else:
   self.frame_number = 0
   self.event_number = random.randrange(animation.next_event_number_min,animation.next_event_number_max+1,1)
  return self.frame_number, self.event_number

 def get_current_animation(self):
   return ANIMATIONS[self.state]







window = tk.Tk()
#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
label.pack()#loop the program
canvas = Canvas(window, label)

ANIMATIONS = get_animations(impath)

pet = Pet(state = AnimationStates.IDLE_TO_SLEEP, 
 event_number = random.randrange(1,3,1), 
 frame_number = 0, 
 x=1400, y=1050, canvas=canvas)


window.after(1,pet.on_tick)
window.mainloop()