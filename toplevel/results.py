import os
import random

import customtkinter as ctk

from frontend.frames.homeframe import _LineFrame
from frontend.assets import CTkMovingFrame, BluePi, BrownPi

from backend.handlers import Settings, resource_path


class Results(ctk.CTkToplevel):

    width = 650
    height = 357.5

    def __init__(self,
                 correct_user_answers, all_answers, difficulty, master=None,
                 **kwargs):
        super().__init__(master=master, **kwargs)

        self.geometry(f"{self.__class__.width}x{self.__class__.height}")

        icon_relpath = os.path.join(
            os.path.dirname(os.path.relpath(__file__)),
            'images', 'icon.ico'
        )
        self.after(201, lambda: self.iconbitmap(
            resource_path(icon_relpath)
        ))
        
        self.resizable(False, False)
        self.title('Results')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.line_color = Settings.create_settings().get('color_theme')

        self.correct_user_answers = correct_user_answers
        self.all_answers = all_answers
        self.difficulty = difficulty

        self.results_msg_frame = ResultsMsgFrame(
            self,
            self.correct_user_answers,
            self.all_answers,
            self.difficulty,
            direction='up',
            until=.25,
            smooth_slowdown=True,
            frequency=.003,
            fg_color='transparent',
        )
        self.results_msg_frame.place(relx=.5, rely=1, anchor='n')

        self.line_label_frame = _LineFrame(
            self,
            img_width=550,
            img_height=36.18,
            direction='down',
            until=.18,
            smooth_slowdown=True,
        )
        self.line_label_frame.place(relx=.5, rely=0, anchor='s')

        self._create_pies()
        self.after(400, lambda: self._place_pies())

    def _create_moods_depend_on_results(self) -> tuple[list[str], str]:
        percent = self.results_msg_frame.correct_answers_percentage()[0]

        if percent <= 30:
            blue_pi_moods = ['thinking_1', 'thinking_2', 'confused_2']
            brown_pi_mood = 'indifferent'
        elif percent > 30 and percent <= 60:
            blue_pi_moods = ['thinking_1', 'thinking_2', 'indifferent']
            brown_pi_mood = 'speaking'
        elif percent > 60 and percent <= 80:
            blue_pi_moods = ['smiley_1', 'smiley_2', 'indifferent']
            brown_pi_mood = 'smiley_2'
        else:
            blue_pi_moods = ['smiley_1', 'smiley_2', 'happy']
            brown_pi_mood = 'smiley_1'

        random.shuffle(blue_pi_moods)
        return (blue_pi_moods, brown_pi_mood)

    def _create_pies(self):
        moods = self._create_moods_depend_on_results()
        blue_pi_moods = moods[0]
        brown_pi_mood = moods[1]

        common_for_blue_pies = {
            'width': 60,
            'height': 60,
            'direction': 'up',
            'until': .79,
            'smooth_slowdown': True,
        }

        self.blue_pi_1 = BluePi(
            self,
            mood=blue_pi_moods[0],
            **common_for_blue_pies,
        )
        self.blue_pi_2 = BluePi(
            self,
            mood=blue_pi_moods[1],
            **common_for_blue_pies,
        )
        self.blue_pi_3 = BluePi(
            self,
            mood=blue_pi_moods[2],
            **common_for_blue_pies,
        )

        self.brown_pi = BrownPi(
            self,
            mood=brown_pi_mood,
            width=100,
            height=100,
            direction='left',
            until=.825,
            frequency=.001,
            smooth_slowdown=True,
        )

    def _place_pies(self):
        self.after(100, lambda: self.blue_pi_1.place(relx=.07, rely=1, anchor='n'))
        self.after(185, lambda: self.blue_pi_2.place(relx=.18, rely=1, anchor='n'))
        self.after(270, lambda: self.blue_pi_3.place(relx=.29, rely=1, anchor='n'))

        self.after(600, lambda: self.brown_pi.place(relx=1, rely=.83, anchor='w'))


class ResultsMsgFrame(CTkMovingFrame):
    def __init__(self, master, correct_user_answers, all_answers, difficulty,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.correct_user_answers = correct_user_answers
        self.all_answers = all_answers
        self.difficulty = difficulty

        self.results_msg_texbox = ctk.CTkTextbox(
            self,
            width=Results.width * .7,
            height=Results.height * .39,
            border_width=.5,
            border_spacing=8,
            border_color=('gray20', 'gray90'),
            text_color=('gray20', 'gray90'),
            font=ctk.CTkFont(family='Book Antiqua', size=18),
            pady=6,
            wrap='word',
        )
        self.results_msg_texbox.insert('0.0', text=self._create_msg())
        self.results_msg_texbox.tag_add('justify_center', 0.0, 100.0)
        self.results_msg_texbox.tag_config('justify_center', justify='center')
        self.results_msg_texbox.configure(state='disabled')
        self.results_msg_texbox.grid()

    def _create_msg(self) -> str:
        approximately_or_not = 'примерно ' if self.was_approximated() else ''
        percent = self.correct_answers_percentage()[0]
        first_part = [
            f'Ваш результат - {self.correct_user_answers}/{self.all_answers}'
            f', что {approximately_or_not}составляет '
            f'{percent}% правильных ответов.\n\n',  #! comma
            f'Ваше количество верных ответов: {self.correct_user_answers} '
            f'из {self.all_answers} - {approximately_or_not}{percent}%.\n\n',
        ]
        first_part = random.choice(first_part)

        if percent <= 30:
            second_part = (
                'Не следует опускать руки. С небольшими, но регулярными '
                'тренировками Ваш результат безусловно будет выше!'
            )
        elif percent > 30 and percent <= 60:
            second_part = (
                'В следующий раз Ваш результат обязательно будет выше!'
            )
        elif percent > 60 and percent <= 80:
            second_part = (
                'Это хороший результат! Продолжайте в том же духе, '
                'и Вы станете настоящим гуру квадратных уравнений.'
            )
        else:
            if self.difficulty in [1,2]:
                second_part = (
                    'Это отличный результат! Теперь Вы можете испытать '
                    'себя на более высоком уровне сложности.'
                )
            else:
                second_part = (
                    'Это превосходный результат! Вы - настоящий '
                    'гуру в решении квадратных уравнений.'
                )

        if self.all_answers <= 3:
            third_part = (
                '\n\nНо Вы прошли меньше четырёх раундов; '
                'для более точного результата и лучшего навыка '
                'проходите большее количество раундов.'
            )
        elif self.all_answers > 3 and self.all_answers <= 8:
            third_part = (
                '\n\nНо Вы прошли меньше восьми раундов; '
                'постарайтесь испытать себя на большем количестве уравнений!'
            )
        else:
            third_part = ''

        return f'{first_part}{second_part}{third_part}'

    def correct_answers_percentage(self) -> tuple[float, float]:
        result = self.correct_user_answers / self.all_answers * 100
        return (round(result, 2), result)

    def was_approximated(self) -> bool:
        nums_after_point = \
            str(self.correct_answers_percentage()[1]).split('.')[1]
        return len(nums_after_point) >= 3
    