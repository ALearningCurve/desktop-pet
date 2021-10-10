from enum import Enum
import tkinter as tk
import random
from itertools import repeat
import pathlib
import os
from os import listdir
from os.path import isfile, join
from PIL import Image


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
    target_resolution: tuple[int, int]

    def __init__(
        self,
        next_animation_states,
        frames: list = None,
        gif_location: str = None,
        image_location: str = None,
        frame_timer=100,
        v_x=0,
        v_y=0,
        repititions=0,
        frame_multiplier=1,
        target_resolution: tuple[int, int] = (100, 100)
    ):
        """
        Args:
            next_animation_states (list[Animations]): possible animations for this animation
            to transition to once this animation finishes
            frames (list[tk.PhotoImage], optional): frames of images that can be rendered by tkinter. Defaults to None.
            gif_location (str, optional): Absolute path to the gif to convert into frames. Defaults to None.
            image_location (str, optional): Absolute path to the images folder to load into frames list. Defaults to None.
            target_resolution (tuple[int, int], optional): Resolution of the frames of the animation, when drawn the canvas will be this big.
            target_resolution[0] is x width, and target_resolution[1] is y width. Defaults to (100, 100).
            frame_timer (int, optional): time in between every frame of the animation. Defaults to 100.
            v_x (int, optional): change in x for every frame of the animation. Defaults to 0.
            v_y (int, optional): change in y for every frame of the animation. Defaults to 0.
            repititions (int, optional): how many times this animation should repeat before transitioning to the next animation. Defaults to 0.
            frame_multiplier (int, optional): how many times to duplicate frames in the frames array. This is useful for really
            fast animations (ie have low frame_timer) to keep the animation updating position but not spazzing out the sprite. Defaults to 1.
        
        """
        self.next_animation_states = next_animation_states
        self.frame_timer = frame_timer
        self.v_x = v_x
        self.v_y = v_y
        self.repititions = repititions

        # Get and set the frames
        # Make sure that we have only one source for the frames
        if frames is None:
            if gif_location is not None:
                frames = Animation.load_gif_to_frames(gif_location)
            elif image_location is not None:
                frames = Animation.load_images_to_frames(image_location)
            else:
                raise Exception("Recieved neither the frames or locations to load the frames. Could not make animation")
        if len(frames) == 0:
            raise Exception("There must be a least one frame in the frames list")

        self.target_resolution = target_resolution
        # TODO: Fix so it applies the scaling of the resolution
        frames = Animation.apply_target_resolution(frames, target_resolution)
        self.frames = [x for item in frames for x in repeat(item, frame_multiplier)]
            
    @staticmethod
    def load_gif_to_frames(path: str) -> list[tk.PhotoImage]:
        """Given a path to a .gif file create and load the frames in the gif. Returns the frames of GIF as a list

        Args:
            path (str) Path to the gif file

        Returns:
            list[tk.PhotoImage]: List of images of the frames in the gif
        """

        file = Image.open(path)
        number_of_frames = file.n_frames
        file.close()

        frames = [
            tk.PhotoImage(file=path, format="gif -index %i" % (i))
            for i in range(number_of_frames)
        ]
        return frames
    
    @staticmethod
    def load_images_to_frames(path: str ):
        files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        frames = [
            tk.PhotoImage(file=path)
            for path in files        
        ]
        return frames

    @staticmethod
    def apply_target_resolution(frames: list[tk.PhotoImage], target_resolution: tuple[int, int]) -> list[tk.PhotoImage]:
        """Given a list of frames, scale it to a certain resolution

        Args:
            frames (list[tk.PhotoImage]) List of frames to alter
            target_resolution (tuple[int, int]) scale to apply where tuple[0] is x width and tuple[1] is y width


        Returns:
            list[tk.PhotoImage]: List of images of the frames in the gif
        """
        
        for i in range(len(frames)):
            image = frames[i]
            scale_w = target_resolution[0]/image.width()
            scale_h = target_resolution[1]/image.height()
            print(scale_w, scale_h)
            # downscale
            if scale_w < 1:
                print
                image = image.subsample(int(1/scale_w), 1)
            # upscale
            elif scale_w > 1:
                image = image.zoom(int(scale_w), 1)
            # downscale
            if scale_h < 1:
                image = image.subsample(1, int(1/scale_h))
            # upscale
            elif scale_h > 1:
                image = image.zoom(1, int(scale_h))
            # image.zoom(scale_w, scale_h)
            frames[i] = image
        return frames

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

    def __repr__(self):
        return f"<Animation: {len(self.frames)} frames each at {self.frame_timer} ms>"


