import random
import tkinter as tk
from animations import Animation, AnimationStates, Canvas, Animator


class Pet:
    """Represents a Virtual Desktop Pet that has animations, basic physics, can be picked up, and will stay on screen
    """
    size = 100
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
        if self.x < 0:
            self.x = Pet.size
        if self.x > self.canvas.resolution["width"] - Pet.size:
            self.x = self.canvas.resolution["width"] - Pet.size

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
        self.canvas.window.geometry(
            str(Pet.size) + "x" + str(Pet.size) + "+" + str(self.x) + "+" + str(self.y)
        )
    
    def __repr__(self):
        return f"<VirtualPet of {Pet.size}x{Pet.size} at ({self.x}, {self.y}) using {str(self.animator)} and {str(self.canvas)}>"

    #################################################### Event Handlers
    def start_move(self, event):
        """ Mouse 1 click """
        self.animator.set_state(AnimationStates.GRABBED)
        self.v_y = 0
    def stop_move(self, event):
        """ Mouse 1 release """
        self.animator.set_state(AnimationStates.FALLING)

    def do_move(self, event):
        """ Mouse movement while clicked """
        self.progress_animation()
        self.x = event.x_root
        self.y = event.y_root
        self.v_y = 0
        self.set_geometry()
