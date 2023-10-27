import os

import customtkinter as ctk
from PIL import Image

from ..assets import CTkMovingFrame

from backend.handlers import Settings, resource_path


class LeftPanel(CTkMovingFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((0,1,2), weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.line_color = Settings.create_settings().get('color_theme')

        self.common_parameters = {
            'corner_radius': 0,
            'font': ctk.CTkFont(family='Book Antiqua', weight='bold'),
            'border_spacing': 10,
            'fg_color': 'transparent',
            'hover_color': ('gray70', 'gray30'),
            'text_color': ('gray20', 'gray90'),
            'anchor': 'w',
        }
        
        self._load_images()

        self._create_home_button()
        self.home_button.grid(row=0, column=0, sticky='nsew')

        self._create_reference_button()
        self.reference_button.grid(row=1, column=0, sticky='nsew')

        self._create_settings_button()
        self.settings_button.grid(row=2, column=0, sticky='nsew')

        self._create_logo()
        self.logo.grid(row=4, column=0, pady=(0, 4))

        self._create_logo_text()
        self.logo_text.grid(row=5, column=0, pady=(0, 4))

    def _create_home_button(self):
        self.home_button = ctk.CTkButton(
            self,
            **self.common_parameters,
            text='Главная',
            image=ctk.CTkImage(
                light_image=self.home_dark_img,
                dark_image=self.home_light_img,
                size=(20, 20),
            ),
        )

    def _create_reference_button(self):
        self.reference_button = ctk.CTkButton(
            self,
            **self.common_parameters,
            text='Справка',
            image=ctk.CTkImage(
                light_image=self.question_dark_img,
                dark_image=self.question_light_img,
                size=(20, 20),
            ),
        )

    def _create_settings_button(self):
        self.settings_button = ctk.CTkButton(
            self,
            **self.common_parameters,
            text='Настройки',
            image=ctk.CTkImage(
                light_image=self.settings_dark_img,
                dark_image=self.settings_light_img,
                size=(20, 20),
            ),
        )

    def _create_logo(self):
        self.logo = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=self.logo_dark,
                dark_image=self.logo_light,
                size=(160, 160)
            )
        )

    def _create_logo_text(self):
        self.logo_text = ctk.CTkLabel(
            self,
            text='Quadratic equation trainer',
            font=ctk.CTkFont(family='White Rabbit', size=10),
            text_color=('gray20', 'gray90'),
        )

    def _load_images(self):
        dirname = os.path.dirname
        join = os.path.join

        img_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'images', 'left_panel'
        )
        logos_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'images', 'left_panel', 'logos'
        )
        self.question_dark_img = Image.open(
            resource_path(join(img_dir, 'question_dark.png'))
        )
        self.question_light_img = Image.open(
            resource_path(join(img_dir, 'question_light.png'))
        )

        self.home_light_img = Image.open(
            resource_path(join(img_dir, 'home_light.png'))
        )
        self.home_dark_img = Image.open(
            resource_path(join(img_dir, 'home_dark.png'))
        )

        self.settings_dark_img = Image.open(
            resource_path(join(img_dir, 'settings_dark.png'))
        )
        self.settings_light_img = Image.open(
            resource_path(join(img_dir, 'settings_light.png'))
        )

        logo_light_relpath = join(logos_dir, f'logo_light_{self.line_color}.png')
        self.logo_light = \
            Image.open(resource_path(logo_light_relpath))
        
        logo_dark_relpath = join(logos_dir, f'logo_dark_{self.line_color}.png')
        self.logo_dark = \
            Image.open(resource_path(logo_dark_relpath))