class Animator:
    """Holds information that is needed to play animations"""

    frame_number: int
    """Current frame of the animation"""
    state: AnimationStates
    """Current animation state (ie the animation that should be playing"""
    animations: dict[AnimationStates, Animation]
    """All supported animations"""
    repititions: int
    """The current repitition of an animation that this is on"""

    def __init__(
        self,
        frame_number: int,
        state: AnimationStates,
        animations: dict[AnimationStates, Animation],
        repititions=0,
    ):
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


def get_animations(pet_name: str = "cat") -> dict[AnimationStates, Animation]:
    """Loads all of the animations for a pet and their source files into a dictionary
    Args:
        pet_name (str): name of the pet, ie the name of folder its animations are in 
    Returns:
        dict[AnimationStates, Animation]
    """
    # Load the animation gifs from the sprite folder and make each of the gifs into a list of frames
    # Path to sprites we want to use
    impath = pathlib.Path().resolve()
    impath = os.path.join(impath, "src", "sprites")

    # **** This can be whatever set of animations you want it to be
    # **** I just like horses so I have set it to that
    animations = get_horse_animations(impath)

    return animations


def get_cat_animations(impath:str):
    """Loads all of the animations for a cat
    Args:
        impath (str): path to the folder the animations are in
    Returns:
        dict[AnimationStates, Animation]
    """
    pj = os.path.join
    impath = pj(impath, "cat")
    standing_actions = [AnimationStates.IDLE_TO_SLEEP]
    standing_actions.extend(repeat(AnimationStates.IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.WALK_NEGATIVE, 4))
    standing_actions.extend(repeat(AnimationStates.WALK_POSITIVE, 4))

    # These are the animations that our spite can do.
    # ! IMPORTANT:
    # ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in the animations dict for 
    # ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
    # ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations 
    # ! other animations are repurposed for these animation states.
    animations: dict[AnimationStates, Animation] = {
        AnimationStates.IDLE: Animation(
            standing_actions, 
            gif_location=pj(impath, "idle.gif"), 
            frame_timer=400
        ),
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP], 
            gif_location=pj(impath, "idle_to_sleep.gif")
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            gif_location=pj(impath, "sleep.gif"),
            frame_timer=1000,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            [AnimationStates.IDLE], 
            gif_location=pj(impath, "sleep_to_idle.gif")
        ),
        AnimationStates.WALK_POSITIVE: Animation(
            standing_actions,
            gif_location=pj(impath, "walking_positive.gif"), 
            v_x=3
        ),
        AnimationStates.WALK_NEGATIVE: Animation(
            standing_actions, 
            gif_location=pj(impath, "walking_negative.gif"), 
            v_x=-3
        ),
        # There is no grabbed gif, so just speed up the walking gif
        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED],
            gif_location=pj(impath, "walking_positive.gif"),
            frame_timer=50,
        ),
        # There is no falling gif, so just speed up the walking gif
        # but as position updates after every frame of animation, incease 
        # update speed to be smoother (increase duplicate frames to prevent)
        # spazzing looking cat
        AnimationStates.FALLING: Animation(
            [AnimationStates.FALLING],
            gif_location=pj(impath, "walking_negative.gif"),
            frame_timer=10,
            frame_multiplier=2,
        ),
    }
    # No landed animation, but instead return the cat to its idle animation so that 
    # it can go to a next animation state after falling
    animations[AnimationStates.LANDED] = animations[AnimationStates.IDLE]
    return animations


def get_horse_animations(impath:str):
    """Loads all of the animations for a horse
    Args:
        impath (str): path to the folder the animations are in
    Returns:
        dict[AnimationStates, Animation]
    """
    pj = os.path.join
    impath = pj(impath, "horse")
    resolution = (400, 400)
    # These are the animations that our spite can do. 
    # ! IMPORTANT:
    # ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in the animations dict for 
    # ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
    # ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations 
    # ! other animations are repurposed for these animation states.
    animations: dict[AnimationStates, Animation] = {
        AnimationStates.IDLE: Animation(
            [AnimationStates.IDLE], 
            gif_location=pj(impath, "idle.gif"), 
            frame_timer=400,
            target_resolution=resolution
        )
    }
    return animations
