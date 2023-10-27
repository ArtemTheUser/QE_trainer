from typing import Literal
import customtkinter as ctk


class CTkMovingFrame(ctk.CTkFrame):
    '''CTk Frame with movement possibility.
    It is not recommended to use the `ms` parameter, because it
    doesn't work the way it is supposed to in tkinter.
    Use `frequency` parameter instead - a "tick"
    that happens every `ms` time.
    '''
    def __init__(
            self,
            master,
            *,
            direction: Literal['left', 'right', 'up', 'down'],
            until: int | float,
            ms: int = 1,
            frequency: int | float = .001,
            smooth_slowdown: bool = False,
            **kwargs):
        super().__init__(master, **kwargs)

        self.direction = direction
        self.end = until
        self.ms = ms
        self.frequency = frequency
        self.smooth_slowdown = smooth_slowdown

        self._animate_called_counter = 0
        self._reset_frequency = frequency
        self.almost_done = False

        # either relx or rely, depending on direction
        self.relx_rely: str = \
            'relx' if self.direction in ['left', 'right'] else 'rely'

    def no_movement_place(self, **kwargs):
        return super().place(**kwargs)
    
    @property
    def pls_mns(self) -> Literal[-1, 1]:
        return -1 if self.direction in ['left', 'up'] else 1
    
    @property
    def _place_condition(self):
        'True when a widget is about to be placed (and not UNplaced).'
        return (
            self.pls_mns == 1 and self.start < self.end
            or self.pls_mns == -1 and self.start > self.end
        )
    
    def place(self, **kwargs):
        self.kwargs = kwargs

        self.start = self.distance_travelled = kwargs.get(self.relx_rely)
        self.distance = abs(self.end - self.start)

        self._reset_vars_for_smooth_slowdown()

        self.distance_parts = self._calcualate_distance_parts(self.distance)
        self._animate(**self.kwargs)

    def unplace(self):
        self._change_direction()
        self._reset_vars_for_smooth_slowdown()

        self.distance_parts = self._calcualate_distance_parts(self.distance)
        self._animate(**self.kwargs)

    def _animate(self, **kwargs):
        if self.smooth_slowdown:
            try:
                part_num, part = self.distance_parts[0]
            except IndexError:
                pass

            if self.pls_mns * (self.distance_travelled - part) >= 0:
                self.distance_parts.pop(0)

            if self.almost_done:
                part_num -= 2

            if self._animate_called_counter % 2 ** part_num == 0:
                super().place(**kwargs)
                self.distance_travelled += (self.pls_mns * self.frequency)
                kwargs.update({self.relx_rely: self.distance_travelled})
        else:
            super().place(**kwargs)
            self.distance_travelled += (self.pls_mns * self.frequency)
            kwargs.update({self.relx_rely: self.distance_travelled})

        if self._place_condition:
            while abs(self.end - self.distance_travelled) < 3 * self.frequency:
                if self.frequency * 4 == self._reset_frequency:
                    kwargs.update({self.relx_rely: self.end})
                    super().place(**kwargs)
                    return
                self.frequency /= 2
                self.almost_done = True
        else:  # unplace
            while abs(self.start - self.distance_travelled) < 3 * self.frequency:
                if self.frequency * 4 == self._reset_frequency:
                    kwargs.update({self.relx_rely: self.start})
                    super().place(**kwargs)
                    self._change_direction()
                    return
                self.frequency /= 2
                self.almost_done = True

        self._animate_called_counter += 1
        self.after(self.ms, lambda: self._animate(**kwargs))

    def _calcualate_distance_parts(self, part):
        distance_parts = [0]  # 0 so to avoid IndexError on the first run
        start_or_end = self.start if self._place_condition else self.end

        while True:
            part /= 2
            if part > self.frequency:
                distance_parts.append(distance_parts[-1] + part)
            else:
                distance_parts.append(self.distance)
                break

        distance_parts.remove(0)
        distance_parts = [
            start_or_end + (i if self.pls_mns == 1 else -i)
            for i in distance_parts
        ]

        return list(enumerate(distance_parts))
    
    def _change_direction(self) -> str:
        match self.direction:
            case 'right':
                self.direction = 'left'
            case 'left':
                self.direction = 'right'
            case 'up':
                self.direction = 'down'
            case 'down':
                self.direction = 'up'

    def _reset_vars_for_smooth_slowdown(self):
        self._animate_called_counter = 0
        self.frequency = self._reset_frequency
        self.almost_done = False


