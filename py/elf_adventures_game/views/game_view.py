import arcade
import os
import json
import random
import math
from entities.hero import Hero
from entities.obstacle import Obstacle
from entities.spike import Spike
from settings_manager import settings_instance
from audio_manager import audio_manager_instance

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.TEA_GREEN
        
        self.hero = None
        self.keys_pressed = set()
        
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 900
        self.jump_start_time = 0
        self.max_jump_duration = 0.3
        
        self.obstacle_list = None
        self.flying_obstacle_list = None
        self.spike_list = None
        self.score = 0
        self.high_score = 0
        self.game_over = False
        
        self.obstacle_timer = 0
        self.obstacle_interval = 2.0
        self.spike_timer = 0
        self.spike_interval = 5.0
        
        self.background_list = None
        self.cloud_list = None
        self.hero_sprite_list = None
        
        self.load_game_music()
        
    def load_game_music(self):
        game_music_paths = [
            r"music/Dragon Teeth On Velvet Streets.mp3"
        ]
        
        audio_manager_instance.stop_music()
        
        for music_path in game_music_paths:
            if audio_manager_instance.load_music(music_path):
                print(f"Игровая музыка загружена: {music_path}")
                if settings_instance.current_settings["music_enabled"]:
                    audio_manager_instance.play_music()
                break
        
    def on_show(self):
        arcade.set_background_color(self.background_color)
        
        if (audio_manager_instance.current_music and 
            not audio_manager_instance.is_music_playing and 
            settings_instance.current_settings["music_enabled"]):
            audio_manager_instance.resume_music()
        
    def setup(self):
        width = self.window.width
        height = self.window.height
        
        current_difficulty = settings_instance.current_settings["difficulty"]
        
        self.hero = Hero(width, height, current_difficulty)
        
        self.hero_sprite_list = arcade.SpriteList()
        self.hero_sprite_list.append(self.hero)
        self.obstacle_list = arcade.SpriteList()
        self.flying_obstacle_list = arcade.SpriteList()
        self.spike_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.cloud_list = arcade.SpriteList()
        
        self.is_jumping = False
        self.jump_velocity = 0
        self.jump_start_time = 0
        self.keys_pressed.clear()
        self.game_over = False
        
        if current_difficulty == "easy":
            self.obstacle_interval = 2.5
        elif current_difficulty == "medium":
            self.obstacle_interval = 2.0
        elif current_difficulty == "hard":
            self.obstacle_interval = 1.5
            self.spike_interval = 4.0
        
        self.load_high_score()
        self.create_background()

    def create_background(self):
        for i in range(5):
            cloud_types = [
                r"tiles/cloud 1.png",
                r"tiles/cloud 2.png", 
                r"tiles/cloud 3.png"
            ]
            
            cloud_path = random.choice(cloud_types)
            
            try:
                cloud = arcade.Sprite(cloud_path, scale=0.5)
            except:
                cloud = arcade.Sprite(":resources:images/topdown_tanks/treeGreen_small.png", scale=0.5)
            
            cloud.center_x = random.randint(100, self.window.width)
            cloud.center_y = random.randint(self.window.height // 2, self.window.height - 10)
            cloud.speed = random.uniform(10, 30)
            self.cloud_list.append(cloud)
    
    def load_high_score(self):
        try:
            with open("high_score.json", "r") as f:
                data = json.load(f)
                self.high_score = data.get("high_score", 0)
        except:
            self.high_score = 0
    
    def save_high_score(self):
        with open("high_score.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)
    
    def spawn_obstacle(self):
        ground_obstacle_types = [
            (r"tiles/obstacle 1.png", 0.3),
            (r"tiles/obstacle 2.png", 0.3),
            (r"tiles/obstacle 3.png", 0.3),
            (r"tiles/obstacle 4.png", 0.3),
        ]
        
        flying_obstacle_types = [
            (r"tiles/obstacle fly 1.png", 0.2),
        ]
        
        current_difficulty = settings_instance.current_settings["difficulty"]
        flying_chance = 0.3
        if current_difficulty == "hard":
            flying_chance = 0.4
        
        obstacle_type = "flying" if random.random() < flying_chance else "ground"
        
        if obstacle_type == "ground":
            available_obstacles = []
            for img_path, scale in ground_obstacle_types:
                if os.path.exists(img_path):
                    available_obstacles.append((img_path, scale, "ground"))
            
            if not available_obstacles:
                available_obstacles = [
                    (":resources:images/tiles/boxCrate_double.png", 0.5, "ground"),
                    (":resources:images/tiles/grassHalf_left.png", 1.0, "ground"),
                ]
        else:
            available_obstacles = []
            for img_path, scale in flying_obstacle_types:
                if os.path.exists(img_path):
                    available_obstacles.append((img_path, scale, "flying"))
            
            if not available_obstacles:
                available_obstacles = [
                    (":resources:images/enemies/slimeBlue.png", 0.8, "flying"),
                    (":resources:images/enemies/fly.png", 1.0, "flying"),
                ]
        
        if not available_obstacles:
            return
        
        img_path, base_scale, obs_type = random.choice(available_obstacles)
        
        if obs_type == "ground":
            if current_difficulty == "easy":
                base_speed = 300
                obstacle_scale = base_scale * random.uniform(0.7, 0.9)
            elif current_difficulty == "medium":
                base_speed = 420
                obstacle_scale = base_scale * random.uniform(0.8, 1.2)
            elif current_difficulty == "hard":
                base_speed = 500
                obstacle_scale = base_scale * random.uniform(1.0, 1.5)
        else:
            if current_difficulty == "easy":
                base_speed = 300
                obstacle_scale = base_scale * random.uniform(0.6, 0.8)
            elif current_difficulty == "medium":
                base_speed = 400
                obstacle_scale = base_scale * random.uniform(0.7, 1.0)
            elif current_difficulty == "hard":
                base_speed = 480
                obstacle_scale = base_scale * random.uniform(0.9, 1.3)
        
        obstacle = Obstacle(img_path, scale=obstacle_scale, speed=base_speed, 
                          difficulty=current_difficulty, obstacle_type=obs_type)
        
        obstacle.left = self.window.width
        
        if obs_type == "ground":
            obstacle.bottom = self.hero.ground_level
            self.obstacle_list.append(obstacle)
        else:
            min_height = self.hero.ground_level + 80
            max_height = self.hero.ground_level + 150
            
            obstacle.center_y = random.uniform(min_height, max_height)
            obstacle.original_y = obstacle.center_y
            self.flying_obstacle_list.append(obstacle)
    
    def spawn_spike(self):
        current_difficulty = settings_instance.current_settings["difficulty"]
        
        if current_difficulty != "hard":
            return
        
        spike = Spike(scale=1.1, speed=360, difficulty=current_difficulty)
        
        spike.left = self.window.width
        spike.bottom = self.hero.ground_level
        
        self.spike_list.append(spike)
        
    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if self.game_over and key == arcade.key.SPACE:
            self.setup()
            self.score = 0
            return
        
        if key == arcade.key.ESCAPE:
            audio_manager_instance.stop_music()
            
            from views.menu_view import MenuView
            menu_view = MenuView()
            menu_view.setup()
            self.window.show_view(menu_view)
        
    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            
        if key == arcade.key.SPACE and self.is_jumping:
            self.is_jumping = False
    
    def on_update(self, delta_time):
        if self.game_over:
            return
        
        if not self.hero:
            return
            
        dx, dy = 0, 0
        
        current_difficulty = settings_instance.current_settings["difficulty"]
        if current_difficulty == "easy":
            speed = 400
        elif current_difficulty == "medium":
            speed = 450
        elif current_difficulty == "hard":
            speed = 500

        self.obstacle_list.update(delta_time)
        self.flying_obstacle_list.update(delta_time)
        self.spike_list.update(delta_time)
        
        for obstacle in self.obstacle_list:
            if obstacle.right < 0:
                obstacle.remove_from_sprite_lists()
                if current_difficulty == "easy":
                    self.score += 10
                elif current_difficulty == "medium":
                    self.score += 15
                elif current_difficulty == "hard":
                    self.score += 20
        
        for obstacle in self.flying_obstacle_list:
            if obstacle.right < 0:
                obstacle.remove_from_sprite_lists()
                if current_difficulty == "easy":
                    self.score += 15
                elif current_difficulty == "medium":
                    self.score += 25
                elif current_difficulty == "hard":
                    self.score += 30
        
        for spike in self.spike_list:
            if spike.right < 0:
                spike.remove_from_sprite_lists()
        
        self.obstacle_timer += delta_time
        if self.obstacle_timer >= self.obstacle_interval:
            self.spawn_obstacle()
            if current_difficulty == "easy":
                self.obstacle_interval = random.uniform(2.0, 3.0)
            elif current_difficulty == "medium":
                self.obstacle_interval = random.uniform(1.5, 2.5)
            elif current_difficulty == "hard":
                self.obstacle_interval = random.uniform(1.0, 2.0)
            self.obstacle_timer = 0
        
        if current_difficulty == "hard":
            self.spike_timer += delta_time
            if self.spike_timer >= self.spike_interval:
                self.spawn_spike()
                self.spike_interval = random.uniform(3.0, 5.0)
                self.spike_timer = 0
        
        for cloud in self.cloud_list:
            cloud.center_x -= cloud.speed * delta_time
            if cloud.right < 0:
                cloud.left = self.window.width
                cloud.center_y = random.randint(self.window.height // 2, self.window.height - 100)
        
        if arcade.check_for_collision_with_list(self.hero, self.obstacle_list):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
        
        if arcade.check_for_collision_with_list(self.hero, self.flying_obstacle_list):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
        
        if current_difficulty == "hard":
            if arcade.check_for_collision_with_list(self.hero, self.spike_list):
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
        
        if current_difficulty == "easy":
            self.score += delta_time * 5
        elif current_difficulty == "medium":
            self.score += delta_time * 8
        elif current_difficulty == "hard":
            self.score += delta_time * 10
        
        if (arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed):
            dx -= speed * delta_time
            
        if (arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed):
            dx += speed * delta_time
        
        if arcade.key.SPACE in self.keys_pressed:
            if not self.is_jumping and self.hero.center_y <= self.hero.ground_level + self.hero.height/2 + 10:
                self.is_jumping = True
                self.jump_start_time = 0
                
                if current_difficulty == "easy":
                    self.jump_velocity = 650
                elif current_difficulty == "medium":
                    self.jump_velocity = 600
                elif current_difficulty == "hard":
                    self.jump_velocity = 550
                
                audio_manager_instance.play_jump_sound()
        
        if self.is_jumping:
            self.jump_start_time += delta_time
            if arcade.key.SPACE in self.keys_pressed and self.jump_start_time < self.max_jump_duration:
                dy += self.jump_velocity * delta_time
            else:
                self.jump_velocity -= self.gravity * delta_time
                dy += self.jump_velocity * delta_time
                
                if self.hero.center_y <= self.hero.ground_level + self.hero.height/2:
                    self.hero.center_y = self.hero.ground_level + self.hero.height/2
                    self.is_jumping = False
                    self.jump_velocity = 0
        else:
            if self.hero.center_y > self.hero.ground_level + self.hero.height/2:
                self.jump_velocity -= self.gravity * delta_time
                dy += self.jump_velocity * delta_time
                
                if self.hero.center_y <= self.hero.ground_level + self.hero.height/2:
                    self.hero.center_y = self.hero.ground_level + self.hero.height/2
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
        
        for cloud in self.cloud_list:
            cloud.center_x -= cloud.speed * delta_time
            
            if cloud.right < 0:
                cloud.left = self.window.width
                
                cloud_paths = [
                    r"tiles/cloud 1",
                    r"tiles/cloud 2.png", 
                    r"tiles/cloud 3.png"
                ]
                
                available_clouds = []
                for cloud_path in cloud_paths:
                    if os.path.exists(cloud_path):
                        available_clouds.append(cloud_path)
                
                if available_clouds:
                    try:
                        new_texture_path = random.choice(available_clouds)
                        cloud.texture = arcade.load_texture(new_texture_path)
                    except:
                        pass
                
                cloud.center_y = random.randint(self.window.height // 2, self.window.height - 100)
                cloud.speed = random.uniform(20, 60)
                cloud.scale = random.uniform(0.3, 0.7)
                if random.random() > 0.7:
                    cloud.alpha = random.randint(180, 230)
                else:
                    cloud.alpha = 255

    def on_draw(self):
        if not self.hero:
            return
            
        self.clear()
        
        width = self.window.width
        height = self.window.height
        
        arcade.draw_lrbt_rectangle_filled(
            0,
            width,
            0,
            height,
            arcade.color.SKY_BLUE
        )
        
        self.cloud_list.draw()
        
        ground_height = self.hero.ground_level
        soft_green = (120, 200, 120)
        
        arcade.draw_lrbt_rectangle_filled(
            0,
            width,
            0,
            ground_height,
            soft_green
        )
        
        dark_soft_green = (80, 160, 80)
        arcade.draw_lrbt_rectangle_filled(
            0,
            width,
            ground_height - 10,
            ground_height,
            dark_soft_green
        )
        
        current_difficulty = settings_instance.current_settings["difficulty"]
        if current_difficulty == "hard":
            self.spike_list.draw()
        
        self.hero_sprite_list.draw()
        
        self.obstacle_list.draw()
        self.flying_obstacle_list.draw()
        
        dark_blue = arcade.color.DARK_BLUE
        
        difficulty_text = f"{settings_instance.get_text('difficulty_level')} {settings_instance.get_difficulty_name(settings_instance.current_settings['difficulty'])}"
        
        panel_width = 400
        panel_height = 180
        panel_x = 40
        panel_y = height - panel_height - 20
        
        arcade.draw_lrbt_rectangle_filled(
            panel_x,
            panel_x + panel_width,
            panel_y,
            panel_y + panel_height,
            (255, 255, 255, 220)
        )
        
        arcade.draw_lrbt_rectangle_outline(
            panel_x,
            panel_x + panel_width,
            panel_y,
            panel_y + panel_height,
            dark_blue,
            border_width=3
        )
        
        arcade.draw_lrbt_rectangle_outline(
            panel_x + 5,
            panel_x + panel_width - 5,
            panel_y + 5,
            panel_y + panel_height - 5,
            dark_blue,
            border_width=2
        )
        
        score_text = f"{settings_instance.get_text('score')}:"
        high_score_text = f"{settings_instance.get_text('high_score')}:"
        
        arcade.draw_text(
            score_text,
            panel_x + 30,
            panel_y + panel_height - 60,
            dark_blue,
            28,
            bold=True
        )
        
        arcade.draw_text(
            high_score_text,
            panel_x + 30,
            panel_y + panel_height - 120,
            dark_blue,
            28,
            bold=True
        )
        
        arcade.draw_text(
            f"{int(self.score)}",
            panel_x + panel_width - 40,
            panel_y + panel_height - 60,
            arcade.color.RED,
            42,
            anchor_x="right",
            bold=True
        )
        
        arcade.draw_text(
            f"{int(self.high_score)}",
            panel_x + panel_width - 40,
            panel_y + panel_height - 120,
            arcade.color.PURPLE,
            42,
            anchor_x="right",
            bold=True
        )
        
        arcade.draw_text(
            difficulty_text,
            panel_x + 20,
            panel_y + 20,
            dark_blue,
            22,
            bold=True
        )
        
        controls_text = settings_instance.get_text("menu_controls")
        controls_font_size = int(24 * (width / 1920))
        
        arcade.draw_lrbt_rectangle_filled(
            20,
            1000,
            60,
            120,
            (255, 255, 255, 200)
        )
        
        arcade.draw_lrbt_rectangle_outline(
            20,
            1000,
            60,
            120,
            dark_blue,
            border_width=2
        )
        
        arcade.draw_text(
            controls_text,
            40,
            90,
            dark_blue,
            controls_font_size,
            bold=True
        )
        
        if self.game_over:
            panel_width = 700
            panel_height = 360
            panel_x = width // 2 - panel_width // 2
            panel_y = height // 2 - panel_height // 2
            
            arcade.draw_lrbt_rectangle_filled(
                panel_x,
                panel_x + panel_width,
                panel_y,
                panel_y + panel_height,
                arcade.color.WHITE
            )
            
            arcade.draw_lrbt_rectangle_outline(
                panel_x,
                panel_x + panel_width,
                panel_y,
                panel_y + panel_height,
                arcade.color.BLACK,
                border_width=3
            )
            
            arcade.draw_lrbt_rectangle_outline(
                panel_x + 10,
                panel_x + panel_width - 10,
                panel_y + 10,
                panel_y + panel_height - 10,
                arcade.color.RED,
                border_width=2
            )
            
            arcade.draw_text(
                settings_instance.get_text("game_over"),
                width // 2,
                panel_y + panel_height - 70,
                arcade.color.RED,
                58,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
            
            final_difficulty_text = f"Сложность: {settings_instance.get_difficulty_name(settings_instance.current_settings['difficulty'])}"
            arcade.draw_text(
                final_difficulty_text,
                width // 2,
                panel_y + panel_height - 140,
                dark_blue,
                34,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
            
            final_score_text = f"{settings_instance.get_text('final_score')}: {int(self.score)}"
            arcade.draw_text(
                final_score_text,
                width // 2,
                panel_y + panel_height - 200,
                dark_blue,
                46,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
            
            if self.score == self.high_score and self.high_score > 0:
                new_record_text = f"{settings_instance.get_text('high_score')}!"
                arcade.draw_text(
                    new_record_text,
                    width // 2,
                    panel_y + panel_height - 260,
                    arcade.color.GOLD,
                    40,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )
            
            arcade.draw_text(
                settings_instance.get_text("restart"),
                width // 2,
                panel_y + 60,
                dark_blue,
                34,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )