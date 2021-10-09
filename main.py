import pyautogui
import random
import tkinter as tk
from enum import Enum
from dataclasses import dataclass

idle_num =[1,2,3,4]
sleep_num = [10,11,12,13,15]
walk_left = [6,7]
walk_right = [8,9]
impath = 'C:\\Users\\willw\\Documents\\GitHub\Personal\\desktop-pet\\demo-gifs\\'

class AnimationStates(Enum):
 IDLE = 0
 IDLE_TO_SLEEP = 1
 SLEEP = 2
 SLEEP_TO_IDLE = 3
 WALK_NEGATIVE = 4
 WALK_POSITIVE = 5

class Pet:
 state: AnimationStates 
 frame_number: int
 x: int
 y: int
 event_number: int

 def __init__(self, state, frame_number, event_number, x, y):
  self.x = x
  self.y = y
  self.state = state
  self.frame_number = frame_number
  self.event_number = event_number

 def update_and_frame(self):
  animation = ANIMATIONS[self.state]
  animation.move()
  frame = animation.frames[self.frame_number]
  self.frame_number, self.event_number = gif_work(self, animation)
  return frame

class Animation:
 """Defines the event numbers for this animation 
 and the ways this animation can transfer to the
 next animation
 """
 event_numbers: list[int]
 # Number that can be trasnsfered to 
 next_event_number_min: int
 next_event_number_max: int
 frames: list 

 # the time between the frame being drawn in the animation
 frame_timer: int
 
 # Some animations require movement
 v_x: int
 v_y: int
 

 def __init__(self, event_numbers, next_event_number_min, next_event_number_max, frames, frame_timer = 100, v_x = 0, v_y = 0):
  self.event_numbers = event_numbers
  self.next_event_number_min = next_event_number_min
  self.next_event_number_max = next_event_number_max
  self.frame_timer = frame_timer
  self.frames = frames
  self.v_x = v_x
  self.v_y = v_y

 def move(self):
  pet.x += self.v_x
  pet.y += self.v_y


pet = Pet(state = AnimationStates.IDLE_TO_SLEEP, 
 event_number = random.randrange(1,3,1), 
 frame_number = 0, 
 x=1400, y=1050)

def update(pet):
 frame = pet.update_and_frame()
 window.geometry('100x100+'+str(pet.x)+'+'+str(pet.y))
 label.configure(image=frame)
 window.after(1,event,pet)

#transfer random no. to event
def event(pet):
 for key in ANIMATIONS.keys():
  if pet.event_number in ANIMATIONS[key].event_numbers:
   pet.state = key
   window.after(ANIMATIONS[key].frame_timer,update,pet)
   return
 raise Exception("Current event number does not belong to any animation!")
  
#making gif work 
def gif_work(pet: Pet,animation: Animation):
 if pet.frame_number < len(animation.frames) -1:
  pet.frame_number+=1
 else:
  pet.frame_number = 0
  pet.event_number = random.randrange(animation.next_event_number_min,animation.next_event_number_max+1,1)
 return pet.frame_number, pet.event_number

window = tk.Tk()

idle = [tk.PhotoImage(file=impath+'idle.gif',format = 'gif -index %i' %(i)) for i in range(5)]#idle gif
idle_to_sleep = [tk.PhotoImage(file=impath+'idle_to_sleep.gif',format = 'gif -index %i' %(i)) for i in range(8)]#idle to sleep gif
sleep = [tk.PhotoImage(file=impath+'sleep.gif',format = 'gif -index %i' %(i)) for i in range(3)]#sleep gif
sleep_to_idle = [tk.PhotoImage(file=impath+'sleep_to_idle.gif',format = 'gif -index %i' %(i)) for i in range(8)]#sleep to idle gif
walk_positive = [tk.PhotoImage(file=impath+'walking_positive.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to left gif
walk_negative = [tk.PhotoImage(file=impath+'walking_negative.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to right gif

ANIMATIONS: dict[AnimationStates, Animation] = {
 AnimationStates.IDLE: Animation([1,2,3,4], 1, 9, idle, 400),
 AnimationStates.IDLE_TO_SLEEP: Animation([5], 10, 10, idle_to_sleep),
 AnimationStates.SLEEP: Animation([10,11,12,13,15], 10, 15, sleep, 1000),
 AnimationStates.SLEEP_TO_IDLE: Animation([14], 1, 1, sleep_to_idle),
 AnimationStates.WALK_POSITIVE: Animation([8,9], 1, 9, walk_positive, v_x=3),
 AnimationStates.WALK_NEGATIVE: Animation([6,7], 1, 9, walk_negative, v_x=-3),
}



assert(len(AnimationStates) == len(ANIMATIONS.keys()))


#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
label.pack()#loop the program
window.after(1,update,pet)
window.mainloop()