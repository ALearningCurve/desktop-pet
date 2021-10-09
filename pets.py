import random
import tkinter as tk
from animations import AnimationStates, Canvas, Animator


class Pet:
 size = 100
 x: int
 y: int
 canvas: Canvas
 animator: Animator

 def __init__(self, x, y, canvas, animator):
  self.x = x
  self.y = y
  self.canvas = canvas
  self.animator = animator 
 
 def keep_on_screen(self):
  if (self.x < 0):
      self.x = Pet.size
  elif self.x > self.canvas.resolution["width"]:
      self.x = self.canvas.resolution["width"] - Pet.size
  if self.y > self.canvas.resolution["height"]:
      self.y = self.y < self.canvas.resolution["height"]

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
  self.canvas.window.geometry(str(Pet.size) + 'x' + str(Pet.size) + '+'+str(self.x)+'+'+str(self.y))
  self.canvas.label.configure(image=frame)
  self.canvas.window.after(1,self.handle_event)

 #transfer random no. to event
 def handle_event(self):
  """Handle a change in the event_number variable
  and then apply the appropiate animation state

  Raises:
      Exception: [description]
  """
  self.canvas.window.after(self.animator.animations[self.animator.state].frame_timer,self.on_tick)

  
 #making gif work 
 def progress_animation(self):
  animation = self.get_current_animation()
  if self.animator.frame_number < len(animation.frames) -1:
   self.animator.frame_number+=1
  else:
   self.animator.frame_number = 0
   self.animator.state = animation.next(self.animator)

 def get_current_animation(self):
   return self.animator.animations[self.animator.state]