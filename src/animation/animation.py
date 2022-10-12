import tkinter as tk
import random
from itertools import repeat
from os import listdir
from os.path import isfile, join
from typing import Tuple
from typing import List
from PIL import Image
from src import logger
from .animation_states import AnimationStates


class Animation:
    """Defines the event numbers for this animation
    and the ways this animation can transfer to the
    next animation
    """

    next_animation_states: List[AnimationStates]
    """possible animations for after this animation"""
    frames: list
    """List of frames in the animation"""
    frame_timer: int
    """time in between every frame of the animation. Should be at most 100ms, otherwise time between
    updates will be too long and will appear laggy. To achieve slower animation at 100ms (or less) user
    frame_multiplier function in init method. (by default if frame_timer>100 then frame_multipler will
    be applied automatically to keep same time between visual image changes (see __init__)"""
    v_x: int
    v_y: int
    a_x: int
    a_y: int
    repititions: int
    """ How many times to repeat given animation before moving onto the next animation """
    target_resolution: Tuple[int, int]

    should_run_preprocessing = False
    """Whether or not to run preprocessing, overwrites saved images. Defaults to False"""

    def __init__(
        self,
        next_animation_states,
        name: str = None,
        frames: list = None,
        gif_location: str = None,
        images_location: str = None,
        frame_timer=100,
        v_x: float = 0,
        v_y: float = 0,
        a_x: float = 0,
        a_y: float = 0,
        repititions: int = 0,
        frame_multiplier: int = 1,
        target_resolution: Tuple[int, int] = (100, 100),
        reverse: bool = False,
    ):
        """
        Args:
            next_animation_states (List[Animations]): possible animations for this animation
            to transition to once this animation finishes
            name (str, optional): The verbose name of this animation
            frames (List[tk.PhotoImage], optional): frames of images that can be rendered by tkinter. Defaults to None.
            gif_location (str, optional): Absolute path to the gif to convert into frames. Defaults to None.
            images_location (str, optional): Absolute path to the images folder to load into frames list. Defaults to None.
            target_resolution (Tuple[int, int], optional): Resolution of the frames of the animation, when drawn the canvas will be this big.
            target_resolution[0] is x width, and target_resolution[1] is y width. Defaults to (100, 100).
            frame_timer (int, optional): time in between every frame of the animation. Defaults to 100.
            v_x (float, optional): change in x for every frame of the animation. Defaults to 0.
            v_y (float, optional): change in y for every frame of the animation. Defaults to 0.
            a_x (float, optional): change in v_x for every frame of the animation. Defaults to 0.
            a_y (float, optional): change in v_y for every frame of the animation. Defaults to 0.
            repititions (int, optional): how many times this animation should repeat before transitioning to the next animation. Defaults to 0.
            frame_multiplier (int, optional): how many times to duplicate frames in the frames array. This is useful for really
            fast animations (ie have low frame_timer) to keep the animation updating position but not spazzing out the sprite. Defaults to 1.
            if None will duplicate frames to keep updating animation automatically every 100 ms. (Prevents "laggy" mouse interactions)
            reverse (bool, optional): Wether or not to reverse the loaded frames (useful for transition animations)
        """
        self.next_animation_states = next_animation_states
        self.frame_timer = frame_timer
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = a_x
        self.a_y = a_y
        self.repititions = repititions

        # Get and set the frames
        # Make sure that we have only one source for the frames
        if name is None:
            name = gif_location.split("src").pop() if gif_location is not None else name
            name = (
                images_location.split("src").pop()
                if images_location is not None
                else name
            )
        self.name = name
        logger.info(f"Loading Animation: {self.name}")
        if frames is None:
            if gif_location is not None:
                frames = Animation.load_gif_to_frames(gif_location)
            elif images_location is not None:
                frames = Animation.load_images_to_frames(images_location)
            else:
                raise Exception(
                    "Recieved neither the frames or locations to load the frames. Could not make animation"
                )
        if len(frames) == 0:
            raise Exception("There must be a least one frame in the frames list")

        self.target_resolution = target_resolution
        frames = Animation.apply_target_resolution(frames, target_resolution)

        if reverse:
            frames.reverse()

        # We want the animation to be updating at least every 100 ms
        # so if the frame_timer is greater than 100ms, then reduce it to be around 100ms
        # by increasing the amount of frames
        if self.frame_timer > 100:
            frame_multiplier = (
                round(frame_timer / 100) * frame_multiplier
            )  # Keep the original multiplier as a factor
            self.frame_timer = 100
            logger.warning(
                f"frame_timer is too long in {self.name}! Setting timer to 100ms, \
                but increasing frames by a factor of {frame_multiplier}"
            )

        self.frames = [x for item in frames for x in repeat(item, frame_multiplier)]

    @staticmethod
    def load_gif_to_frames(path: str) -> List[tk.PhotoImage]:
        """Given a path to a .gif file create and load the frames in the gif. Returns the frames of GIF as a list

        Args:
            path (str) Path to the gif file

        Returns:
            List[tk.PhotoImage]: List of images of the frames in the gif
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
    def load_images_to_frames(path: str) -> List[tk.PhotoImage]:
        """Take the images, preferably png, from a source folder, path, and then convert them to
        Tkinter images

        Args:
            path (str): Path to the folder with the images
            preprocessor (Callable, optional): function to handle image conversions before adding them
            to the array (such as removing transparency). Defaults to None

        Returns:
            List[tk.PhotoImage]: [description]
        """

        # Get all the images from the folder and sort alphabetically
        files = [
            join(path, f)
            for f in sorted(listdir(path))
            if (isfile(join(path, f)) and f.split(".").pop().lower() == "png")
        ]
        if Animation.should_run_preprocessing:
            for path in files:
                Animation.remove_partial_transparency_png(path)

        frames = [tk.PhotoImage(file=path) for path in files]
        return frames

    @staticmethod
    def apply_target_resolution(
        frames: List[tk.PhotoImage], target_resolution: Tuple[int, int]
    ) -> List[tk.PhotoImage]:
        """Given a list of frames, scale it to a certain resolution

        Args:
            frames (List[tk.PhotoImage]) List of frames to alter
            target_resolution (Tuple[int, int]) scale to apply where Tuple[0] is x width and Tuple[1] is y width


        Returns:
            List[tk.PhotoImage]: List of images of the frames in the gif
        """

        for i in range(len(frames)):
            image = frames[i]
            scale_w = target_resolution[0] / image.width()
            scale_h = target_resolution[1] / image.height()
            # downscale
            if scale_w < 1:
                image = image.subsample(int(1 / scale_w), 1)
            # upscale
            elif scale_w > 1:
                image = image.zoom(int(scale_w), 1)
            # downscale
            if scale_h < 1:
                image = image.subsample(1, int(1 / scale_h))
            # upscale
            elif scale_h > 1:
                image = image.zoom(1, int(scale_h))
            # image.zoom(scale_w, scale_h)
            frames[i] = image
        return frames

    def remove_partial_transparency_png(path: str) -> Image:
        """Given a path to a png, try to force all data to be either completly transparent
        or completly opaque. Saves image when done editing the image

        Args:
            path (str): absolute path to the file
        """
        logger.info("START:remove_partial_transparency_png -> " + path)
        # We assume that the data is a png
        png = Image.open(path)
        # Just return the image if it is not a png, we don't know the format otherwise
        if path.split(".").pop().lower() != "png":
            return png

        png = png.convert("RGBA")

        # alpha_composite = Image.alpha_composite(background, png).show()
        # alpha_composite.save('foo.jpg', 'JPEG', quality=80)
        datas = png.getdata()

        newData = []
        for item in datas:
            if item[3] != 255:
                newData.append((item[0], item[1], item[2], round(item[3] / 255) * 255))
            else:
                newData.append(item)

        png.putdata(newData)
        png.save(path, path.split(".").pop())
        return png

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

    def get_velocity(self) -> Tuple[int, int]:
        """returns the change in position that this animation expects

        Returns:
            Tuple[int, int]: change in x, change in y
        """
        return (self.v_x, self.v_y)

    def get_acceleration(self) -> Tuple[int, int]:
        """returns the change in velocity that this animation expects

        Returns:
            Tuple[int, int]: change in v_x, change in v_y
        """
        return (self.a_x, self.a_y)

    def __repr__(self):
        return f"<Animation: {len(self.frames)} frames each at {self.frame_timer} ms>"
