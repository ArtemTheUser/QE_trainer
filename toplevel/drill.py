import math
import os
import random

import customtkinter as ctk
from PIL import Image

from frontend.frames.homeframe import _LineFrame
from frontend.assets import CTkDelayedLabel, CTkMovingFrame, BluePi, BrownPi

from backend.equation import QuadraticEquation
from backend.handlers import Settings, resource_path

from .viet import Hint, SwitchFrame


class Drill(ctk.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.geometry(f"{700}x{400}")
        self.after(201, lambda: self.iconbitmap(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'images', 'icon.ico'
            )
        ))
        self.resizable(False, False)
        self.title('Training')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_for_focus = ctk.CTkFrame(self, corner_radius=0,
                                            fg_color='transparent')
        self.frame_for_focus.grid(row=0, column=0, sticky='nsew')

        self.settings = Settings.create_settings()
        self.difficulty = self.settings.get('difficulty')
        self.line_color = self.settings.get('color_theme')

        self._load_images()

        self.counter_frame = CounterFrame(
            self,
            direction='left',
            until=.67,
            smooth_slowdown=True,
            frequency=.002
        )
        common_for_msgs = {
            'direction': 'down',
            'until': .27,
            'smooth_slowdown': True,
            'frequency': .002,
        }
        self.correct_msg_frame = CorrectMsgFrame(
            self,
            **common_for_msgs,
        )
        self.incorrect_msg_frame = IncorrectMsgFrame(
            self,
            **common_for_msgs,
        )

        self.line = _LineFrame(
            self,
            direction='down',
            until=.12,
            smooth_slowdown=True,
        )

        # for equation to disappear as nice as possible
        match self.difficulty:
            case 1:
                self.until = -.18
            case 2:
                self.until = -.215
            case 3:
                self.until = -.235

        self.create_equation_frame()
        self.no_movement_place_eq_frame()

        self.hint = Hint(
            self,
            direction='right',
            until=.327,
            frequency=.002,
            smooth_slowdown=True,
        )
        self.answers_frame = AnswersFrame(
            self,
            direction='up',
            until=.458,
            smooth_slowdown=True,
            frequency=.002,
        )
        self.hint_switch = SwitchFrame(
            self,
            frame_to_place=self.hint,
            direction='up',
            until=.872,
            smooth_slowdown=True,
        )

        self.ms_for_delay = (
            self.equation_frame.eq_label.ms
            * (self.equation_frame.eq_label.text_len + 5)
        )
        self.after(self.ms_for_delay, self._place_line_frame)
        self.after(self.ms_for_delay + 200, self._place_answers_frame)
        self.after(self.ms_for_delay + 500, self._place_hint_switch_frame)
        self.after(self.ms_for_delay + 1300, self._place_counter_frame)

        self._create_pies()
        self.place_pies()

    def _load_images(self):
        dirname = os.path.dirname
        join = os.path.join

        solutions_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'frontend', 'images', 'toplevel'
        )
        lines_dir = join(
            dirname(dirname(os.path.relpath(__file__))),
            'frontend', 'images', 'toplevel', 'lines'
        )

        solutions_light_relpath = join(solutions_dir, 'solutions_light.png')
        self.solutions_light = \
            Image.open(resource_path(solutions_light_relpath))
        
        solutions_dark_relpath = join(solutions_dir, 'solutions_dark.png')
        self.solutions_dark = \
            Image.open(resource_path(solutions_dark_relpath))

        line_light_relpath = join(lines_dir, f'line_light_{self.line_color}.png')
        self.line_light = \
            Image.open(resource_path(line_light_relpath))
        
        line_dark_relpath = join(lines_dir, f'line_dark_{self.line_color}.png')
        self.line_dark = \
            Image.open(resource_path(line_dark_relpath))

    def create_equation_frame(self):
        self.equation_frame = EquationFrame(
            self,
            direction='left',
            frequency=.004,
            until=self.until,
            smooth_slowdown=True,
        )

    def no_movement_place_eq_frame(self):
        self.equation_frame.no_movement_place(relx=.5, rely=.372,
                                              anchor='center')
        
    def _place_equation_frame(self):
        self.equation_frame.place(relx=.5, rely=.372, anchor='center')

    def _place_line_frame(self):
        self.line.place(relx=.5, rely=0, anchor='s')

    def _place_answers_frame(self):
        self.answers_frame.place(relx=.5, rely=1, relwidth=.23,
                                 relheight=.38, anchor='n')
        
    def _place_hint_switch_frame(self):
        self.hint_switch.place(relx=.5, rely=1, anchor='n')

    def _place_counter_frame(self):
        self.counter_frame.place(relx=1, rely=.458, anchor='nw')

    def _create_pies(self, correct_answer_given: bool = None):
        win_moods = ['smiley_1', 'smiley_2', 'happy']
        loose_moods = ['confused_1', 'indifferent', 'thinking_1']

        match self.difficulty:
            case 1:
                if correct_answer_given is None:
                    brown_pi_mood = 'smiley_2'
                    moods = ['indifferent', 'smiley_1', 'thinking_2']
                elif correct_answer_given:
                    brown_pi_mood = 'smiley_1'
                    moods = win_moods
                else:
                    brown_pi_mood = 'indifferent'
                    moods = loose_moods
            case 2:
                if correct_answer_given is None:
                    brown_pi_mood = 'showing'
                    moods = ['indifferent', 'thinking_1', 'thinking_2']
                elif correct_answer_given:
                    brown_pi_mood = 'smiley_1'
                    moods = win_moods
                else:
                    brown_pi_mood = 'indifferent'
                    moods = loose_moods
            case 3:
                if correct_answer_given is None:
                    brown_pi_mood = 'thinking'
                    moods = ['confused_2', 'thinking_1', 'thinking_2']
                elif correct_answer_given:
                    brown_pi_mood = 'smiley_1'
                    moods = win_moods
                else:
                    brown_pi_mood = 'indifferent'
                    moods = loose_moods
        random.shuffle(moods)

        common_for_blue_pies = {
            'width': 60,
            'height': 60,
            'direction': 'up',
            'until': .82,
            'smooth_slowdown': True,
        }
        self.blue_pi_1 = BluePi(
            self,
            mood=moods[0],
            **common_for_blue_pies,
        )
        self.blue_pi_2 = BluePi(
            self,
            mood=moods[1],
            **common_for_blue_pies,
        )
        self.blue_pi_3 = BluePi(
            self,
            mood=moods[2],
            **common_for_blue_pies,
        )

        self.brown_pi = BrownPi(
            self,
            mood=brown_pi_mood,
            width=100,
            height=100,
            direction='left',
            until=.845,
            frequency=.001,
            smooth_slowdown=True,
        )

    def place_pies(self, correct_answer_given=None, after_attempt=False):
        if correct_answer_given is not None or after_attempt:
            ms = 0
        elif correct_answer_given is None:
            ms = self.ms_for_delay + 600
        
        if correct_answer_given is not None and not after_attempt:
            self.after(ms, self.blue_pi_1.unplace)
            self.after(ms + 85, self.blue_pi_2.unplace)
            self.after(ms + 170, self.blue_pi_3.unplace)
            self.after(ms + 255, self.brown_pi.unplace)

            self.after(420, self.blue_pi_1.destroy)
            self.after(520, self.blue_pi_2.destroy)
            self.after(620, self.blue_pi_3.destroy)
            self.after(720, self.brown_pi.destroy)
        else:
            self.after(ms, self.place_blue_pi_1)
            self.after(ms + 85, self.place_blue_pi_2)
            self.after(ms + 170, self.place_blue_pi_3)

            self.after(ms + 255, self.place_brown_pi)

    def place_blue_pi_1(self):
        self.blue_pi_1.place(relx=.06, rely=1, anchor='n')

    def place_blue_pi_2(self):
        self.blue_pi_2.place(relx=.16, rely=1, anchor='n')

    def place_blue_pi_3(self):
        self.blue_pi_3.place(relx=.26, rely=1, anchor='n')

    def place_brown_pi(self):
        self.brown_pi.place(relx=1, rely=.85, anchor='w')


