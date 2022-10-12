from enum import Enum, auto


class AnimationStates(Enum):
    """Represents all the possible animation states for our desktop pet"""

    # Recommended all pets have these first few states
    IDLE = "idle"
    IDLE_TO_SLEEP = auto()
    SLEEP_TO_IDLE = auto()
    SLEEP = auto()
    WALK_NEGATIVE = auto()
    WALK_POSITIVE = auto()
    IDLE_TO_GRABBED = auto()  # OPTIONAL
    GRABBED = auto()
    GRAB_TO_FALL = auto()  # OPTIONAL
    FALLING = auto()
    LANDED = auto()

    ### These are some states specific for some pets
    ## Horse specific states
    GRAZING_START = auto()
    GRAZING_END = auto()
    GRAZING = auto()
