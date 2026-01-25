import os
import json

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TITLE = "ELF ADVENTURES"

class Settings:
    def __init__(self):
        self.settings_file = "game_settings.json"
        self.default_settings = {
            "language": "ru",
            "sound_volume": 0.3,
            "music_volume": 0.5,
            "fullscreen": True,
            "music_enabled": True,
            "sound_effects_enabled": True
        }
        self.current_settings = self.default_settings.copy()
        self.load_settings()
        
        self.localization = self.load_localization()
        
    def load_settings(self): #загрузка настроек
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    for key in self.default_settings:
                        if key in loaded_settings:
                            self.current_settings[key] = loaded_settings[key]
            else:
                print("Файл настроек не найден, используются настройки по умолчанию")
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            
    def save_settings(self): #сохранение настроек 
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_settings, f, indent=4, ensure_ascii=False)
            print(f"Настройки сохранены в {self.settings_file}")
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            
    def load_localization(self): #загрузка локализации
        localizations = {
            "ru": {
                "game_title": "ПРИКЛЮЧЕНИЯ ЭЛЬФА",
                "game_subtitle": "МЕНЮ",
                "play_button": "ИГРАТЬ",
                "settings_button": "НАСТРОЙКИ",
                "back_button": "НАЗАД",
                "save_button": "СОХРАНИТЬ",
                "language": "Язык",
                "sound_volume": "Громкость звуков",
                "music_volume": "Громкость музыки",
                "fullscreen": "Полный экран",
                "music_enabled": "Музыка",
                "sound_effects_enabled": "Звуки",
                "controls_instruction": "Нажмите кнопку 'ИГРАТЬ' или клавишу ENTER",
                "game_controls": "Управление в игре: ←→/AD - движение, ПРОБЕЛ - прыжок",
                "menu_controls": "Управление: ←→/AD - движение, ПРОБЕЛ - прыжок, ESC - меню",
                "settings_title": "НАСТРОЙКИ ИГРЫ",
                "apply_changes": "Применить изменения",
                "settings_controls": "← → для изменения, ENTER для выбора, ESC для отмены",
                "english": "Английский",
                "russian": "Русский",
                "on": "Вкл",
                "off": "Выкл",
                "yes": "Да",
                "no": "Нет",
                "enabled": "Включено",
                "disabled": "Выключено"
            },
            "en": {
                "game_title": "ELF ADVENTURES",
                "game_subtitle": "MENU",
                "play_button": "PLAY",
                "settings_button": "SETTINGS",
                "back_button": "BACK",
                "save_button": "SAVE",
                "language": "Language",
                "sound_volume": "Sound Volume",
                "music_volume": "Music Volume",
                "fullscreen": "Fullscreen",
                "music_enabled": "Music",
                "sound_effects_enabled": "Sounds",
                "controls_instruction": "Press the 'PLAY' button or ENTER key",
                "game_controls": "Game controls: ←→/AD - movement, SPACE - jump",
                "menu_controls": "Controls: ←→/AD - move, SPACE - jump, ESC - menu",
                "settings_title": "GAME SETTINGS",
                "apply_changes": "Apply Changes",
                "settings_controls": "← → to change, ENTER to select, ESC to cancel",
                "english": "English",
                "russian": "Russian",
                "on": "On",
                "off": "Off",
                "yes": "Yes",
                "no": "No",
                "enabled": "Enabled",
                "disabled": "Disabled"
            }
        }
        
        language = self.current_settings.get("language", "ru")
        return localizations.get(language, localizations["ru"])
    
    def get_text(self, key):
        return self.localization.get(key, key)
    
    def change_language(self, language): #смена языка
        if language in ["ru", "en"]:
            self.current_settings["language"] = language
            self.localization = self.load_localization()
            return True
        return False
    
    def get_language_name(self, code):
        languages = {
            "ru": self.get_text("russian"),
            "en": self.get_text("english")
        }
        return languages.get(code, code)
settings = Settings()