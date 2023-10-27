from typing import Literal

# import tkinter as tk
# import _tkinter
import customtkinter as ctk

        
# def _deletecommand(self, name):
#     self.tk.deletecommand(name)
#     try:
#         self._tclCommands.remove(name)
#     except (ValueError, AttributeError):
#         pass

# def _destroy(self):
#     if self._tclCommands is not None:
#         for name in self._tclCommands:
#             try:
#                 self.tk.deletecommand(name)
#             except _tkinter.TclError:
#                 pass
#         self._tclCommands = None
    

class CTkDelayedLabel:
    '''CTk label that makes given text show up letter-by-letter.
    ms parameter stays for miliseconds - delay between each letter showing up.
    '''
    # tk.Misc.deletecommand = _deletecommand
    # tk.Misc.destroy = _destroy

    def __init__(self, master, *, ms=100, text='CTkDelayedLabel',
                 spaces_included=True, **kwargs):

        self.master_ = master

        self.ms = ms
        self.text = text
        self.text_len = len(self.text)
        self.counter = 1
        self.spaces_included = spaces_included
        self.placing_method: Literal['place', 'grid', 'pack'] = 'place'

        self.kwargs = kwargs
        self.conf_kwargs = None

    # calling __getattr__ bcs self.label raises an AttributeError
    def __getattr__(self, attr):
        return getattr(self.label, attr)
    
    def configure(self, **conf_kwargs):
        self.conf_kwargs = conf_kwargs

        if 'ms' in conf_kwargs:
            self.ms = conf_kwargs.pop('ms')
        if 'spaces_included' in conf_kwargs:
            self.spaces_included = conf_kwargs.pop('spaces_included')

    def grid(self, **kwds):
        self.placing_method = 'grid'
        self._create_delayed_label(**kwds)
    
    def place(self, **kwds):
        self._create_delayed_label(**kwds)
    
    def pack(self, **kwds):
        self.placing_method = 'pack'
        self._create_delayed_label(**kwds)

    def _create_delayed_label(self, **kwds):
        self.kwds = kwds
        
        if self.kwds:
            self.non_empty_kwds = kwds
        else:
            try:
                self.kwds = self.non_empty_kwds
            except AttributeError:  # user didn't pass any kwds
                if self.placing_method == 'grid':
                    raise ValueError('no arguments were given')

        if self.counter != 1:
            # delay with 1 ms is required to avoid the situation
            # where we try to destroy a label that doesn't exist
            self.label.after(1, self.label.destroy)

        if self.ms == 0:
            self.counter += self.text_len - 1
        
        truncated_text = self.text[:self.counter]
        if self.conf_kwargs is None:
            self.label = ctk.CTkLabel(
                self.master_,
                text=truncated_text,
                **self.kwargs,
            )
        else:
            text = {'text': truncated_text}
            kwargs =  self.kwargs | text | self.conf_kwargs
            self.label = ctk.CTkLabel(
                self.master_,
                **kwargs,
            )
        match self.placing_method:
            case 'grid':
                self.label.grid(**self.kwds)
            case 'place':
                self.label.place(**self.kwds)
            case 'pack':
                self.label.pack(**self.kwds)

        self.counter += 1

        if self.counter != self.text_len + 1:
            if self.spaces_included:
                self.after(self.ms, self._create_delayed_label)
            else:
                self.after(
                    0 if truncated_text.endswith(' ') else self.ms,
                    self._create_delayed_label
                )


class _App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry(f"{700}x{430}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(self, command=self.callback, text='destroy').place(relx=.3, rely=.4)
        ctk.CTkButton(self, command=self.another_callback, text='place').place(relx=.3, rely=.6)

        self.label = CTkDelayedLabel(self, ms=10, text='a' * 100)
        # self.label = ctk.CTkLabel(self, text='a' * 10)
        self.label.place(relx=.5, rely=.5, anchor='w')
        # self.label.grid(row=0, column=0)

        # self.frame = ctk.CTkFrame(
        #     self,
        #     corner_radius=0,
        # )
        # self.frame.place(relx=.3, rely=.5, relwidth=.3, relheight=1, anchor='e')

    def callback(self):
        self.label.destroy()

    def another_callback(self):
        self.label.place(relx=.5, rely=.5, anchor='nw')


def main():
    app = _App()
    app.mainloop()


if __name__ == '__main__':
    main()
