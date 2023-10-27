import os
import customtkinter as ctk

from toplevel import Drill
from toplevel import Results
from toplevel import FontRequirement

from frontend.frames import \
    HomeFrame, LeftPanel, ReferenceFrame, SettingsFrame

from backend.handlers import \
    Settings, _load_theme_or_theme_path, font_requires_installing


class App(ctk.CTk):

    _instance = None

    def __new__(cls, *args, **kwargs):
        cls.settings = Settings.create_settings()
        ctk.set_default_color_theme(
            _load_theme_or_theme_path(cls.settings.get('color_theme'))
        )
        
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        super().__init__()

        self.geometry(f"{700}x{430}")
        self.iconbitmap(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'toplevel', 'images', 'icon.ico'
            )
        )
        self.resizable(False, False)
        self.title('Quadratic equation trainer')

        self.home_button_toggled = False
        self.reference_button_toggled = False
        self.settings_button_toggled = False
        
        common_for_starting_ui = {
            'corner_radius': 0,
            'smooth_slowdown': True,
            'frequency': .002,
            'until': .25,
        }

        self.left_panel = LeftPanel(
            self,
            **common_for_starting_ui,
            direction='right',
        )

        self.home_frame = HomeFrame(
            self,
            **common_for_starting_ui,
            direction='left',
        )
        self.home_frame.start_button.configure(
            command=self.drill_button_callback
        )
        self.bind('<Control-Return>', self.drill_button_callback)
        
        self.reference_frame = ReferenceFrame(self, corner_radius=0)
        self.settings_frame = SettingsFrame(self, corner_radius=0)

        self.last_open_frame = self.__class__.settings.get('last_open_frame')

        self._configure_starting_ui()

        for button, command in [
            [self.left_panel.home_button, self.home_button_callback],
            [self.left_panel.reference_button, self.reference_button_callback],
            [self.left_panel.settings_button, self.settings_button_callback],
        ]:
            button.configure(command=command)

    def _place_left_panel(self):
        self.left_panel.place(
            relx=0,
            rely=.5,
            relwidth=.25,
            relheight=1,
            anchor='e',
        )

    def _configure_starting_ui(self):
        if self.last_open_frame == 'settings':
            self.left_panel.no_movement_place(
                relx=.25,
                rely=.5,
                relwidth=.25,
                relheight=1,
                anchor='e',
            )
            self.settings_button_callback()
        else:
            self.home_button_callback()
            self.after(250, self._place_left_panel)

    def home_button_callback(self):
        self._select_frame_by_name('home')
        if not self.home_button_toggled:
            self.home_frame.place(
                relx=.5,
                rely=.5,
                relwidth=.75,
                relheight=1,
                anchor='w',
            )
            self.home_frame._configure_starting_ui()
            self.home_button_toggled = True

    def reference_button_callback(self):
        self._select_frame_by_name('reference')
        if not self.reference_button_toggled:
            self.reference_frame._configure_starting_ui()
            self.reference_button_toggled = True

    def settings_button_callback(self):
        self._select_frame_by_name('settings')
        if not self.settings_button_toggled:
            self.settings_frame._configure_starting_ui()
            self.settings_button_toggled = True
        Settings.update_settings('last_open_frame', 'home')

    def _select_frame_by_name(self, chosen_name: str):
        for button, frame, name in [
            [
                self.left_panel.home_button,
                self.home_frame,
                'home',
            ], [
                self.left_panel.reference_button,
                self.reference_frame,
                'reference',
            ], [
                self.left_panel.settings_button,
                self.settings_frame,
                'settings',
            ],
        ]:
            if name == chosen_name:
                button.configure(fg_color=('gray75', 'gray25'))
                if not frame.winfo_ismapped():
                    frame.no_movement_place(
                        relx=.25,
                        rely=.5,
                        relwidth=.75,
                        relheight=1,
                        anchor='w',
                    )
            else:
                button.configure(fg_color='transparent')
                frame.place_forget()

    def drill_button_callback(self, event=None):
        self.drill = Drill(self)
        self.withdraw()

        self.wait_window(self.drill)

        if self.drill.counter_frame.counter_label.cget('text') != '0/0':
            self.results = Results(
                self.drill.counter_frame.correct_user_answers,
                self.drill.counter_frame.all_answers,
                self.drill.difficulty,
                master=self,
            )
            self.wait_window(self.results)
        
        self.deiconify()


def main():
    ctk.set_appearance_mode(Settings.create_settings().get('appearance_mode'))
    for font_name in ['book_antiqua', 'cambria', 'white_rabbit']:
        if font_requires_installing(font_name):
            font_requirement = FontRequirement()
            font_requirement.mainloop()
            break
    else:  # no break
        while True:
            try:
                app = App()
                app.mainloop()
                # user himself closes the window; no exceptions caught
                break
            except SystemExit:
                app.destroy()


if __name__ == '__main__':
    main()
