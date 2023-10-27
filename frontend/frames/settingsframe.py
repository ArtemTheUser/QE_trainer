import os
import random

import customtkinter as ctk
import darkdetect
from PIL import Image

from ..assets import CTkDelayedLabel, CTkMovingFrame

from backend.handlers import (
    Settings,
    _make_ru_en_dict, _load_theme_or_theme_path, resource_path,
    _create_buttons_from_values_with_condition
)


ctk.CTkSegmentedButton._create_buttons_from_values = \
    _create_buttons_from_values_with_condition


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure((0,1,2), weight=1, uniform='fred')
        self.grid_rowconfigure((0,1,2), weight=1, uniform='fred')

        common_for_frames = {
            'border_width': 1,
            'border_color': ('gray20', 'gray90'),
            'smooth_slowdown': True,
        }

        self.color_theme_frame = ColorThemesFrame(
            self,
            **common_for_frames,
            until=.583,
            direction='left',
            frequency=.005
        )

        self.appearance_mode_frame = AppearanceModeFrame(
            self,
            **common_for_frames,
            until=.558,  # the middle of difficulty frame
            direction='right',
            frequency=.005,
        )
        
        self.difficulty_frame = DifficultyFrame(
            self,
            **common_for_frames,
            until=.4145,
            direction='up',
            frequency=.003,
        )
    
    def no_movement_place(self, **kwargs):
        return super().place(**kwargs)
    
    def _place_color_theme_frame(self):
        self.color_theme_frame.place(
            relx=1,
            rely=.25,
            relwidth=.358,
            relheight=.2,
            anchor='w',
        )

    def _place_appearance_mode_frame(self):
        self.appearance_mode_frame.place(
            relx=0,
            rely=.25,
            relwidth=.478,
            relheight=.2,
            anchor='e',
        )

    def _place_difficulty_frame(self):
        self.difficulty_frame.place(
            relx=.5,
            rely=1,
            relwidth=.88,
            relheight=.4145,
            anchor='n',
        )
    
    def _configure_starting_ui(self):
        if ColorThemesFrame.settings_frame_last_opened:
            self.color_theme_frame.no_movement_place(
                relx=.583,
                rely=.25,
                relwidth=.358,
                relheight=.2,
                anchor='w',
            )
            self.appearance_mode_frame.no_movement_place(
                relx=.558,
                rely=.25,
                relwidth=.478,
                relheight=.2,
                anchor='e',
            )
            self.difficulty_frame.no_movement_place(
                relx=.5,
                rely=.436,
                relwidth=.88,
                relheight=.4145,
                anchor='n',
            )
        else:
            DifficultyFrame.first_starting_ui_configure = True
            delays = [0, 300, 600]
            random.shuffle(delays)
            self.after(delays[0], self._place_color_theme_frame)
            self.after(delays[1], self._place_appearance_mode_frame)
            self.after(delays[2], self._place_difficulty_frame)

        settings = Settings.create_settings()

        # color theme
        self.color_theme_frame.color_theme_option_menu.set(
            _make_ru_en_dict(
                settings.get('color_theme'), self.color_theme_frame.pairs
            ).get('ru')
        )

        # appearance mode
        cur_appearance_mode = settings.get('appearance_mode')
        self.appearance_mode_frame.appearance_mode_segmented_button.set(
            # call segmented_button_callback to return ru
            self.appearance_mode_frame.segmented_button_callback(
                cur_appearance_mode
            )
        )

        # difficulty
        value = settings.get('difficulty')
        self.difficulty_frame.difficulty_slider_callback(value=value)
        self.difficulty_frame.difficulty_slider.set(value)


