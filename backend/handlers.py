import darkdetect
import json
import os
import shutil
import sys


def resource_path(relative_path):
    'relative path must be passed with the file itself'

    abs_path = os.path.abspath(relative_path)
    return abs_path


class Settings:

    backend_settings_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'settings.json'
    )
    
    if hasattr(sys, '_MEIPASS'):
        settings_dir_path = \
            os.path.join(os.path.dirname(sys._MEIPASS), '_QE_SETTINGS')
        settings_path = os.path.join(settings_dir_path, 'settings.json')
        if not os.path.exists(settings_dir_path):
            os.mkdir(settings_dir_path)
            shutil.copyfile(backend_settings_path, settings_path)
    else:
        settings_path = backend_settings_path

    @classmethod
    def create_settings(cls) -> dict:
        with open(cls.settings_path) as fp:
            return json.load(fp)
        
    @classmethod
    def update_settings(cls, key, value) -> None:
        with open(cls.settings_path, 'r+') as fp:
            settngs = json.load(fp)

            # delete current content so to write the new one
            fp.seek(0)
            fp.truncate()

            settngs[key] = value
            json.dump(settngs, fp, indent=4)


def _make_ru_en_dict(value, pairs) -> dict[str, str]:
    for pair in pairs:
        if value in pair:
            return {'ru': pair[0], 'en': pair[1]}
        

def _load_theme_or_theme_path(theme: str) -> str:
    if theme in ['blue', 'dark-blue', 'green']:
        return theme
    
    dirname = os.path.dirname
    join = os.path.join
    
    loaded_theme = resource_path(join(
        dirname(dirname(os.path.abspath(__file__))),
        'frontend', 'themes', f'{theme}.json'
    ))

    return loaded_theme


def _create_text(file: str):
    dirname = os.path.dirname
    join = os.path.join

    references_dir = join(
        dirname(dirname(os.path.relpath(__file__))),
        'frontend', 'frames', file
    )

    with open(resource_path(references_dir), encoding='utf-8') as fp:
        data = fp.read()
        return data


# class Font:
#     def __init__(self, font_name):
#         self.font_name: str = font_name  # one of the directories in `assets`
#         self.font_path = os.path.join(
#             os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#             'assets', self.font_name
#         )
#         self.actual_font_names = os.listdir(self.font_path)  # font.ttf
#         self.fonts: list[str] = [
#             os.path.join(self.font_path, font)
#             for font in self.actual_font_names
#         ]
#         self.installed_fonts: list[str] = os.listdir(r'C:\Windows\Fonts')

#     def install(self):
#         for font in self.fonts:
#             # shutil.copy2(
#             #     font,
#             #     # os.path.join(r'C:\Windows\Fonts', os.path.split(font)[1])
#             #     r'C:\Windows\Fonts'
#             # )
#             # # shutil.copystat
#             print('FONT:', font)
#             gdi32.AddFontResourceA(font)
    
#     def requires_installing(self):
#         bools = []
#         for font in self.actual_font_names:
#             bools.append(font not in self.installed_fonts)

#         return all(bools)


def font_requires_installing(font_name):
    font_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'assets', font_name
    )
    actual_font_names = os.listdir(font_path)  # font.ttf
    # fonts: list[str] = [
    #     os.path.join(font_path, font)
    #     for font in actual_font_names
    # ]
    installed_fonts: list[str] = os.listdir(r'C:\Windows\Fonts')
    try:
        installed_fonts_2 = os.listdir(
            r'C:\Users\{0}\AppData\Local\Microsoft\Windows\Fonts'
            .format(os.getlogin())
        )
    except FileNotFoundError:
        installed_fonts_2 = []
    installed_fonts.extend(installed_fonts_2)

    bools = []
    for font in actual_font_names:
        bools.append(font in installed_fonts)

    return not all(bools)


def _create_buttons_from_values_with_condition(self):
    assert len(self._buttons_dict) == 0
    assert len(self._value_list) > 0

    for index, value in enumerate(self._value_list):
        if value == 'Системная' and darkdetect.theme() is None:
            self._state = 'disabled'
        self._buttons_dict[value] = self._create_button(index, value)
        self._configure_button_corners_for_index(index)
