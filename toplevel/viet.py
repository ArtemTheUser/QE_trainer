import os

import customtkinter as ctk
from PIL import Image

from frontend.assets import CTkMovingFrame

from backend.handlers import Settings, resource_path


class Hint(CTkMovingFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._load_images()

        self.default_width = 33.87
        self.default_height = 17.93

        self.hint_label = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=self.viet_dark,
                dark_image=self.viet_light,
                size=(self.default_width * 5.5, self.default_height * 5.5)
            ),
        )
        self.hint_label.grid(row=0, column=0, padx=(7,0), pady=15)

    def _load_images(self):
        dirname = os.path.dirname
        join = os.path.join

        img_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'frontend', 'images', 'toplevel'
        )
        # 32.57 x 18.53
        self.viet_light = Image.open(
            resource_path(join(img_dir, 'viet_light.png'))
        )
        self.viet_dark = Image.open(
            resource_path(join(img_dir, 'viet_dark.png'))
        )


class SwitchFrame(CTkMovingFrame):
    def __init__(self, master, frame_to_place: Hint, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_to_place = frame_to_place
        self.difficulty = Settings.create_settings().get('difficulty')
        self.switch_var = ctk.IntVar(value=0)

        self.switch = ctk.CTkSwitch(
            self,
            text='Подсказка',
            width=36,
            height=18,
            command=self.switch_callback,
            onvalue=1,
            offvalue=0,
            variable=self.switch_var,
            font=ctk.CTkFont(family='Book Antiqua', size=14),
            text_color=('gray20', 'gray90'),
        )
        self.switch.grid(row=0, column=0, padx=10, pady=10)

        if self.difficulty in [2, 3]:
            self.switch.configure(state='disabled')

    def switch_callback(self):
        if self.switch.get():
            self.frame_to_place.place(relx=0, rely=.458, anchor='ne')
        else:
            self.frame_to_place.unplace()
