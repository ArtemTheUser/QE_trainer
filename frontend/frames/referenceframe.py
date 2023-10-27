import customtkinter as ctk

from backend.handlers import Settings, _create_text

from ..assets import CTkDelayedLabel, CTkMovingFrame, BrownPi


class ReferenceFrame(ctk.CTkFrame):
    def __init__(self, master, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.settings = Settings.create_settings()

        self._create_pies()

        common_for_references = {
            'fg_color': 'transparent',
            'smooth_slowdown': True,
        }

        self.usage_reference_frame = UsageReference(
            self,
            **common_for_references,
            direction='right',
            until=.75,
            frequency=.005,
        )
        self.usage_reference_label = CTkDelayedLabel(
            self,
            ms=50,
            text='Справка по использованию',
            font=ctk.CTkFont(family='Book Antiqua', size=18)
        )

        self.viet_reference_frame = VietReference(
            self,
            **common_for_references,
            direction='up',
            until=.54,
            frequency=.003
        )
        self.viet_reference_label = CTkDelayedLabel(
            self,
            ms=50,
            text='О решении через теорему Виета',
            font=ctk.CTkFont(family='Book Antiqua', size=18)
        )

    def no_movement_place(self, **kwargs):
        return super().place(**kwargs)
    
    def _configure_starting_ui(self):
        if self.settings.get('last_open_frame') == 'settings':
            self.usage_reference_frame.no_movement_place(
                relx=.75,
                rely=.25,
                relwidth=.7,
                relheight=.3,
                anchor='e',
            )
            self.usage_reference_label.configure(ms=0)
            self.usage_reference_label.place(
                relx=.17,
                rely=.05,
                anchor='w',
            )
            self.brown_pi_speaking.no_movement_place(
                relx=.77,
                rely=.25,
                anchor='w',
            )

            self.viet_reference_frame.no_movement_place(
                relx=.59,
                rely=.55,
                relwidth=.765,
                relheight=.44,
                anchor='n',
            )
            self.viet_reference_label.configure(ms=0)
            self.viet_reference_label.place(
                relx=.32,
                rely=.52,
                anchor='w',
            )
            self.brown_pi_showing_reversed.no_movement_place(
                relx=.18,
                rely=.88,
                anchor='e',
            )
        else:
            self.usage_reference_frame.place(
                relx=0,
                rely=.25,
                relwidth=.7,
                relheight=.3,
                anchor='e',
            )
            self.after(630, lambda: self.usage_reference_label.place(
                relx=.17,
                rely=.05,
                anchor='w',
            ))
            self.after(730, lambda: self.brown_pi_speaking.place(
                relx=1,
                rely=.25,
                anchor='w',
            ))

            self.after(1230, lambda: self.viet_reference_frame.place(
                relx=.59,
                rely=1,
                relwidth=.765,
                relheight=.44,
                anchor='n',
            ))
            self.after(2000, lambda: self.viet_reference_label.place(
                relx=.32,
                rely=.52,
                anchor='w',
            ))
            self.after(2300, lambda: self.brown_pi_showing_reversed.place(
                relx=0,
                rely=.88,
                anchor='e',
            ))

    def _create_pies(self):
        self.brown_pi_speaking = BrownPi(
            self,
            mood='speaking',
            width=100,
            height=100,
            direction='left',
            until=.77,
            smooth_slowdown=True,
        )
        self.brown_pi_showing_reversed = BrownPi(
            self,
            mood='showing_reversed',
            width=80,
            height=80,
            direction='right',
            until=.18,
            smooth_slowdown=True,
        )


class UsageReference(CTkMovingFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.usage_reference_texbox = ctk.CTkTextbox(
            self,
            border_width=.5,
            border_spacing=8,
            border_color=('gray20', 'gray90'),
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua', size=16),
            wrap='word',
        )
        self.usage_reference_texbox.insert('0.0', text=_create_text(
            'usage_reference.txt'
        ))
        self.usage_reference_texbox.tag_add('justify_center_1', 1.0, '1.end')
        self.usage_reference_texbox.tag_config('justify_center_1', justify='center')

        self.usage_reference_texbox.tag_add('justify_center_2', 6.0, '6.end')
        self.usage_reference_texbox.tag_config('justify_center_2', justify='center')

        self.usage_reference_texbox.configure(state='disabled')
        self.usage_reference_texbox.grid(row=0, column=0, padx=10, sticky='nsew')


class VietReference(CTkMovingFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.viet_reference_texbox = ctk.CTkTextbox(
            self,
            border_width=.5,
            border_spacing=8,
            border_color=('gray20', 'gray90'),
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua', size=16),
            wrap='word',
        )
        self.viet_reference_texbox.insert('0.0', text=_create_text(
            'viet_reference.txt'
        ))

        self.viet_reference_texbox.configure(state='disabled')
        self.viet_reference_texbox.grid(row=0, column=0, pady=10, sticky='nsew')
