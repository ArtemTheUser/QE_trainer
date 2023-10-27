import customtkinter as ctk


class ScrollableTabview(ctk.CTkTabview):
    def _create_tab(self) -> ctk.CTkScrollableFrame:
        return ctk.CTkScrollableFrame(
            self,
            height=0,
            width=0,
            fg_color=self._fg_color,
            border_width=0,
            corner_radius=self._corner_radius,
        )
    

class _Test(ScrollableTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.tab_1 = self.add('tab_1')
        self.tab_2 = self.add('tab_2')
        self.tab_3 = self.add('tab_3')

        self.label_tab_1 = ctk.CTkLabel(
            self.tab_1,
            text='label on tab_1\n' * 79,
        )
        self.label_tab_1.pack()


class _App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry(f"{700}x{430}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollable_tabview = _Test(
            self,
        )
        self.scrollable_tabview.grid()


def main():
    app = _App()
    app.mainloop()


if __name__ == '__main__':
    main()
