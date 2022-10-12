import tkinter as tk
from .animation import Animation, AnimationStates, Canvas, Animator
from src import logger

# ! IMPORTANT:
# ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in its animator.animations dict for
# ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
# ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations
# ! other animations are repurposed for these animation states.
class Pet:
    """Represents a Virtual Desktop Pet that has animations, basic physics, can be picked up, and will stay on screen.
    This class can use a variety of diferent animations as definied in its animator.
    """

    x: int
    y: int
    v_x: float = 0
    v_y: float = 0
    a_x: float = 0
    a_y: float = 0

    canvas: Canvas
    animator: Animator

    def __init__(self, x, y, canvas, animator):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.animator = animator

    def reset_movement(self):
        """Resets the movement information for the pet based on the current animation"""
        animation = self.get_current_animation()
        self.v_x, self.v_y = animation.get_velocity()
        self.a_x, self.a_y = animation.get_acceleration()

    def do_movement(self):
        """Keep the pet on the screen and if the pet is in the air, then make the pet fall down to the "floor" """
        # Update Position and Velocity
        self.v_x += self.a_x
        self.v_y += self.a_y
        self.x = int(self.x + self.v_x)
        self.y = int(self.y + self.v_y)

        logger.debug(
            f"Pet Anim/Movement: accel:({self.a_x}, {self.a_y}), vel:({self.v_x}, {self.v_y}), posn:({self.x}, {self.y}) anim:{self.get_current_animation().a_y}"
        )

        # check and move x to be on screen
        size = self.animator.animations[self.animator.state].target_resolution
        if self.x < 0:
            self.x = size[0]
        if self.x > self.canvas.resolution["width"] - size[0]:
            self.x = self.canvas.resolution["width"] - size[0]

        # do stuff with the y position
        # to make sure the pet falls to ground and is not off the bottom of the screen
        if self.y > self.canvas.resolution["height"] - size[1]:
            self.y = self.canvas.resolution["height"] - size[1]
            if self.animator.state == AnimationStates.FALLING:
                if AnimationStates.LANDED in self.animator.animations:
                    self.set_animation_state(AnimationStates.LANDED)
                else:
                    raise Exception(
                        "Stuck falling as no AnimationStates.LANDED is defined\
                        so the animation handler does not know how to transition out of the falling state! \
                        Define AnimationStates.LANDED to resolve this error."
                    )

    def update(self):
        """Move the pet according to the animation and physics as well as progressing to the next frame of the animation"""
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
            logger.debug("frame repeating")
            self.animator.frame_number += 1
        else:
            logger.debug("getting next state")
            self.animator.frame_number = 0
            self.set_animation_state(animation.next(self.animator))

        logger.debug(f"{self.animator.state.__repr__()}, {self.animator.frame_number}")

    def get_current_animation(self) -> Animation:
        """Returns the current animation of the Pet instance

        Returns:
            Animation
        """
        return self.animator.animations[self.animator.state]

    def set_animation_state(self, state: AnimationStates) -> bool:
        """Sets the animation state for this pet

        Args:
            state (AnimationStates): Animation state to try to set

        Returns:
            bool: Whether or not the state actually changed values
        """
        changed = self.animator.set_animation_state(state)
        if changed:
            self.reset_movement()
        return changed

    def set_geometry(self):
        """Update the window position and scale to match that of the pet instance's location and size"""
        size = self.animator.animations[self.animator.state].target_resolution
        self.canvas.window.geometry(
            str(size[0]) + "x" + str(size[1]) + "+" + str(self.x) + "+" + str(self.y)
        )

    def __repr__(self):
        size = self.animator.animations[self.animator.state].target_resolution
        return f"<VirtualPet of {size[0]}x{size[1]} at ({self.x}, {self.y}) using {str(self.animator)} and {str(self.canvas)}>"

    #################################################### Event Handlers
    def start_move(self, event):
        """Mouse 1 click"""
        # Try to visually indicate that the pet has been grabbed, but only
        # if the animation exists
        if AnimationStates.GRABBED in self.animator.animations:
            self.set_animation_state(AnimationStates.GRABBED)

    def stop_move(self, event):
        """Mouse 1 release"""
        # to transfer out of the falling state, there has to be a landed state. Do not go into the falling state unless
        # landed state and falling state are defined
        if (
            AnimationStates.FALLING in self.animator.animations
            and AnimationStates.LANDED in self.animator.animations
        ):
            # if transition animation, try to use it
            if AnimationStates.GRAB_TO_FALL in self.animator.animations:
                self.set_animation_state(AnimationStates.GRAB_TO_FALL)
            else:
                self.set_animation_state(AnimationStates.FALLING)
        else:
            logger.warning(
                f'AnimationStates.LANDED and/or AnimationStates.FALLING are not defined, the \
                pet cannot "fall" without these states being part of the pets animations!'
            )
            self.set_animation_state(AnimationStates.IDLE)

    def do_move(self, event):
        """Mouse movement while clicked"""
        # Get the resolution of the current animation
        size = self.animator.animations[self.animator.state].target_resolution

        # Get the location on the desktop (root) and center the transform in the
        # center of the frame (rather than the default top left corner)
        self.x = event.x_root - int(size[0] / 2)
        self.y = event.y_root - int(size[1] / 2)
        # Relocate the window on the screen to match
        self.set_geometry()
