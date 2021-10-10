import tkinter as tk
from src.animations import Animation, AnimationStates, Canvas, Animator

# ! IMPORTANT:
# ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in its animator.animations dict for 
# ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
# ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations 
# ! other animations are repurposed for these animation states.
class Pet:
    """Represents a Virtual Desktop Pet that has animations, basic physics, can be picked up, and will stay on screen.
    This class can use a variety of diferent animations as definied in its animator.
    """

    """ Pixel size of the pet's gif """
    x: int
    y: int
    v_y: float = 0
    a_y: float = 0.3
    canvas: Canvas
    animator: Animator

    def __init__(self, x, y, canvas, animator):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.animator = animator

    def do_movement(self):
        """Keep the pet on the screen and if the pet is in the air, then make the pet fall down to the "floor"
        """
        # check and move x to be on screen
        size = self.animator.animations[self.animator.state].target_resolution
        if self.x < 0:
            self.x = size[0]
        if self.x > self.canvas.resolution["width"] - size[0]:
            self.x = self.canvas.resolution["width"] - size[0]

        # do stuff with the y position
        # to make sure the pet falls to ground and is not off the bottom of the screen
        if self.y > self.canvas.resolution["height"]:
            self.y = self.canvas.resolution["height"]
            if self.animator.state == AnimationStates.FALLING:
                self.v_y = 0
                if AnimationStates.LANDED in self.animator.animations:
                    self.animator.set_state(AnimationStates.LANDED)

        if self.animator.state == AnimationStates.FALLING:
            self.v_y += self.a_y
            self.y += self.v_y
            self.y = int(self.y)

    def update(self):
        """Move the pet according to the animation and physics as well as progressing to the next frame of the animation
        """
        animation = self.get_current_animation()
        x, y = animation.get_velocity()
        self.x += x
        self.y += y
        self.do_movement()
        self.progress_animation()

    def draw(self) -> tk.PhotoImage:
        """Ussing the 

        Returns:
            tk.PhotoImage: image of animation to draw
        """
        animation = self.get_current_animation()
        return animation.frames[self.animator.frame_number]

    def on_tick(self):
        """Draw the current animation"""
        self.update()
        frame = self.draw()
        self.set_geometry()
        self.canvas.label.configure(image=frame)
        self.canvas.window.after(1, self.handle_event)

    # transfer random no. to event
    def handle_event(self):
        """Part of animation loop, after delay between frames in animation
        proceed to begin logic of drawing next frame

        Raises:
            Exception: [description]
        """
        self.canvas.window.after(
            self.animator.animations[self.animator.state].frame_timer, self.on_tick
        )

    # making gif work
    def progress_animation(self):
        """Move the animation forward one frame. If the animation has finished (ie current frame is
        the last frame) then try to progress to the next animation
        """
        animation = self.get_current_animation()
        if self.animator.frame_number < len(animation.frames) - 1:
            self.animator.frame_number += 1
        else:
            self.animator.frame_number = 0
            self.animator.set_state(animation.next(self.animator))

    #   print(self.animator.state, self.animator.frame_number)

    def get_current_animation(self) -> Animation:
        """Returns the current animation of the Pet instance

        Returns:
            Animation
        """
        return self.animator.animations[self.animator.state]



    def set_geometry(self):
        """Update the window position and scale to match that of the pet instance's location and size
        """
        size = self.animator.animations[self.animator.state].target_resolution
        self.canvas.window.geometry(
            str(size[0]) + "x" + str(size[1]) + "+" + str(self.x) + "+" + str(self.y)
        )
    
    def __repr__(self):
        size = self.animator.animations[self.animator.state].target_resolution
        return f"<VirtualPet of {size[0]}x{size[1]} at ({self.x}, {self.y}) using {str(self.animator)} and {str(self.canvas)}>"

    #################################################### Event Handlers
    def start_move(self, event):
        """ Mouse 1 click """
        if AnimationStates.GRABBED in self.animator.animations:
            self.animator.set_state(AnimationStates.GRABBED)
        self.v_y = 0
    def stop_move(self, event):
        """ Mouse 1 release """
        if AnimationStates.GRABBED in self.animator.animations:
            self.animator.set_state(AnimationStates.FALLING)

    def do_move(self, event):
        """ Mouse movement while clicked """
        self.progress_animation()
        self.x = event.x_root
        self.y = event.y_root
        self.v_y = 0
        self.set_geometry()
