import arcade
from settings import settings
from audio_manager import audio_manager

class SettingsView(arcade.View):
    
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        self.background_color = arcade.color.DARK_SLATE_GRAY
        
        self.background_texture = None
        self.background_sprite = None
        try:
            self.background_texture = arcade.load_texture(r"tiles/1644039805_1-abrakadabra-fun-p-fon-dlya-platformera-1.png")
            print("Фон для настроек успешно загружен")
            
            self.background_sprite = arcade.Sprite()
            self.background_sprite.texture = self.background_texture
        except Exception as e:
            print(f"Ошибка загрузки фона для настроек: {e}")
            self.background_texture = None
            self.background_sprite = None
        
        self.button_width_base = 650
        self.button_height_base = 85
        self.button_spacing_base = 30
        
        self.button_width = self.button_width_base
        self.button_height = self.button_height_base
        self.button_spacing = self.button_spacing_base
        
        self.settings_button_texture = None
        self.setting_sprites = []
        self.setting_sprite_lists = []
        
        try:
            self.settings_button_texture = arcade.load_texture(r"tiles/полное.png")
            print("Текстура для кнопок настроек успешно загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры для кнопок настроек: {e}")
        
        self.back_button = {
            "x": 0,
            "y": 220,
            "width": 400,
            "height": 90
        }
        
        self.save_button = {
            "x": 0,
            "y": 320,
            "width": 400,
            "height": 90
        }
        
        self.back_button_sprite = None
        self.save_button_sprite = None
        self.back_button_sprite_list = None
        self.save_button_sprite_list = None
        
        try:
            action_button_texture = arcade.load_texture(r"tiles/кнопка.png")
            
            self.back_button_sprite = arcade.Sprite()
            self.back_button_sprite.texture = action_button_texture
            self.back_button_sprite_list = arcade.SpriteList()
            self.back_button_sprite_list.append(self.back_button_sprite)
            
            self.save_button_sprite = arcade.Sprite()
            self.save_button_sprite.texture = action_button_texture
            self.save_button_sprite_list = arcade.SpriteList()
            self.save_button_sprite_list.append(self.save_button_sprite)
            
            print("Текстуры для кнопок действий загружены")
        except Exception as e:
            print(f"Ошибка загрузки текстуры для кнопок действий: {e}")
            self.back_button_sprite = None
            self.save_button_sprite = None
        
        self.selected_setting = None
        self.temp_settings = settings.current_settings.copy()
        
    def on_show(self):
        arcade.set_background_color(self.background_color)
        
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
        
        self.setting_sprites = []
        self.setting_sprite_lists = []
        
        for i in range(5):
            sprite = arcade.Sprite()
            if self.settings_button_texture:
                sprite.texture = self.settings_button_texture
            sprite.width = self.button_width
            sprite.height = self.button_height
            
            self.setting_sprites.append(sprite)
            
            sprite_list = arcade.SpriteList()
            sprite_list.append(sprite)
            self.setting_sprite_lists.append(sprite_list)
        
        self.back_button["width"] = int(400 * scale)
        self.back_button["height"] = int(90 * scale)
        self.save_button["width"] = int(400 * scale)
        self.save_button["height"] = int(90 * scale)
        
        self.back_button["x"] = width // 2
        self.back_button["y"] = int(230 * scale)
        self.save_button["x"] = width // 2
        self.save_button["y"] = int(340 * scale)
        
        if self.back_button_sprite:
            self.back_button_sprite.width = self.back_button["width"]
            self.back_button_sprite.height = self.back_button["height"]
            
        if self.save_button_sprite:
            self.save_button_sprite.width = self.save_button["width"]
            self.save_button_sprite.height = self.save_button["height"]
        
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
            (0, 0, 0, 100)
        )
        
        title_font_size = int(56 * (width / 1920))
        setting_font_size = int(34 * (width / 1920))
        button_font_size = int(38 * (width / 1920))
        instruction_font_size = int(24 * (width / 1920))
        
        pale_pink = (255, 200, 210)
        value_pink = (255, 150, 170)
        value_highlight_pink = (255, 180, 200)
        white = (255, 255, 255)
        
        arcade.draw_text(
            settings.get_text("settings_title"),
            width // 2,
            height - 85,
            white,
            title_font_size,
            anchor_x="center",
            bold=True
        )

        y_pos = height - 165
        
        for i in range(5):
            if i == 0:
                name = settings.get_text("language")
                value = f"{settings.get_language_name(self.temp_settings['language'])}"
            elif i == 1:
                name = settings.get_text("sound_volume")
                sound_percent = int(self.temp_settings["sound_volume"] * 100)
                value = f"{sound_percent}%"
            elif i == 2:
                name = settings.get_text("music_volume")
                music_percent = int(self.temp_settings["music_volume"] * 100)
                value = f"{music_percent}%"
            elif i == 3:
                name = settings.get_text("music_enabled")
                music_enabled_text = settings.get_text("enabled") if self.temp_settings["music_enabled"] else settings.get_text("disabled")
                value = music_enabled_text
            elif i == 4:
                name = settings.get_text("sound_effects_enabled")
                sound_enabled_text = settings.get_text("enabled") if self.temp_settings["sound_effects_enabled"] else settings.get_text("disabled")
                value = sound_enabled_text
            
            if i < len(self.setting_sprites):
                sprite = self.setting_sprites[i]
                sprite.center_x = width // 2
                sprite.center_y = y_pos
                
                if self.selected_setting == i:
                    sprite.color = (220, 220, 180)
                else:
                    sprite.color = (255, 255, 255)
                    
                self.setting_sprite_lists[i].draw()
            
            name_y_offset = 3
            name_x = width // 2 - self.button_width // 2 + 35
            
            arcade.draw_text(
                name,
                name_x,
                y_pos + name_y_offset,
                value_pink if self.selected_setting != i else pale_pink,
                setting_font_size,
                anchor_y="center",
                bold=True
            )
            
            value_y_offset = 3
            value_x = width // 2 + self.button_width // 2 - 30
            
            arcade.draw_text(
                value,
                value_x,
                y_pos + value_y_offset,
                value_pink if self.selected_setting != i else value_highlight_pink,
                setting_font_size,
                anchor_x="right",
                anchor_y="center",
                bold=True
            )
            
            y_pos -= self.button_height + self.button_spacing
        
        if self.save_button_sprite_list:
            self.save_button_sprite.center_x = self.save_button["x"]
            self.save_button_sprite.center_y = self.save_button["y"]
            self.save_button_sprite_list.draw()
        else:
            save_left = self.save_button["x"] - self.save_button["width"]/2
            save_right = self.save_button["x"] + self.save_button["width"]/2
            save_bottom = self.save_button["y"] - self.save_button["height"]/2
            save_top = self.save_button["y"] + self.save_button["height"]/2
            
            arcade.draw_lrbt_rectangle_filled(
                save_left, save_right, save_bottom, save_top,
                arcade.color.GREEN
            )
            
            arcade.draw_lrbt_rectangle_outline(
                save_left, save_right, save_bottom, save_top,
                white,
                3
            )
        
        save_text_y_offset = 2
        arcade.draw_text(
            settings.get_text("save_button"),
            self.save_button["x"],
            self.save_button["y"] + save_text_y_offset,
            white,
            button_font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        if self.back_button_sprite_list:
            self.back_button_sprite.center_x = self.back_button["x"]
            self.back_button_sprite.center_y = self.back_button["y"]
            self.back_button_sprite_list.draw()
        else:
            back_left = self.back_button["x"] - self.back_button["width"]/2
            back_right = self.back_button["x"] + self.back_button["width"]/2
            back_bottom = self.back_button["y"] - self.back_button["height"]/2
            back_top = self.back_button["y"] + self.back_button["height"]/2
            
            arcade.draw_lrbt_rectangle_filled(
                back_left, back_right, back_bottom, back_top,
                arcade.color.RED
            )
            
            arcade.draw_lrbt_rectangle_outline(
                back_left, back_right, back_bottom, back_top,
                white,
                3
            )
        
        back_text_y_offset = 2
        arcade.draw_text(
            settings.get_text("back_button"),
            self.back_button["x"],
            self.back_button["y"] + back_text_y_offset,
            white,
            button_font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        instruction_y_offset = 10
        arcade.draw_text(
            settings.get_text("settings_controls"),
            width // 2,
            135 + instruction_y_offset,
            white,
            instruction_font_size,
            anchor_x="center",
            bold=True
        )
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            audio_manager.play_button_click_sound()
            self.window.show_view(self.previous_view)
            
        elif key == arcade.key.ENTER:
            audio_manager.play_menu_select_sound()
            if self.selected_setting is not None:
                self._change_setting()
            else:
                self.save_settings()
                
        elif key == arcade.key.UP:
            audio_manager.play_button_click_sound()
            if self.selected_setting is None:
                self.selected_setting = 0
            else:
                self.selected_setting = max(0, self.selected_setting - 1)
                
        elif key == arcade.key.DOWN:
            audio_manager.play_button_click_sound()
            if self.selected_setting is None:
                self.selected_setting = 0
            else:
                self.selected_setting = min(4, self.selected_setting + 1)
                
        elif key == arcade.key.LEFT:
            audio_manager.play_button_click_sound()
            self._adjust_setting(-1)
            
        elif key == arcade.key.RIGHT:
            audio_manager.play_button_click_sound()
            self._adjust_setting(1)
            
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            audio_manager.play_button_click_sound()
            
            save_left = self.save_button["x"] - self.save_button["width"]/2
            save_right = self.save_button["x"] + self.save_button["width"]/2
            save_bottom = self.save_button["y"] - self.save_button["height"]/2
            save_top = self.save_button["y"] + self.save_button["height"]/2
            
            if save_left <= x <= save_right and save_bottom <= y <= save_top:
                audio_manager.play_menu_select_sound()
                self.save_settings()
                
            back_left = self.back_button["x"] - self.back_button["width"]/2
            back_right = self.back_button["x"] + self.back_button["width"]/2
            back_bottom = self.back_button["y"] - self.back_button["height"]/2
            back_top = self.back_button["y"] + self.back_button["height"]/2
            
            if back_left <= x <= back_right and back_bottom <= y <= back_top:
                audio_manager.play_button_click_sound()
                self.window.show_view(self.previous_view)
            
            y_pos = self.window.height - 165
            for i in range(5):
                left = self.window.width // 2 - self.button_width/2
                right = self.window.width // 2 + self.button_width/2
                bottom = y_pos - self.button_height/2
                top = y_pos + self.button_height/2
                
                if left <= x <= right and bottom <= y <= top:
                    self.selected_setting = i
                    break
                    
                y_pos -= self.button_height + self.button_spacing
                    
    def _change_setting(self):
        if self.selected_setting == 0:
            current_lang = self.temp_settings["language"]
            new_lang = "en" if current_lang == "ru" else "ru"
            self.temp_settings["language"] = new_lang
            settings.localization = settings.load_localization()
            
        elif self.selected_setting == 3:
            self.temp_settings["music_enabled"] = not self.temp_settings["music_enabled"]
            
        elif self.selected_setting == 4:
            self.temp_settings["sound_effects_enabled"] = not self.temp_settings["sound_effects_enabled"]
            
    def _adjust_setting(self, delta):
        if self.selected_setting == 1:
            self.temp_settings["sound_volume"] = max(0.0, min(1.0,
                self.temp_settings["sound_volume"] + delta * 0.1))
                
        elif self.selected_setting == 2:
            self.temp_settings["music_volume"] = max(0.0, min(1.0,
                self.temp_settings["music_volume"] + delta * 0.1))
                
    def save_settings(self):
        settings.current_settings = self.temp_settings.copy()
        settings.save_settings()
        
        settings.localization = settings.load_localization()
        
        audio_manager.update_music_volume()
        
        if not settings.current_settings["music_enabled"]:
            audio_manager.pause_music()
        elif audio_manager.current_music and not audio_manager.is_music_playing:
            audio_manager.resume_music()
        
        from views.menu_view import MenuView
        menu_view = MenuView()
        menu_view.setup()
        self.window.show_view(menu_view)