import arcade
from settings_manager import settings_instance
from audio_manager import audio_manager_instance
from views.settings_view import SettingsView
from views.game_view import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_BLUE
        self.background_texture = None
        self.background_sprite = None
        
        try:
            self.background_texture = arcade.load_texture(r"tiles/images.png")
            print("Фон меню успешно загружен")
            self.background_sprite = arcade.Sprite()
            self.background_sprite.texture = self.background_texture
        except Exception as e:
            print(f"Ошибка загрузки фона меню: {e}")
            self.background_texture = None
            self.background_sprite = None
        
        self.button_width_base = 400
        self.button_height_base = 100
        self.button_spacing_base = 60
        
        self.button_width = self.button_width_base
        self.button_height = self.button_height_base
        self.button_spacing = self.button_spacing_base
        
        self.play_button_sprite = None
        self.play_button_sprite_list = None
        self.settings_button_sprite = None
        self.settings_button_sprite_list = None
        self.exit_button_sprite = None
        self.exit_button_sprite_list = None
        
        try:
            texture = arcade.load_texture(r"tiles/button.png")
            print("Текстура для кнопок успешно загружена")
            
            self.play_button_sprite = arcade.Sprite()
            self.play_button_sprite.texture = texture
            
            self.settings_button_sprite = arcade.Sprite()
            self.settings_button_sprite.texture = texture
            
            self.exit_button_sprite = arcade.Sprite()
            self.exit_button_sprite.texture = texture
            
            self.play_button_sprite_list = arcade.SpriteList()
            self.play_button_sprite_list.append(self.play_button_sprite)
            
            self.settings_button_sprite_list = arcade.SpriteList()
            self.settings_button_sprite_list.append(self.settings_button_sprite)
            
            self.exit_button_sprite_list = arcade.SpriteList()
            self.exit_button_sprite_list.append(self.exit_button_sprite)
            
        except Exception as e:
            print(f"Ошибка загрузки текстуры кнопки: {e}")
            self.play_button_sprite = None
            self.play_button_sprite_list = None
            self.settings_button_sprite = None
            self.settings_button_sprite_list = None
            self.exit_button_sprite = None
            self.exit_button_sprite_list = None
        
        self.button_scale = 1.0
        self.animation_direction = 1
        self.animation_speed = 0.5
        
        self.play_button = None
        self.settings_button = None
        self.exit_button = None
        
        self.start_y = 0

        self.load_menu_music()
        
    def load_menu_music(self):
        music_paths = [
            r"music/Mystic Sands.mp3"
        ]
        for music_path in music_paths:
            if audio_manager_instance.load_music(music_path):
                print(f"Музыка меню загружена: {music_path}")
                if settings_instance.current_settings["music_enabled"]:
                    audio_manager_instance.play_music()
                break
        
    def on_show(self):
        if (audio_manager_instance.current_music and 
            not audio_manager_instance.is_music_playing and 
            settings_instance.current_settings["music_enabled"]):
            audio_manager_instance.resume_music()
        
    def setup(self):
        width = self.window.width
        height = self.window.height
        
        scale_x = width / 1920
        scale_y = height / 1080
        scale = min(scale_x, scale_y)
        
        self.button_width = int(self.button_width_base * scale)
        self.button_height = int(self.button_height_base * scale)
        self.button_spacing = int(self.button_spacing_base * scale)
        
        if self.background_sprite:
            self.background_sprite.width = width
            self.background_sprite.height = height
            self.background_sprite.center_x = width // 2
            self.background_sprite.center_y = height // 2
        
        if self.play_button_sprite:
            self.play_button_sprite.width = self.button_width
            self.play_button_sprite.height = self.button_height
            
        if self.settings_button_sprite:
            self.settings_button_sprite.width = self.button_width
            self.settings_button_sprite.height = self.button_height
            
        if self.exit_button_sprite:
            self.exit_button_sprite.width = self.button_width
            self.exit_button_sprite.height = self.button_height
        
        self.start_y = height // 2 + self.button_height // 2
        
        self.play_button = {
            "x": width // 2,
            "y": self.start_y,
            "width": self.button_width,
            "height": self.button_height
        }
        
        self.settings_button = {
            "x": width // 2,
            "y": self.start_y - self.button_height - self.button_spacing,
            "width": self.button_width,
            "height": self.button_height
        }
        
        self.exit_button = {
            "x": width // 2,
            "y": self.start_y - (self.button_height + self.button_spacing) * 2,
            "width": self.button_width,
            "height": self.button_height
        }
        
        if self.play_button_sprite:
            self.play_button_sprite.center_x = self.play_button["x"]
            self.play_button_sprite.center_y = self.play_button["y"]
        
        if self.settings_button_sprite:
            self.settings_button_sprite.center_x = self.settings_button["x"]
            self.settings_button_sprite.center_y = self.settings_button["y"]
            
        if self.exit_button_sprite:
            self.exit_button_sprite.center_x = self.exit_button["x"]
            self.exit_button_sprite.center_y = self.exit_button["y"]
        
    def on_draw(self):
        self.clear()
        
        width = self.window.width
        height = self.window.height
        
        if self.background_sprite:
            bg_list = arcade.SpriteList()
            bg_list.append(self.background_sprite)
            bg_list.draw()
        else:
            arcade.set_background_color(self.background_color)
            arcade.draw_lrbt_rectangle_filled(
                0, width, 0, height,
                self.background_color
            )
        
        arcade.draw_lrbt_rectangle_filled(
            0, width, 0, height,
            (0, 0, 0, 128)
        )
        
        title_font_size = int(64 * (width / 1920))
        subtitle_font_size = int(32 * (width / 1920))
        button_font_size = int(36 * (width / 1920))
        instruction_font_size = int(24 * (width / 1920))
        controls_font_size = int(20 * (width / 1920))
        
        white = arcade.color.WHITE
        
        arcade.draw_text(
            settings_instance.get_text("game_title"),
            width // 2,
            height - 350,
            white,
            title_font_size,
            anchor_x="center",
            bold=True
        )
        
        arcade.draw_text(
            settings_instance.get_text("game_subtitle"),
            width // 2,
            height - 240,
            white,
            subtitle_font_size,
            anchor_x="center"
        )
        
        button_scale = self.button_scale
        
        if self.play_button_sprite_list:
            original_width = self.button_width
            original_height = self.button_height
            scaled_width = original_width * button_scale
            scaled_height = original_height * button_scale
            
            self.play_button_sprite.width = scaled_width
            self.play_button_sprite.height = scaled_height
            
            self.play_button_sprite_list.draw()
            
            self.play_button_sprite.width = original_width
            self.play_button_sprite.height = original_height
        else:
            play_width = self.button_width * button_scale
            play_height = self.button_height
            play_left = self.play_button["x"] - play_width/2
            play_right = self.play_button["x"] + play_width/2
            play_bottom = self.play_button["y"] - play_height/2
            play_top = self.play_button["y"] + play_height/2
            
            arcade.draw_lrbt_rectangle_filled(
                play_left, play_right, play_bottom, play_top,
                arcade.color.GREEN
            )
        
        arcade.draw_text(
            settings_instance.get_text("play_button"),
            self.play_button["x"],
            self.play_button["y"],
            white,
            button_font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        if self.settings_button_sprite_list:
            self.settings_button_sprite_list.draw()
        else:
            settings_left = self.settings_button["x"] - self.button_width/2
            settings_right = self.settings_button["x"] + self.button_width/2
            settings_bottom = self.settings_button["y"] - self.button_height/2
            settings_top = self.settings_button["y"] + self.button_height/2
            
            arcade.draw_lrbt_rectangle_filled(
                settings_left, settings_right, settings_bottom, settings_top,
                arcade.color.BLUE
            )
        
        arcade.draw_text(
            settings_instance.get_text("settings_button"),
            self.settings_button["x"],
            self.settings_button["y"],
            white,
            button_font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        if self.exit_button_sprite_list:
            self.exit_button_sprite_list.draw()
        else:
            exit_left = self.exit_button["x"] - self.button_width/2
            exit_right = self.exit_button["x"] + self.button_width/2
            exit_bottom = self.exit_button["y"] - self.button_height/2
            exit_top = self.exit_button["y"] + self.button_height/2
            
            arcade.draw_lrbt_rectangle_filled(
                exit_left, exit_right, exit_bottom, exit_top,
                arcade.color.RED
            )
        
        exit_text = "ВЫХОД" if settings_instance.current_settings["language"] == "ru" else "EXIT"
        arcade.draw_text(
            exit_text,
            self.exit_button["x"],
            self.exit_button["y"],
            white,
            button_font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        difficulty_text = f"{settings_instance.get_text('difficulty_level')} {settings_instance.get_difficulty_name(settings_instance.current_settings['difficulty'])}"
        arcade.draw_text(
            difficulty_text,
            width // 2,
            70,
            white,
            instruction_font_size,
            anchor_x="center",
            bold=True
        )
        
        arcade.draw_text(
            settings_instance.get_text("controls_instruction"),
            width // 2,
            150,
            white,
            instruction_font_size,
            anchor_x="center"
        )
        
        arcade.draw_text(
            settings_instance.get_text("game_controls"),
            width // 2,
            110,
            white,
            controls_font_size,
            anchor_x="center"
        )
        
    def on_update(self, delta_time):
        self.button_scale += self.animation_direction * self.animation_speed * delta_time
        
        if self.button_scale > 1.1:
            self.button_scale = 1.1
            self.animation_direction = -1
        elif self.button_scale < 1.0:
            self.button_scale = 1.0
            self.animation_direction = 1
            
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            audio_manager_instance.play_menu_select_sound()
            self.start_game()
        elif key == arcade.key.S:
            audio_manager_instance.play_menu_select_sound()
            self.open_settings()
        elif key == arcade.key.ESCAPE:
            audio_manager_instance.play_button_click_sound()
            self.window.close()
            
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            audio_manager_instance.play_button_click_sound()
            
            play_left = self.play_button["x"] - self.button_width/2
            play_right = self.play_button["x"] + self.button_width/2
            play_bottom = self.play_button["y"] - self.button_height/2
            play_top = self.play_button["y"] + self.button_height/2
            
            if play_left <= x <= play_right and play_bottom <= y <= play_top:
                audio_manager_instance.play_menu_select_sound()
                self.start_game()
                
            settings_left = self.settings_button["x"] - self.button_width/2
            settings_right = self.settings_button["x"] + self.button_width/2
            settings_bottom = self.settings_button["y"] - self.button_height/2
            settings_top = self.settings_button["y"] + self.button_height/2
            
            if settings_left <= x <= settings_right and settings_bottom <= y <= settings_top:
                audio_manager_instance.play_menu_select_sound()
                self.open_settings()
                
            exit_left = self.exit_button["x"] - self.button_width/2
            exit_right = self.exit_button["x"] + self.button_width/2
            exit_bottom = self.exit_button["y"] - self.button_height/2
            exit_top = self.exit_button["y"] + self.button_height/2
            
            if exit_left <= x <= exit_right and exit_bottom <= y <= exit_top:
                audio_manager_instance.play_button_click_sound()
                self.window.close()
                
    def start_game(self):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
        
    def open_settings(self):
        settings_view = SettingsView(self)
        settings_view.setup()
        self.window.show_view(settings_view)