# testing frames
class _LeftFrame(CTkMovingFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.button = ctk.CTkButton(
            self,
            text="I'm a button!",
        )
        self.button.place(relx=.5, rely=.3, anchor='center')

        self.label = ctk.CTkLabel(
            self,
            text="I'm a label!",
        )
        self.label.place(relx=.5, rely=.7, anchor='center')


class _RightFrame(CTkMovingFrame): ...


class _UpperFrame(CTkMovingFrame): ...


class _DownFrame(CTkMovingFrame): ...


class _App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry(f"{430}x{200}")

        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.grid_columnconfigure(0, weight=1)

        test_frame_1 = ctk.CTkFrame(
            self,
            fg_color='red',
            corner_radius=0
        )
        test_frame_1.place(relx=.35, rely=.5, relwidth=.25, relheight=1,
                         anchor='e')

        test_frame_2 = ctk.CTkFrame(
            self,
            fg_color='red',
            corner_radius=0
        )
        test_frame_2.place(relx=.65, rely=.5, relwidth=.25, relheight=1,
                         anchor='w')
        
        self.left_panel = _LeftFrame(
            self,
            until=.35,
            direction='right',
            ms=1,
            smooth_slowdown=True,
            frequency=.001,
        )
        self.right_panel = _RightFrame(
            self,
            until=.65,
            direction='left',
            ms=1,
            smooth_slowdown=True,
            frequency=.001,
        )
        self.upper_panel = _UpperFrame(
            self,
            until=.25,
            direction='down',
            ms=1,
            smooth_slowdown=True,
            frequency=.001,
        )
        self.down_panel = _DownFrame(
            self,
            until=.75,
            direction='up',
            ms=1,
            smooth_slowdown=True,
            frequency=.001
        )

        self.left_panel_button = ctk.CTkButton(
            self,
            text='Left Panel',
            command=self.left_panel_button_callback,
        )
        self.left_panel_button.grid(column=0, row=1)

        self.right_panel_button = ctk.CTkButton(
            self,
            text='Right Panel',
            command=self.right_panel_button_callback,
        )
        self.right_panel_button.grid(column=0, row=2)

        self.upper_panel_button = ctk.CTkButton(
            self,
            text='Upper button',
            command=self.upper_panel_button_callback,
        )
        self.upper_panel_button.grid(column=0, row=3)

        self.down_panel_button = ctk.CTkButton(
            self,
            text='Down button',
            command=self.down_panel_button_callback,
        )
        self.down_panel_button.grid(column=0, row=4)

    def left_panel_button_callback(self):
        self.left_panel.place(relx=.1, rely=.5, relwidth=.25, relheight=.8, anchor='e')
        # self.right_panel.unplace()

    def right_panel_button_callback(self):
        self.right_panel.place(relx=.9, rely=.5, relwidth=.2, relheight=.8, anchor='w')
        # self.left_panel.unplace()

    def upper_panel_button_callback(self):
        self.upper_panel.place(relx=.75, rely=0, relwidth=.2, relheight=.33, anchor='s')
        # self.down_panel.unplace()

    def down_panel_button_callback(self):
        self.down_panel.place(relx=.75, rely=1, relwidth=.2, relheight=.33, anchor='n')
        # self.upper_panel.unplace()


def main():
    app = _App()
    app.mainloop()


if __name__ == '__main__':
    main()