class EquationFrame(CTkMovingFrame):
    def __init__(self, master: Drill, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.eq = QuadraticEquation(master.difficulty)
        # self.eq = '100𝑥² + 200𝑥 + 100 = 0'  # test
        self.eq_label = CTkDelayedLabel(
            self,
            ms=50,
            text=str(self.eq),
            font=ctk.CTkFont(family='Cambria', size=30),
            text_color=('gray20', 'gray90')
        )

    def __getattribute__(self, attr):
        if attr in ['place', 'no_movement_place']:
            self.eq_label.grid(row=0, column=0)
        return object.__getattribute__(self, attr)


class AnswersFrame(CTkMovingFrame):
    def __init__(self, master: Drill, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)

        self.master_ = master
        self.user_answers = []

        self.x_1_var = ctk.StringVar()
        self.x_2_var = ctk.StringVar()

        self._create_solutions()
        self.solutions.grid(row=0, column=0, rowspan=2, padx=(3,0), pady=(5,0))

        self._create_entries()
        self.entry_x_1.grid(row=0, column=1, pady=(3,1))
        self.entry_x_2.grid(row=1, column=1, pady=(0,0))

        self._create_answer_button()
        self.check_answer_button.grid(row=2, column=0, columnspan=2,
                                      sticky='ew', padx=7.5, pady=(3,3))
        
        self._create_skip_button()
        self.skip_button.grid(row=3, column=0, columnspan=2,
                              sticky='ew', padx=7.5, pady=(0,5))
        
        self.master_.bind('<Control-Return>', self.check_button_callback)
        self.master_.frame_for_focus.bind('<1>', self.focus_on_mouse_click)

    def focus_on_mouse_click(self, event):
        self.master_.focus()  # <=> self.master_.frame_for_focus.focus()

    def _create_solutions(self):
        self.solutions = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=self.master_.solutions_dark,
                dark_image=self.master_.solutions_light,
                size=(63, 63),
            ),
        )
        
    def _create_entries(self):
        font_and_size = {
            'font': ctk.CTkFont(family='Book Antiqua', size=18),
            'text_color': ('gray20', 'gray90'),
            'width': 70,
        }
        self.entry_x_1 = ctk.CTkEntry(
            self,
            textvariable=self.x_1_var,
            **font_and_size,
        )
        self.entry_x_2 = ctk.CTkEntry(
            self,
            textvariable=self.x_2_var,
            **font_and_size,
        )

    def _create_answer_button(self):
        if self.master_.line_color == 'blackwhite':
            disabled_color = ('gray40', 'gray75')
        else:
            disabled_color = ('gray40', 'gray60')
        
        self.check_answer_button = ctk.CTkButton(
            self,
            text='Проверить',
            text_color=('gray20', 'gray90'),
            text_color_disabled=disabled_color,
            font=ctk.CTkFont(family='Book Antiqua'),
            command=self.check_button_callback,
        )

    def check_button_callback(self, event=None):
        is_correct: bool = self.is_correct_answer(event=event)
        self.msg = (
            self.master_.correct_msg_frame if is_correct
            else self.master_.incorrect_msg_frame
        )
        loose_msgs = [
            'Неверно; попытайтесь ещё!',
            'Возможно, забыли минус?',
            'Неправильно; ещё одна попытка?',
            'Попытайтесь разложить на другие множители!',
        ]
        if not is_correct:
            self.msg.incorrect_msg.configure(text=random.choice(loose_msgs))

        def action_depends_on_answer(first_place_pies_param):
            self._deactivate_interactivity()

            # replace with happy pies
            self.master_.place_pies(first_place_pies_param, False)
            self.after(
                700,
                lambda: self.master_._create_pies(first_place_pies_param)
            )
            self.after(
                720,
                lambda: self.master_.place_pies(first_place_pies_param, True)
            )
            def tmp():
                self._configure_counter(is_correct)
                self.msg.place(relx=.5, rely=0, anchor='s')
            self.after(720, tmp)

            # replace again, with initial pies
            def tmp():
                self.master_.place_pies(first_place_pies_param, False)
                if is_correct:
                    self.master_._place_equation_frame()
                self.msg.unplace()
            self.after(3000, tmp)
            def tmp():
                self.master_._create_pies()
                if is_correct:
                    self.master_.equation_frame.destroy()
            self.after(3700, tmp)
            def tmp():
                self.master_.place_pies(None, True)
                if is_correct:
                    self.master_.create_equation_frame()
                    self.master_.no_movement_place_eq_frame()
            self.after(3710, tmp)
            self.after(4500, lambda: self._activate_interactivity())

        action_depends_on_answer(is_correct)

    def _create_skip_button(self):
        if self.master_.line_color == 'blackwhite':
            disabled_color = ('gray40', 'gray75')
        else:
            disabled_color = ('gray40', 'gray60')
        
        self.skip_button = ctk.CTkButton(
            self,
            text='Пропустить',
            text_color=('gray20', 'gray90'),
            text_color_disabled=disabled_color,
            font=ctk.CTkFont(family='Book Antiqua'),
            command=self.skip_button_callback,
        )

    def skip_button_callback(self):
        self.skip_button.configure(state='disabled')
        self._deactivate_interactivity()

        self.master_._place_equation_frame()
        self._configure_counter(False, time=700)

        self.after(700, lambda: self.master_.equation_frame.destroy())
        self.after(701, lambda: self.master_.create_equation_frame())
        self.after(701, lambda: self.master_.no_movement_place_eq_frame())

        def tmp():
            self._activate_interactivity()
            self.skip_button.configure(state='normal')
        self.after(self.master_.ms_for_delay + 700, tmp)

    def is_correct_answer(self, event):
        self.answers = self.master_.equation_frame.eq.solutions.copy()
        self.is_correct_answer_x_1(event=event)
        self.is_correct_answer_x_2(event=event)

        is_correct_answer = all(self.user_answers)
        self.user_answers.clear()

        return is_correct_answer

    def is_correct_answer_x_1(self, event):
        answer = self.x_1_var.get()
        checked_answer = self._check_answer(answer)

        self.user_answers.append(checked_answer)

    def is_correct_answer_x_2(self, event):
        answer = self.x_2_var.get()
        checked_answer = self._check_answer(answer)

        self.user_answers.append(checked_answer)
    
    def _check_answer(self, answer: str):
        if answer == 'show_answers':
            print(self.master_.equation_frame.eq.solutions)
        elif answer == 'psts':
            return True
        
        def gcded_answer(answer):
            num, denom = [int(i) for i in answer.split('/')]
            gcd = math.gcd(num, denom)
            num //= gcd
            denom //= gcd
            answer = f'{num}/{denom}' if denom != 1 else num

            return answer
        
        answer = answer.replace(' ', '').replace(',', '.')
        if '/' not in answer:
            answer: float = float(answer)
            if answer.is_integer():
                answer = int(answer)
            else:
                # answer.as_integer_ratio() doesn't work
                # due to the floating point arithmetic
                answer = (
                    f"{str(answer).replace('.', '')}"
                    # below is the 10 ** (amount of digits after the '.')
                    f"/{10 ** len(str(answer).split('.')[1])}"
                )
                answer = gcded_answer(answer)
        else:
            answer = gcded_answer(answer)

        answer = str(answer)

        to_be_returned = answer in self.answers
        if to_be_returned:
            self.answers.remove(answer)

        return to_be_returned

    def _activate_interactivity(self):
        self.check_answer_button.configure(state='normal')
        self.skip_button.configure(state='normal')
        self.entry_x_1.configure(state='normal')
        self.entry_x_2.configure(state='normal')

        self.master_.bind('<Control-Return>', self.check_button_callback)

    def _deactivate_interactivity(self):
        self.check_answer_button.configure(state='disabled')
        self.skip_button.configure(state='disabled')
        self.entry_x_1.configure(state='disabled')
        self.entry_x_2.configure(state='disabled')

        self.x_1_var.set('')
        self.x_2_var.set('')

        try:
            self.master_.unbind('<Control-Return>', self.check_button_callback)
        except TypeError:
            pass

    def _configure_counter(self, is_correct, time=2300):
        self.master_.counter_frame.all_answers += 1
        if is_correct:
            self.master_.counter_frame.correct_user_answers += 1
            self.master_.counter_frame.counter_label.configure(
                text_color=('#00E600', '#00FF00'),
            )
        else:
            self.master_.counter_frame.counter_label.configure(
                text_color=('#F90101', '#FF0000'),
            )

        self.master_.counter_frame.counter_label.configure(
            text=(
                f'{self.master_.counter_frame.correct_user_answers}'
                f'/{self.master_.counter_frame.all_answers}'
            )
        )

        def tmp():
            self.master_.counter_frame.counter_label.configure(
                text_color=('gray20', 'gray90')
            )
        self.after(time, tmp)


