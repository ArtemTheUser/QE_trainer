import os
from typing import Literal

import customtkinter as ctk
from PIL import Image

from ..ctk_moving_frame import CTkMovingFrame

from backend.handlers import resource_path


def _load_image_by_mood(
        directory: Literal['blue_pi', 'brown_pi'],
        chosen_mood) -> Image:
    dirname = os.path.dirname
    join = os.path.join

    img_dir = join(dirname(os.path.relpath(__file__)), directory)

    for img in os.listdir(img_dir):
        mood = img.split('.')[0]

        if mood == chosen_mood:
            return Image.open(
                resource_path(join(img_dir, img))
            )


class BluePi(CTkMovingFrame):
    def __init__(
            self,
            master,
            mood: Literal[
                'thinking_1', 'thinking_2',
                'confused_1', 'confused_2',
                'smiley_1', 'smiley_2',
                'indifferent', 'happy',
            ],
            width,  # width & height will be passen into image size
            height,
            fg_color='transparent',
            **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.mood = mood
        self.width = width
        self.height = height

        image = _load_image_by_mood('blue_pi', self.mood)

        self.label = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=image,
                size=(self.width, self.height)
            ),
        )
        self.label.grid()


class BrownPi(CTkMovingFrame):
    def __init__(
            self,
            master,
            mood: Literal['speaking', 'showing', 'showing_reversed', 'smiley_1',
                          'smiley_2', 'dunno', 'thinking', 'indifferent'],
            width,
            height,
            fg_color='transparent',
            **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.mood = mood
        self.width = width
        self.height = height

        image = _load_image_by_mood('brown_pi', self.mood)

        self.label = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=image,
                size=(self.width, self.height)
            ),
        )
        self.label.grid()
