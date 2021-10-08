import pyautogui
import random
import tkinter as tk
from enum import Enum

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
 state: AnimationStates # check

 frame_number: int #cycle
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
  #idle
  if self.state == AnimationStates.IDLE:
   frame = idle[self.frame_number]
   self.frame_number, self.event_number = gif_work(self,idle,1,9)
  #idle to sleep
  elif self.state == AnimationStates.IDLE_TO_SLEEP:
   frame = idle_to_sleep[self.frame_number]
   self.frame_number, self.event_number = gif_work(self,idle_to_sleep,10,10)#sleep
  elif self.state == AnimationStates.SLEEP:
   frame = sleep[self.frame_number]
   self.frame_number, self.event_number = gif_work(self,sleep,10,15)#sleep to idle
  elif self.state == AnimationStates.SLEEP_TO_IDLE:
   frame = sleep_to_idle[self.frame_number]
   self.frame_number, self.event_number = gif_work(self,sleep_to_idle,1,1)#walk toward left
  elif self.state == AnimationStates.WALK_POSITIVE:
   frame = walk_positive[self.frame_number]
   self.frame_number, self.event_number = gif_work(self,walk_positive,1,9)
   self.x -= 3#walk towards right
  elif self.state == AnimationStates.WALK_NEGATIVE:
   frame = walk_negative[self.frame_number]
   self.frame_number, self.event_number = gif_work(self,walk_negative,1,9)
   self.x -= -3
  return frame



class Animation:
 event_numbers: list[int]

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
 if pet.event_number in idle_num:
  pet.state = AnimationStates.IDLE
  print('idle')
  window.after(400,update,pet)
  return
 elif pet.event_number == 5:
  pet.state = AnimationStates.IDLE_TO_SLEEP
  print('from idle to sleep')
 elif pet.event_number in walk_left:
  pet.state = AnimationStates.WALK_NEGATIVE
  print('walking towards left')
 elif pet.event_number in walk_right:
  pet.state = AnimationStates.WALK_POSITIVE
  print('walking towards right')
 elif pet.event_number in sleep_num:
  pet.state = AnimationStates.SLEEP
  print('sleep')
  window.after(1000,update,pet)
  return
 elif pet.event_number == 14:
  pet.state = AnimationStates.SLEEP_TO_IDLE
  print('from sleep to idle')
 
 window.after(100,update,pet)#no. 15 = sleep to idle
  
#making gif work 
def gif_work(pet,frames,first_num,last_num):
 if pet.frame_number < len(frames) -1:
  pet.frame_number+=1
 else:
  pet.frame_number = 0
  pet.event_number = random.randrange(first_num,last_num+1,1)
 return pet.frame_number, pet.event_number

window = tk.Tk()

idle = [tk.PhotoImage(file=impath+'idle.gif',format = 'gif -index %i' %(i)) for i in range(5)]#idle gif
idle_to_sleep = [tk.PhotoImage(file=impath+'idle_to_sleep.gif',format = 'gif -index %i' %(i)) for i in range(8)]#idle to sleep gif
sleep = [tk.PhotoImage(file=impath+'sleep.gif',format = 'gif -index %i' %(i)) for i in range(3)]#sleep gif
sleep_to_idle = [tk.PhotoImage(file=impath+'sleep_to_idle.gif',format = 'gif -index %i' %(i)) for i in range(8)]#sleep to idle gif
walk_positive = [tk.PhotoImage(file=impath+'walking_positive.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to left gif
walk_negative = [tk.PhotoImage(file=impath+'walking_negative.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to right gif

#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
label.pack()#loop the program
window.after(1,update,pet)
window.mainloop()