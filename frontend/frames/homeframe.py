import os
import random

import customtkinter as ctk
from PIL import Image

from backend.handlers import Settings, resource_path

from ..assets import CTkMovingFrame, BluePi, BrownPi


class HomeFrame(CTkMovingFrame):
    def __init__(self, master, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.settings = Settings.create_settings()

        self._load_images()

        self.start_button = ctk.CTkButton(
            self,
            text='Начать тренировку',
            text_color=('gray20', 'gray90'),
            fg_color='transparent',
            border_width=1,
            border_color=('gray10', 'gray90'),
            hover_color=('gray85', 'gray20'),
            border_spacing=10,
            image=ctk.CTkImage(
                light_image=self.start_button_dark,
                dark_image=self.start_button_light,
            ),
            font=ctk.CTkFont(family='Book Antiqua'),
        )
        self.start_button.place(relx=.5, rely=.5, anchor='center')

        self.line_frame = _LineFrame(self, direction='down', until=.15,
                                     smooth_slowdown=True)

        self.logo_text = ctk.CTkLabel(
            self,
            text='Quadratic equation trainer',
            font=ctk.CTkFont(family='White Rabbit', size=25),
            text_color=('gray20', 'gray90'),
        )
        self.logo_text.place(relx=.5, rely=.25, anchor='center')

        moods = ['smiley_1', 'smiley_2', 'happy']
        random.shuffle(moods)
        self.smiley_1_blue_pi = BluePi(
            self,
            mood=moods[0],
            width=60,
            height=60,
            smooth_slowdown=True,
            direction='up',
            until=.825,
            frequency=.001,
        )
        self.smiley_2_blue_pi = BluePi(
            self,
            mood=moods[1],
            width=60,
            height=60,
            smooth_slowdown=True,
            direction='up',
            until=.825,
            frequency=.001,
        )
        self.happy_blue_pi = BluePi(
            self,
            mood=moods[2],
            width=60,
            height=60,
            smooth_slowdown=True,
            direction='up',
            until=.825,
            frequency=.001,
        )

        self.showing_brown_pi = BrownPi(
            self,
            mood='showing',
            width=100,
            height=100,
            smooth_slowdown=True,
            direction='left',
            until=.77,
            frequency=.0015,
        )

    def _place_line_frame(self):
        self.line_frame.place(relx=.5, rely=0, anchor='s')

    def place_smiley_1_blue_pi(self):
        self.smiley_1_blue_pi.place(relx=.08, rely=1, anchor='n')

    def place_smiley_2_blue_pi(self):
        self.smiley_2_blue_pi.place(relx=.23, rely=1, anchor='n')

    def place_happy_blue_pi(self):
        self.happy_blue_pi.place(relx=.38, rely=1, anchor='n')

    def place_showing_brown_pi(self):
        self.showing_brown_pi.place(relx=1, rely=.855, anchor='w')

    def _configure_starting_ui(self):
        if self.settings.get('last_open_frame') == 'settings':
            # place a bit earlier
            self.after(200, self.place_smiley_1_blue_pi)
            self.after(270, self.place_smiley_2_blue_pi)
            self.after(340, self.place_happy_blue_pi)

            self.after(400, self.place_showing_brown_pi)

            self.after(500, self._place_line_frame)
        else:
            self.after(580, self.place_smiley_1_blue_pi)
            self.after(680, self.place_smiley_2_blue_pi)
            self.after(750, self.place_happy_blue_pi)

            self.after(810, self.place_showing_brown_pi)

            self.after(1100, self._place_line_frame)

    def _load_images(self):
        dirname = os.path.dirname
        join = os.path.join

        buttons_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'images', 'home_frame'
        )
        lines_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'images', 'home_frame', 'lines'
        )
        start_button_dark_relpath = join(buttons_dir, 'start_button_dark.png')
        self.start_button_dark = \
            Image.open(resource_path(start_button_dark_relpath))
        
        start_button_light_relpath = join(buttons_dir, 'start_button_light.png')
        self.start_button_light = \
            Image.open(resource_path(start_button_light_relpath))
        
        line_color = self.settings.get('color_theme')
        line_light_relpath = join(lines_dir, f'line_light_{line_color}.png')
        self.line_light = \
            Image.open(resource_path(line_light_relpath))
        
        line_dark_relpath = join(lines_dir, f'line_dark_{line_color}.png')
        self.line_dark = \
            Image.open(resource_path(line_dark_relpath))


class _LineFrame(CTkMovingFrame):
    def __init__(self, master: HomeFrame, fg_color='transparent',
                 img_width=480, img_height=31.57, **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._load_lines()

        self.line = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=self.line_dark,
                dark_image=self.line_light,
                size=(img_width, img_height),
            ),
        )
        self.line.grid()

    def _load_lines(self):
        dirname = os.path.dirname
        join = os.path.join
        lines_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'images', 'home_frame', 'lines'
        )
        
        line_color = Settings.create_settings().get('color_theme')
        
        line_light_relpath = join(lines_dir, f'line_light_{line_color}.png')
        self.line_light = \
            Image.open(resource_path(line_light_relpath))
        
        line_dark_relpath = join(lines_dir, f'line_dark_{line_color}.png')
        self.line_dark = \
            Image.open(resource_path(line_dark_relpath))
