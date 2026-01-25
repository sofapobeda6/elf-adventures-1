import arcade
from settings import settings
from audio_manager import audio_manager
from hero import Hero

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.TEA_GREEN
        
        self.hero = None
        self.keys_pressed = set()
        
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 900
        
        self.hero_sprite_list = None
        
        self.load_game_music()
        
    def load_game_music(self):
        game_music_paths = [
            r"music/Dragon Teeth On Velvet Streets.mp3"
        ]
        
        audio_manager.stop_music()
        
        for music_path in game_music_paths:
            if audio_manager.load_music(music_path):
                print(f"Игровая музыка загружена: {music_path}")
                if settings.current_settings["music_enabled"]:
                    audio_manager.play_music()
                break
        
    def on_show(self):
        arcade.set_background_color(self.background_color)
        
        if (audio_manager.current_music and 
            not audio_manager.is_music_playing and 
            settings.current_settings["music_enabled"]):
            audio_manager.resume_music()
        
    def setup(self):
        width = self.window.width
        height = self.window.height
        
        self.hero = Hero(width, height)

        self.hero_sprite_list = arcade.SpriteList()
        self.hero_sprite_list.append(self.hero)
        
    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
        if key == arcade.key.ESCAPE:
            audio_manager.stop_music()
            
            from views.menu_view import MenuView
            menu_view = MenuView()
            menu_view.setup()
            self.window.show_view(menu_view)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_update(self, delta_time):
        if not self.hero:
            return
            
        dx, dy = 0, 0
        speed = 500
        
        if (arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed):
            dx -= speed * delta_time
            
        if (arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed):
            dx += speed * delta_time
        
        if arcade.key.SPACE in self.keys_pressed and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = 600
            audio_manager.play_jump_sound()
        
        if self.is_jumping:
            self.jump_velocity -= self.gravity * delta_time
            dy += self.jump_velocity * delta_time
            
            if self.hero.center_y <= self.hero.ground_level + self.hero.height/2:
                self.hero.center_y = self.hero.ground_level + self.hero.height/2
                self.is_jumping = False
                self.jump_velocity = 0
        
        self.hero.center_x += dx
        self.hero.center_y += dy
        
        self.hero.update_state(dx, dy, self.is_jumping)
        
        self.hero.center_x = max(self.hero.width/2, 
                                min(self.window.width - self.hero.width/2, 
                                self.hero.center_x))
        self.hero.center_y = max(self.hero.ground_level + self.hero.height/2, 
                                min(self.window.height - self.hero.height/2, 
                                self.hero.center_y))

    def on_draw(self):
        if not self.hero:
            return
            
        self.clear()
        
        width = self.window.width
        height = self.window.height
        
        ground_height = self.hero.ground_level
        arcade.draw_lrbt_rectangle_filled(
            0, width, 0, ground_height,
            arcade.color.BROWN
        )
        
        self.hero_sprite_list.draw()
        
        controls_font_size = int(24 * (width / 1920))

        arcade.draw_text(
            settings.get_text("menu_controls"), 
            int(30 * (width / 1920)), 
            height - int(50 * (height / 1080)), 
            arcade.color.BLACK, 
            controls_font_size
        )