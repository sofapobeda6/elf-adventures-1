import os
import arcade

class AudioManager:
    def __init__(self):
        self.music_player = None
        self.current_music = None
        self.is_music_playing = False

        self.jump_sound = None
        self.menu_select_sound = None
        self.button_click_sound = None

        self.load_sounds()
        
    def load_sounds(self):
        try:
            self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")
            self.menu_select_sound = arcade.load_sound(":resources:sounds/coin2.wav")
            self.button_click_sound = arcade.load_sound(":resources:sounds/rockHit2.wav")
            print("Звуковые эффекты загружены")
        except Exception as e:
            print(f"Ошибка загрузки звуковых эффектов: {e}")
    
    def load_music(self, music_file_path):
        try:
            if os.path.exists(music_file_path):
                self.current_music = arcade.load_sound(music_file_path)
                print(f"Музыка загружена: {music_file_path}")
                return True
            else:
                print(f"Файл музыки не найден: {music_file_path}")
                return False
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")
            return False
    
    def play_music(self, loop=True):
        from settings_manager import settings_instance
        
        if (self.current_music and 
            settings_instance.current_settings["music_enabled"] and 
            settings_instance.current_settings["music_volume"] > 0):
            
            if self.music_player:
                self.stop_music()
            
            volume = settings_instance.current_settings["music_volume"]
            self.music_player = self.current_music.play(volume=volume, loop=loop)
            self.is_music_playing = True
            print(f"Музыка начала играть (громкость: {volume})")
            
    def stop_music(self):
        if self.current_music and self.music_player:
            self.current_music.stop(self.music_player)
            self.music_player = None
            self.is_music_playing = False
            print("Музыка остановлена")
    
    def pause_music(self):
        if self.current_music and self.music_player:
            self.current_music.pause(self.music_player)
            self.is_music_playing = False
            print("Музыка на паузе")
    
    def resume_music(self):
        from settings_manager import settings_instance
        
        if (self.current_music and self.music_player and 
            settings_instance.current_settings["music_enabled"]):
            
            volume = settings_instance.current_settings["music_volume"]
            self.current_music.resume(self.music_player)
            self.is_music_playing = True
            print("Музыка возобновлена")
    
    def update_music_volume(self):
        from settings_manager import settings_instance
        
        if self.current_music and self.music_player and self.is_music_playing:
            volume = settings_instance.current_settings["music_volume"]
            if settings_instance.current_settings["music_enabled"] and volume > 0:
                was_playing = self.is_music_playing
                self.stop_music()
                if was_playing:
                    self.play_music()
    
    def play_sound_effect(self, sound, volume_multiplier=1.0):
        from settings_manager import settings_instance
        
        if (sound and 
            settings_instance.current_settings["sound_effects_enabled"] and 
            settings_instance.current_settings["sound_volume"] > 0):
            
            volume = settings_instance.current_settings["sound_volume"] * volume_multiplier
            sound.play(volume=volume)
    
    def play_jump_sound(self):
        self.play_sound_effect(self.jump_sound)
    
    def play_menu_select_sound(self):
        self.play_sound_effect(self.menu_select_sound, 0.7)
    
    def play_button_click_sound(self):
        self.play_sound_effect(self.button_click_sound, 0.5)


audio_manager_instance = AudioManager()