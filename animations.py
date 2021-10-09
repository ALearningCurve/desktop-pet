from enum import Enum
import tkinter as tk

class AnimationStates(Enum):
 IDLE = 0
 IDLE_TO_SLEEP = 1
 SLEEP = 2
 SLEEP_TO_IDLE = 3
 WALK_NEGATIVE = 4
 WALK_POSITIVE = 5


class Animator:
    event_number: int
    frame_number: int
    state: AnimationStates

    def __init__(self, event_number, frame_number, state):
        self.event_number = event_number
        self.frame_number = frame_number
        self.state = state
        
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

 def get_velocity(self):
    return (self.v_x, self.v_y)

def get_animations(impath):
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
    return ANIMATIONS
