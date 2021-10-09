import random
import tkinter as tk
from animations import AnimationStates, Canvas, Animator


class Pet:
 size = 100
 x: int
 y: int
 v_y: float = 0
 a_y: float = .3
 canvas: Canvas
 animator: Animator

 def __init__(self, x, y, canvas, animator):
  self.x = x
  self.y = y
  self.canvas = canvas
  self.animator = animator 
 
 def do_movement(self):
  if (self.x < 0):
      self.x = Pet.size
  if self.x > self.canvas.resolution["width"] - Pet.size:
      self.x = self.canvas.resolution["width"] -  Pet.size

  # do stuff with the y position
  if self.y > self.canvas.resolution["height"]:
      self.y = self.canvas.resolution["height"]
      if self.animator.state == AnimationStates.FALLING:
          self.v_y = 0
          self.animator.set_state(AnimationStates.LANDED)
          
  if self.animator.state == AnimationStates.FALLING:
      self.v_y += self.a_y
      self.y += self.v_y
      self.y = int(self.y)

 def update(self):
  animation = self.get_current_animation()
  x, y = animation.get_velocity()
  self.x += x
  self.y += y  
  self.do_movement()
  self.progress_animation()

 def draw(self):
  animation = self.get_current_animation()
  return animation.frames[self.animator.frame_number]

 def on_tick(self):
  """Draw the current animation
  """
  self.update()
  frame = self.draw()
  self.set_geometry()
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
   self.animator.set_state(animation.next(self.animator))
#   print(self.animator.state, self.animator.frame_number)

 def get_current_animation(self):
   return self.animator.animations[self.animator.state]

 def start_move(self, event):
      self.animator.set_state(AnimationStates.GRABBED)
    #   self.x = event.x_root
    #   self.y = event.y_root
      self.v_y = 0

 def stop_move(self, event):
      self.animator.set_state(AnimationStates.FALLING)

 def do_move(self, event):
    self.progress_animation()
    self.x = event.x_root
    self.y = event.y_root
    self.v_y = 0
    self.set_geometry()
    ## self.geometry(f"+{x}+{y}")

 def set_geometry(self):
   self.canvas.window.geometry(str(Pet.size) + 'x' + str(Pet.size) + '+'+str(self.x)+'+'+str(self.y))
