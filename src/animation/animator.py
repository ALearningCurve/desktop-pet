from typing import Dict
from src import logger
from .animation_states import AnimationStates
from .animation import Animation


class Animator:
    """Holds information that is needed to play animations"""

    frame_number: int
    """Current frame of the animation"""
    state: AnimationStates
    """Current animation state (ie the animation that should be playing"""
    animations: Dict[AnimationStates, Animation]
    """All supported animations"""
    repititions: int
    """The current repitition of an animation that this is on"""

    def __init__(
        self,
        frame_number: int,
        state: AnimationStates,
        animations: Dict[AnimationStates, Animation],
        repititions=0,
    ):
        """
        Args:
            frame_number (int): Current frame number of the animation
            state (AnimationStates): Current animation state
            animations (Dict[AnimationStates, Animation]): All possible animations to choose from
            repititions (int): The current repitation of a animation that we are on. Defaults to 0.
        """
        self.frame_number = frame_number
        self.state = state
        self.animations = animations
        self.repititions = repititions

    def set_animation_state(self, state: AnimationStates) -> bool:
        """Update the state and reset variables that change with each animation

        Args:
            state (AnimationStates): state to set

        Returns: Whether or not the state was changed
        """
        # If the state is the same, then do nothing
        # As we don't want the animation to keep reseting
        logger.debug(f"{self.state.__repr__()} changing to {state.__repr__()}")
        if state == self.state:
            return False
        self.frame_number = 0
        self.repititions = 0
        self.state = state
        return True

    def __repr__(self):
        return f"<Animator: {str(self.state)} on frame {self.frame_number}>"
