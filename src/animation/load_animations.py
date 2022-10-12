from itertools import repeat
import pathlib
import os
from typing import Tuple, Dict
from .animation_states import AnimationStates
from .animation import Animation


def get_animations(
    pet_name: str, target_resolution: Tuple[int, int], should_run_preprocessing: bool
) -> Dict[AnimationStates, Animation]:
    """Loads all of the animations for a pet and their source files into a dictionary
    Args:
        pet_name (str): name of the pet, ie the name of folder its animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    # Load the animation gifs from the sprite folder and make each of the gifs into a list of frames
    # Path to sprites we want to use
    impath = pathlib.Path().resolve()
    impath = os.path.join(impath, "src", "sprites")
    Animation.should_run_preprocessing = should_run_preprocessing
    # **** This can be whatever set of animations you want it to be
    # **** I just like horses so I have set it to that
    if pet_name == "cat":
        animations = get_cat_animations(impath, target_resolution)
    elif pet_name == "horse":
        animations = get_horse_animations(impath, target_resolution)

    return animations


def get_cat_animations(impath: str, target_resolution: Tuple[int, int]):
    """Loads all of the animations for a cat
    Args:
        impath (str): path to the folder the animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
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
    animations: Dict[AnimationStates, Animation] = {
        AnimationStates.IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "idle.gif"),
            frame_timer=400,
            target_resolution=target_resolution,
        ),
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP],
            gif_location=pj(impath, "idle_to_sleep.gif"),
            target_resolution=target_resolution,
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
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            [AnimationStates.IDLE],
            gif_location=pj(impath, "sleep_to_idle.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_POSITIVE: Animation(
            standing_actions,
            gif_location=pj(impath, "walking_positive.gif"),
            v_x=3,
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_NEGATIVE: Animation(
            standing_actions,
            gif_location=pj(impath, "walking_negative.gif"),
            v_x=-3,
            target_resolution=target_resolution,
        ),
        # There is no grabbed gif, so just speed up the walking gif
        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED],
            gif_location=pj(impath, "walking_positive.gif"),
            frame_timer=50,
            target_resolution=target_resolution,
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
            target_resolution=target_resolution,
            a_y=2,
        ),
    }
    # No landed animation, but instead return the cat to its idle animation so that
    # it can go to a next animation state after falling
    animations[AnimationStates.LANDED] = animations[AnimationStates.IDLE]
    return animations


def get_horse_animations(impath: str, target_resolution: Tuple[int, int]):
    """Loads all of the animations for a horse
    Args:
        impath (str): path to the folder the animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    pj = os.path.join
    impath = pj(impath, "horse", "Horse")
    standing_actions = [AnimationStates.IDLE_TO_SLEEP, AnimationStates.GRAZING_START]
    standing_actions.extend(repeat(AnimationStates.IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.WALK_NEGATIVE, 5))
    standing_actions.extend(repeat(AnimationStates.WALK_POSITIVE, 5))

    # These are the animations that our spite can do.
    # ! IMPORTANT:
    # ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in the animations dict for
    # ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
    # ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations
    # ! other animations are repurposed for these animation states.
    animations: Dict[AnimationStates, Animation] = {
        ######### IDLE
        AnimationStates.IDLE: Animation(
            standing_actions,
            images_location=pj(impath, "Idle", "Right"),
            target_resolution=target_resolution,
            repititions=3,
        ),
        ######### SLEEP
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP],
            images_location=pj(impath, "Sleep", "IdleToSleep"),
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            images_location=pj(impath, "Sleep", "Sleeping"),
            frame_timer=1000,
            repititions=2,
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            [AnimationStates.IDLE],
            images_location=pj(impath, "Sleep", "IdleToSleep"),
            target_resolution=target_resolution,
            reverse=True,
        ),
        ######### WALKING
        AnimationStates.WALK_POSITIVE: Animation(
            standing_actions,
            images_location=pj(impath, "Walking", "Right"),
            v_x=3,
            repititions=7,
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_NEGATIVE: Animation(
            standing_actions,
            images_location=pj(impath, "Walking", "Left"),
            v_x=-3,
            repititions=7,
            target_resolution=target_resolution,
        ),
        ########## GRAZING
        AnimationStates.GRAZING_START: Animation(
            [AnimationStates.GRAZING],
            images_location=pj(impath, "Grazing", "Transition"),
            target_resolution=target_resolution,
        ),
        AnimationStates.GRAZING_END: Animation(
            standing_actions,
            images_location=pj(impath, "Grazing", "Transition"),
            target_resolution=target_resolution,
            reverse=True,
        ),
        AnimationStates.GRAZING: Animation(
            [AnimationStates.GRAZING, AnimationStates.GRAZING_END],
            images_location=pj(impath, "Grazing", "Active"),
            repititions=1,
            frame_timer=200,
            target_resolution=target_resolution,
        ),
        ########### MOUSE INTERACTIONS
        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED],
            images_location=pj(impath, "MouseInteractions", "Grabbed"),
            frame_timer=50,
            target_resolution=target_resolution,
        ),
        AnimationStates.GRAB_TO_FALL: Animation(
            [AnimationStates.FALLING],
            images_location=pj(impath, "MouseInteractions", "GrabToFall"),
            target_resolution=target_resolution,
        ),
        AnimationStates.FALLING: Animation(
            [AnimationStates.FALLING],
            images_location=pj(impath, "MouseInteractions", "Falling"),
            frame_timer=50,
            frame_multiplier=2,
            a_y=1,
            target_resolution=target_resolution,
        ),
        AnimationStates.LANDED: Animation(
            [AnimationStates.IDLE],
            images_location=pj(impath, "MouseInteractions", "Landed"),
            frame_timer=100,
            target_resolution=target_resolution,
        ),
    }

    return animations
