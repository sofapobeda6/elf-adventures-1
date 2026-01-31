import arcade
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from settings_manager import settings_instance
from audio_manager import audio_manager_instance
from views.menu_view import MenuView

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, 
                        fullscreen=settings_instance.current_settings["fullscreen"])
        
        self.set_update_rate(1/60)
        
        menu_view = MenuView()
        menu_view.setup()
        self.show_view(menu_view)
        
    def on_resize(self, width, height):
        if self.current_view and hasattr(self.current_view, 'setup'):
            self.current_view.setup()
        print(f"Окно изменило размер: {width}x{height}")

    def on_close(self):
        print("Игра закрывается...")
        if audio_manager_instance.is_music_playing:
            audio_manager_instance.stop_music()

        settings_instance.save_settings()
        
        self.close()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.getcwd()
    print(f"Текущая рабочая директория: {current_dir}")
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()