class CounterFrame(CTkMovingFrame):
    def __init__(self, master: Drill, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        self.correct_user_answers = 0
        self.all_answers = 0

        self.reference_text = ctk.CTkLabel(
            self,
            text='Правильных ответов/Всего ответов',
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua', size=10),
        )
        self.reference_text.grid(row=0, column=0, padx=12)

        self.counter_label = ctk.CTkLabel(
            self,
            text=f'{self.correct_user_answers}/{self.all_answers}',
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua', size=30),
        )
        self.counter_label.grid(row=1, column=0, pady=(0,6))


class CorrectMsgFrame(CTkMovingFrame):
    def __init__(self, master: Drill, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.correct_msg = ctk.CTkLabel(
            self,
            text='Верно!',
            text_color=('#00E600', '#00FF00'),
            font=ctk.CTkFont(family='Book Antiqua', size=30),
        )
        self.correct_msg.grid()


class IncorrectMsgFrame(CTkMovingFrame):
    def __init__(self, master: Drill, fg_color='transparent', **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.incorrect_msg = ctk.CTkLabel(
            self,
            text='',  # will be configured afterwards
            text_color=('#F90101', '#FF0000'),
            font=ctk.CTkFont(family='Book Antiqua', size=25),
        )
        self.incorrect_msg.grid()