class ColorThemesFrame(CTkMovingFrame):

    settings_frame_last_opened = False

    def __init__(self, master, fg_color='transparent', **kwargs):
        direction = kwargs.pop('direction')
        until = kwargs.pop('until')
        frequency = kwargs.pop('frequency')
        smooth_slowdown = kwargs.pop('smooth_slowdown')
        super().__init__(
            master,
            direction=direction,
            until=until,
            frequency=frequency,
            smooth_slowdown=smooth_slowdown,
            fg_color=fg_color,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.pairs = [
            ('Синее', 'blue'),
            ('Тёмно-синее', 'dark-blue'),
            ('Зелёное', 'green'),
            ('Тёмно-зелёное', 'dark-green'),
            ('Горчичное', 'mustard'),
            ('Фиолетовое', 'violet'),
            ('Оранжевое', 'orange'),
            ('Аквамариновое', 'aquamarine'),
            ('Чёрно-белое', 'blackwhite'),
        ]
        
        # the actual frame on which everything is placed
        self.parent_frame = ctk.CTkFrame(
            self,
            **kwargs,
        )
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)
        self.parent_frame.grid(row=0, column=0, sticky='nsew', padx=10)

        self.color_theme_label = ctk.CTkLabel(
            self.parent_frame,
            text='Цветовое оформление',
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua'),
        )
        self.color_theme_label.place(relx=.5, rely=.26, anchor='center')

        self.color_theme_option_menu = ctk.CTkOptionMenu(
            self.parent_frame,
            values=[
                'Синее', 'Тёмно-синее',
                'Зелёное', 'Тёмно-зелёное',
                'Горчичное',
                'Фиолетовое',
                'Оранжевое',
                'Аквамариновое',
                'Чёрно-белое',
            ],
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua', size=15),
            command=self.option_menu_callback,
        )
        self.color_theme_option_menu.place(relx=.5, rely=.65, anchor='center')

    def option_menu_callback(self, value):
        self.__class__.settings_frame_last_opened = True

        ru_en_dict: dict[str, str] =  _make_ru_en_dict(value, self.pairs)
        en_theme = ru_en_dict.get('en')

        ctk.set_default_color_theme(_load_theme_or_theme_path(en_theme))
        Settings.update_settings('color_theme', en_theme)
        Settings.update_settings('last_open_frame', 'settings')

        raise SystemExit


class AppearanceModeFrame(CTkMovingFrame):
    def __init__(self, master, fg_color='transparent', **kwargs):
        direction = kwargs.pop('direction')
        until = kwargs.pop('until')
        frequency = kwargs.pop('frequency')
        smooth_slowdown = kwargs.pop('smooth_slowdown')
        super().__init__(
            master,
            direction=direction,
            until=until,
            frequency=frequency,
            smooth_slowdown=smooth_slowdown,
            fg_color=fg_color,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.parent_frame = ctk.CTkFrame(
            self,
            **kwargs,
        )
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)
        self.parent_frame.grid(row=0, column=0, sticky='nsew', padx=10)

        self.appearance_mode_label = ctk.CTkLabel(
            self.parent_frame,
            text='Выберите тему',
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua'),
        )
        self.appearance_mode_label.place(relx=.5, rely=.3, anchor='center')

        self.appearance_mode_segmented_button = ctk.CTkSegmentedButton(
            self.parent_frame,
            values=['Светлая', 'Тёмная', 'Системная'],
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua', size=13),
            command=self.segmented_button_callback,
        )
        self.appearance_mode_segmented_button.place(
            relx=.5, rely=.7, anchor='center'
        )

    def segmented_button_callback(self, value: str) -> str:
        pairs = [
            ('Светлая', 'light'),
            ('Тёмная', 'dark'),
            ('Системная', 'system'),
        ]
        ru_en_dict: dict[str, str] = _make_ru_en_dict(value, pairs)

        appearance_mode = ru_en_dict.get('en')

        if appearance_mode == 'system':
            avoid_system_var = darkdetect.theme().lower()
        else:
            avoid_system_var = appearance_mode
        
        ctk.set_appearance_mode(avoid_system_var)
        Settings.update_settings('appearance_mode', appearance_mode)

        return ru_en_dict.get('ru')


