import random
import tkinter as tk
from animations import AnimationStates, Canvas, Animator


class Pet:
 x: int
 y: int
 canvas: Canvas
 animator: Animator

 def __init__(self, x, y, canvas, animator):
  self.x = x
  self.y = y
  self.canvas = canvas
  self.animator = animator

 def update(self):
  animation = self.get_current_animation()
  x, y = animation.get_velocity()
  self.x += x
  self.y += y  
  self.progress_animation()

 def draw(self):
  animation = self.get_current_animation()
  return animation.frames[self.animator.frame_number]

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
  animations = self.animator.animations
  for key in animations.keys():
   if self.animator.event_number in animations[key].event_numbers:
    self.animator.state = key
    self.canvas.window.after(animations[key].frame_timer,self.on_tick)
    return
  raise Exception("Current event number does not belong to any animation!")
  
 #making gif work 
 def progress_animation(self):
  animation = self.get_current_animation()
  if self.animator.frame_number < len(animation.frames) -1:
   self.animator.frame_number+=1
  else:
   self.animator.frame_number = 0
   self.animator.event_number = random.randrange(animation.next_event_number_min,animation.next_event_number_max+1,1)

 def get_current_animation(self):
   return self.animator.animations[self.animator.state]