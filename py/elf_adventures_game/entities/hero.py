import arcade

class Hero(arcade.Sprite):
    def __init__(self, screen_width, screen_height, difficulty="medium"):
        try:
            initial_texture_path = r"d:/users/sofa/Downloads/elfStoit.png"
            initial_texture = arcade.load_texture(initial_texture_path)
            super().__init__(initial_texture)
            print("Текстура персонажа загружена")
        except Exception as e:
            print(f"Ошибка загрузки начальной текстуры персонажа: {e}")
            super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png")

        self.scale = 2.5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.difficulty = difficulty
        
        if difficulty == "easy":
            self.center_x = self.width // 2 + 100
            self.max_jump_height = 200
        elif difficulty == "medium":
            self.center_x = self.width // 2 + 50
            self.max_jump_height = 200
        elif difficulty == "hard":
            self.center_x = self.width // 2 + 30
            self.max_jump_height = 150
        
        self.center_y = int(screen_height * 0.15) + self.height // 2
        self.ground_level = int(screen_height * 0.15)

        self.is_walking = False
        self.is_jumping = False
        self.facing_left = False
        self.state = "idle"
        
        self.textures_dict = {
            "idle_right": None,
            "idle_left": None,
            "walk_right": None,
            "walk_left": None,
            "jump_right": None,
            "jump_left": None
        }
        
        self._load_textures()

    def _load_textures(self):
        try:
            self.textures_dict["idle_right"] = arcade.load_texture(
                r"d:/users/sofa/Downloads/elfStoit.png"
            )
            print("Текстура покоя вправо загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры покоя вправо: {e}")
            self.textures_dict["idle_right"] = arcade.load_texture(
                ":resources:images/animated_characters/female_person/femalePerson_idle.png"
            )
        
        try:
            idle_right_texture = self.textures_dict["idle_right"]
            self.textures_dict["idle_left"] = idle_right_texture
            print("Текстура покоя влево создана")
        except Exception as e:
            print(f"Ошибка создания текстуры покоя влево: {e}")
            self.textures_dict["idle_left"] = arcade.load_texture(
                ":resources:images/animated_characters/female_person/femalePerson_idle.png"
            )
        
        try:
            self.textures_dict["walk_right"] = arcade.load_texture(
                r"d:/users/sofa/Downloads/Elfright1.png"
            )
            print("Текстура движения вправо загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры движения вправо: {e}")
            self.textures_dict["walk_right"] = self.textures_dict["idle_right"]
        
        try:
            self.textures_dict["walk_left"] = arcade.load_texture(
                r"d:/users/sofa/Downloads/Elfleft1.png"
            )
            print("Текстура движения влево загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры движения влево: {e}")
            self.textures_dict["walk_left"] = self.textures_dict["idle_left"]
        
        try:
            self.textures_dict["jump_right"] = arcade.load_texture(
                r"d:/users/sofa/Downloads/Elfright1.png"
            )
            print("Текстура прыжка вправо загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры прыжка вправо: {e}")
            self.textures_dict["jump_right"] = self.textures_dict["walk_right"]
        
        try:
            self.textures_dict["jump_left"] = arcade.load_texture(
                r"d:/users/sofa/Downloads/Elfleft1.png"
            )
            print("Текстура прыжка влево загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры прыжка влево: {e}")
            self.textures_dict["jump_left"] = self.textures_dict["walk_left"]
        
        self.texture = self.textures_dict["idle_right"]

    def update_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_level = int(screen_height * 0.15)
        self.center_y = self.ground_level + self.height // 2

    def update_state(self, dx, dy, is_jumping):
        self.is_jumping = is_jumping
        
        if dx < 0:
            self.facing_left = True
        elif dx > 0:
            self.facing_left = False
        
        if is_jumping:
            self.state = "jump"
        elif dx != 0:
            self.state = "walk"
        else:
            self.state = "idle"
        
        if self.state == "jump":
            if self.facing_left:
                new_texture = self.textures_dict["jump_left"]
            else:
                new_texture = self.textures_dict["jump_right"]
        elif self.state == "walk":
            if self.facing_left:
                new_texture = self.textures_dict["walk_left"]
            else:
                new_texture = self.textures_dict["walk_right"]
        else:
            if self.facing_left:
                new_texture = self.textures_dict["idle_left"]
            else:
                new_texture = self.textures_dict["idle_right"]
                
        if new_texture and new_texture != self.texture:
            self.texture = new_texture