class DifficultyFrame(CTkMovingFrame):

    first_starting_ui_configure = False

    def __init__(self, master: SettingsFrame, fg_color='transparent', **kwargs):
        direction = kwargs.pop('direction')
        until = kwargs.pop('until')
        frequency = kwargs.pop('frequency')
        smooth_slowdown = kwargs.pop('smooth_slowdown')
        super().__init__(
            master,
            direction=direction,
            until=until,
            frequency=frequency,
            smooth_slowdown=smooth_slowdown,
            fg_color=fg_color,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # the actual frame on which everything is placed
        self.parent_frame = ctk.CTkFrame(
            self,
            **kwargs,
        )
        self.parent_frame.grid_columnconfigure((0,1,2), weight=2, uniform='fred')
        self.parent_frame.grid_columnconfigure(3, weight=4, uniform='fred')
        self.parent_frame.grid_rowconfigure(0, weight=1, uniform='fred')
        self.parent_frame.grid(row=0, column=0, sticky='nsew', pady=10)

        # required for difficulty_slider_callback
        self.passed_value = None
        self.common_for_text = {
            'font': ctk.CTkFont(family='Book Antiqua'),
            'text_color': ('gray20', 'gray90'),
        }

        self._load_images()
        self.create_gds()

        # just a line for separation
        self.separator = ctk.CTkFrame(
            self.parent_frame,
            width=1.4,
            corner_radius=1000,
            fg_color=('gray20', 'gray90'),
        )
        self.separator.place(relx=.6, rely=.5, anchor='center', relheight=.9)

        self.difficulty_label = ctk.CTkLabel(
            self.parent_frame,
            text='Сложность',
            **self.common_for_text,
        )
        self.difficulty_label.place(relx=.3, rely=.2, anchor='center')

        self.difficulty_slider = ctk.CTkSlider(
            self.parent_frame,
            from_=1,
            to=3,
            number_of_steps=2,
            command=self.difficulty_slider_callback,
        )
        self.difficulty_slider.place(relx=.1, rely=.5, anchor='w',
                                     relwidth=.4)
        
    def __getattribute__(self, attr):
        if attr == 'place':
            self.after(1400, self.create_no_overlay_frame)
            self.after(1400, self.place_no_overlay_frame)
        elif attr == 'no_movement_place':
            self.create_no_overlay_frame()
            self.place_no_overlay_frame()
        return object.__getattribute__(self, attr)
        
    def create_no_overlay_frame(self):
        # for GDs to appear/disappear without overlaying the border
        self.no_overlay_frame = ctk.CTkFrame(
            self.parent_frame,
            height=1,
            fg_color=('gray20', 'gray90'),  # must be the same as border_color
        )
        
    def place_no_overlay_frame(self):
        self.no_overlay_frame.place(relx=.01, rely=1, relwidth=.59,
                                    anchor='sw')

    def _load_images(self):
        dirname = os.path.dirname
        join = os.path.join

        img_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'images', 'settings_frame'
        )
        self.parent_frame.gd_easy_img = Image.open(
            resource_path(join(img_dir, 'gd_easy.png'))
        )
        self.parent_frame.gd_normal_img = Image.open(
            resource_path(join(img_dir, 'gd_normal.png'))
        )
        self.parent_frame.gd_harder_img = Image.open(
            resource_path(join(img_dir, 'gd_harder.png'))
        )

    def difficulty_slider_callback(self, value):
        '''dummy checkings are required due to slider callback mechanism'''

        if self.passed_value == value:
            return  # check the __doc__

        if value == 1:
            self.difficulty_level = 1

            self.difficulty_slider.configure(
                button_color='#2EADFF',
                button_hover_color='#0064A3',
                state='disabled',
            )
            self.after(1100, lambda: self.difficulty_slider.configure(
                state='normal',
            ))
            if self.passed_value is not None:
                if self.prev_passed_value == 2:
                    self.gd_normal.unplace()
                    self.normal_label.destroy()
                else:
                    self.gd_harder.unplace()
                    self.harder_label.destroy()
            
            self.gd_easy.place(relx=.117, rely=1, anchor='n')

            self._create_easy_label()
            self.easy_label.place(relx=.8, rely=.5, anchor='center')

            self.passed_value = self.prev_passed_value = value
        elif value == 2:
            self.difficulty_level = 2

            self.difficulty_slider.configure(
                button_color='#FFBA0A',
                button_hover_color='#B88200',
                state='disabled',
            )
            self.after(1100, lambda: self.difficulty_slider.configure(
                state='normal',
            ))
            if self.passed_value is not None:
                if self.prev_passed_value == 1:
                    self.gd_easy.unplace()
                    self.easy_label.destroy()
                else:
                    self.gd_harder.unplace()
                    self.harder_label.destroy()
                
            self.gd_normal.place(relx=.3, rely=1, anchor='n')

            self._create_normal_label()
            self.normal_label.place(relx=.8, rely=.5, anchor='center')

            self.passed_value = self.prev_passed_value = value
        elif value == 3:
            self.difficulty_level = 3

            self.difficulty_slider.configure(
                button_color='#FF1C0A',
                button_hover_color='#8F0B00',
                state='disabled',
            )
            self.after(1100, lambda: self.difficulty_slider.configure(
                state='normal',
            ))
            if self.passed_value is not None:
                if self.prev_passed_value == 1:
                    self.gd_easy.unplace()
                    self.easy_label.destroy()
                else:
                    self.gd_normal.unplace()
                    self.normal_label.destroy()
            
            self.gd_harder.place(relx=.483, rely=1, anchor='n')

            self._create_harder_label()
            self.harder_label.place(relx=.8, rely=.5, anchor='center')

            self.passed_value = self.prev_passed_value = value

        Settings.update_settings('difficulty', self.difficulty_level)

    def _create_easy_label(self):
        self.easy_label = CTkDelayedLabel(
            self.parent_frame,
            text=(
                'Только приведённые\n\n'
                'квадратные уравнения.\n\n'
                'Низкие коэффициенты.'
            ),
            **self.common_for_text,
            ms=(
                0 if ColorThemesFrame.settings_frame_last_opened or
                self.__class__.first_starting_ui_configure
                else 10
            ),
        )
        ColorThemesFrame.settings_frame_last_opened = False
        self.__class__.first_starting_ui_configure = False

    def _create_normal_label(self):
        self.normal_label = CTkDelayedLabel(
            self.parent_frame,
            text=(
                'В основном приведённые\n\n'
                'квадратные уравнения.\n\n'
                'Более высокие\n\n'
                'коэффициенты.'
            ),
            **self.common_for_text,
            ms=(
                0 if ColorThemesFrame.settings_frame_last_opened or
                self.__class__.first_starting_ui_configure
                else 10
            ),
        )
        ColorThemesFrame.settings_frame_last_opened = False
        self.__class__.first_starting_ui_configure = False

    def _create_harder_label(self):
        self.harder_label = CTkDelayedLabel(
            self.parent_frame,
            text=(
                'В основном\n\n'
                'неприведённые\n\n'
                'квадратные уравнения.\n\n'
                'Высокие коэффициенты.'
            ),
            **self.common_for_text,
            ms=(
                0 if ColorThemesFrame.settings_frame_last_opened or
                self.__class__.first_starting_ui_configure
                else 10
            ),
        )
        ColorThemesFrame.settings_frame_last_opened = False
        self.__class__.first_starting_ui_configure = False

    def create_gds(self):
        self.gd_easy = _GDEasy(
            self.parent_frame,
            direction='up',
            until=.665,
            smooth_slowdown=True,
            frequency=.003,
        )
        self.gd_normal = _GDNormal(
            self.parent_frame,
            direction='up',
            until=.665,
            smooth_slowdown=True,
            frequency=.003,
        )
        self.gd_harder = _GDHarder(
            self.parent_frame,
            direction='up',
            until=.665,
            smooth_slowdown=True,
            frequency=.003,
        )


# internal classes
class _GDEasy(CTkMovingFrame):
    def __init__(self, master, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._gd_easy_label = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=master.gd_easy_img,
                size=(30,30)
            ),
        )
        self._gd_easy_label.grid()


class _GDNormal(CTkMovingFrame):
    def __init__(self, master, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._gd_normal_label = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=master.gd_normal_img,
                size=(30,30)
            ),
        )
        self._gd_normal_label.grid()


class _GDHarder(CTkMovingFrame):
    def __init__(self, master, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._gd_harder_label = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=master.gd_harder_img,
                size=(30,30)
            ),
        )
        self._gd_harder_label.grid()
