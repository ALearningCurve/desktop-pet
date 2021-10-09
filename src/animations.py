from enum import Enum
import tkinter as tk
import random
from itertools import repeat
import pathlib
import os


class Canvas:
    """Represents information on the tkinter window and label as well as information of the
    desktop's width and height, aka resolution
    """

    window: tk.Tk
    label: tk.Label
    resolution: any

    def __init__(self, window, label, resolution):
        """
        Args:
            window (tkinter.Tk)
            label (tkinter.Label)
            resolution (dict[str, int]): must have "width" and "height" as keys
        """
        self.window = window
        self.label = label
        self.resolution = resolution

    def __repr__(self):
        return f"<Canvas:c width {self.resolution['width']}px and height {self.resolution['height']}px>"


class AnimationStates(Enum):
    """Represents all the possible animation states for our desktop pet"""

    IDLE = 0
    IDLE_TO_SLEEP = 1
    SLEEP = 2
    SLEEP_TO_IDLE = 3
    WALK_NEGATIVE = 4
    WALK_POSITIVE = 5
    GRABBED = 6
    FALLING = 7
    LANDED = 8


class Animation:
    """Defines the event numbers for this animation
    and the ways this animation can transfer to the
    next animation
    """

    next_animation_states: list[AnimationStates]
    """possible animations for after this animation"""
    frames: list
    """List of frames in the animation"""
    frame_timer: int
    """time in between every frame of the animation"""
    v_x: int
    v_y: int
    repititions: int  
    """ How many times to repeat given animation before moving onto the next animation """

    def __init__(
        self,
        next_animation_states,
        frames,
        frame_timer=100,
        v_x=0,
        v_y=0,
        repititions=0,
        frame_multiplier=1,
    ):
        """
        Args:
            next_animation_states (list[Animations]): possible animations for this animation
            to transition to once this animation finishes
            frames (list[tk.PhotoImage]): frames of images that can be rendered by tkinter
            frame_timer (int, optional): time in between every frame of the animation. Defaults to 100.
            v_x (int, optional): change in x for every frame of the animation. Defaults to 0.
            v_y (int, optional): change in y for every frame of the animation. Defaults to 0.
            repititions (int, optional): how many times this animation should repeat before transitioning to the next animation. Defaults to 0.
            frame_multiplier (int, optional): how many times to duplicate frames in the frames array. This is useful for really
            fast animations (ie have low frame_timer) to keep the animation updating position but not spazzing out the sprite. Defaults to 1.
        """
        self.next_animation_states = next_animation_states
        self.frame_timer = frame_timer
        self.frames = [x for item in frames for x in repeat(item, frame_multiplier)]
        self.v_x = v_x
        self.v_y = v_y
        self.repititions = repititions

    def next(self, animator) -> AnimationStates:
        """Provides the next animation after this animation finishes. If there are repitions, then it will repeat until
        all the repitions are complete before transitionaing

        Args:
            animator (Animator)

        Returns:
            AnimationStates
        """
        if animator.repititions < self.repititions:
            animator.repititions += 1
            return animator.state
        else:
            animator.repititions = 0
        return random.choice(self.next_animation_states)

    def get_velocity(self) -> tuple[int, int]:
        """returns the change in position that this animation expects

        Returns:
            tuple[int, int]: change in x, change in y
        """
        return (self.v_x, self.v_y)

    def load_frames(self):
        #TODO: implement
        pass

    def __repr__(self):
        return f"<Animation: {len(self.frames)} frames each at {self.frame_timer} ms>"


class Animator:
    """Holds information that is needed to play animations 
    """
    frame_number: int
    """Current frame of the animation"""
    state: AnimationStates
    """Current animation state (ie the animation that should be playing"""
    animations: dict[AnimationStates, Animation]
    """All supported animations"""
    repititions: int
    """The current repitition of an animation that this is on"""

    def __init__(self, frame_number: int, state: AnimationStates, animations: dict[AnimationStates, Animation], repititions = 0):
        """
        Args:
            frame_number (int): Current frame number of the animation
            state (AnimationStates): Current animation state
            animations (dict[AnimationStates, Animation]): All possible animations to choose from
            repititions (int): The current repitation of a animation that we are on. Defaults to 0.
        """
        self.frame_number = frame_number
        self.state = state
        self.animations = animations
        self.repititions = repititions

    def set_state(self, state: AnimationStates) -> None:
        """Update the state and reset variables that change with each animation

        Args:
            state (AnimationStates): state to set
        """
        # If the state is the same, then do nothing
        # As we don't want the animation to keep reseting
        if state == self.state:
            return
        self.frame_number = 0
        self.state = state

    def __repr__(self):
        return f"<Animator: {str(self.state)} on frame {self.frame_number}>"


def get_animations() -> dict[AnimationStates, Animation]:
    """Loads all of the animations and their source files into a dictionary

    Returns:
        dict[AnimationStates, Animation]
    """
    # Load the animation gifs from the sprite folder and make each of the gifs into a list of frames
    # Path to sprites we want to use
    impath = pathlib.Path().resolve()
    _ = os.path.join
    impath = _(impath, "src", "sprites", "cat")

    # Convert into frames
    idle_frames = [
        tk.PhotoImage(file=_(impath, "idle.gif"), format="gif -index %i" % (i))
        for i in range(5)
    ] 
    idle_to_sleep_frames = [
        tk.PhotoImage(file=_(impath, "idle_to_sleep.gif"), format="gif -index %i" % (i))
        for i in range(8)
    ] 
    sleep_frames = [
        tk.PhotoImage(file=_(impath, "sleep.gif"), format="gif -index %i" % (i))
        for i in range(3)
    ] 
    sleep_to_idle_frames = [
        tk.PhotoImage(file=_(impath, "sleep_to_idle.gif"), format="gif -index %i" % (i))
        for i in range(8)
    ] 
    walk_positive_frames = [
        tk.PhotoImage(
            file=_(impath, "walking_positive.gif"), format="gif -index %i" % (i)
        )
        for i in range(8)
    ]
    walk_negative_frames = [
        tk.PhotoImage(
            file=_(impath, "walking_negative.gif"), format="gif -index %i" % (i)
        )
        for i in range(8)
    ] 

    standing_actions = [AnimationStates.IDLE_TO_SLEEP]
    standing_actions.extend(repeat(AnimationStates.IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.WALK_NEGATIVE, 4))
    standing_actions.extend(repeat(AnimationStates.WALK_POSITIVE, 4))

    # These are the animations that our spite can do. There should be one animation for 
    # each of the AnimationStates
    # TODO: Make it so that loads gif on init rather than having two seperate steps
    ANIMATIONS: dict[AnimationStates, Animation] = {
        AnimationStates.IDLE: Animation(standing_actions, idle_frames, frame_timer=400),
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP], idle_to_sleep_frames
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            sleep_frames,
            frame_timer=1000,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation([AnimationStates.IDLE], sleep_to_idle_frames),
        AnimationStates.WALK_POSITIVE: Animation(
            standing_actions, walk_positive_frames, v_x=3
        ),
        AnimationStates.WALK_NEGATIVE: Animation(
            standing_actions, walk_negative_frames, v_x=-3
        ),
        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED], walk_positive_frames, frame_timer=50
        ),
        AnimationStates.FALLING: Animation(
            [AnimationStates.FALLING], walk_negative_frames, frame_timer=10, frame_multiplier=2
        ),
    }
    ANIMATIONS[AnimationStates.LANDED] = ANIMATIONS[AnimationStates.IDLE]

    assert len(AnimationStates) == len(ANIMATIONS.keys())
    return ANIMATIONS
