import os
import customtkinter as ctk

from frontend.assets import CTkDelayedLabel, CTkMovingFrame


class FontRequirement(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{600}x{330}")

        icon_abspath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'images', 'icon.ico'
        )
        self.after(201, lambda: self.iconbitmap(icon_abspath))
        
        self.resizable(False, False)
        self.title('Requirement')

        self.mgs_frame = MgsFrame(
            self,
            direction='down',
            until=.85,
            frequency=.002,
            smooth_slowdown=True,
            fg_color='transparent'
        )
        self.mgs_frame.place(
            relx=.5,
            rely=0,
            relwidth=.8,
            relheight=.7,
            anchor='s',
        )


class MgsFrame(CTkMovingFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        _MsgFrame(
            self,
            border_width=1,
            border_color=('gray20', 'gray90'),
        ).grid(row=0, column=0, pady=10, sticky='nsew')


class _MsgFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        common = {
            'ms': 40,
            'font': ctk.CTkFont(size=16)
        }

        self.label_1 = CTkDelayedLabel(
            self,
            text='Пожалуйста, для правильного отображения установите',
            **common,
        )
        self.label_2 = CTkDelayedLabel(
            self,
            text='все шрифты, лежащие в папке с приложением',
            **common,
        )

        self.place_labels()

    def place_labels(self):
        self.after(
            200,
            lambda: self.label_1.place(relx=.055, rely=.42, anchor='w')
        )
        self.after(
            60 * 40 + 200,
            lambda: self.label_2.place(relx=.13, rely=.62, anchor='w')
        )
