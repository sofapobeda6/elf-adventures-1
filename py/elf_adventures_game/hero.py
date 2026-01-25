import arcade


class Hero(arcade.Sprite):
    def __init__(self, screen_width, screen_height):
        try:
            initial_texture_path = r"tiles/elfStoit.png"
            initial_texture = arcade.load_texture(initial_texture_path)
            super().__init__(initial_texture)
            print("Текстура персонажа загружена")
        except Exception as e:
            print(f"Ошибка загрузки начальной текстуры персонажа: {e}")
            super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png")

        self.scale = 2.5
        
        #размер экрана
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        #начальная позиция
        self.center_x = self.width // 2 + 50
        self.center_y = int(screen_height * 0.15) + self.height // 2
        
        #состояния
        self.is_walking = False
        self.is_jumping = False
        self.facing_left = False
        self.state = "idle"
        
        #анимации перса
        self.textures_dict = {
            "idle_right": None,
            "idle_left": None,
            "walk_right": None,
            "walk_left": None,
            "jump_right": None,
            "jump_left": None
        }
        
        self._load_textures()
        
        #уровень земли
        self.ground_level = int(screen_height * 0.15)

    def _load_textures(self):
        try:
            #в покое вправо
            self.textures_dict["idle_right"] = arcade.load_texture(
                r"tiles/elfStoit.png"
            )
            print("Текстура покоя вправо загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры покоя вправо: {e}")
            self.textures_dict["idle_right"] = arcade.load_texture(
                ":resources:images/animated_characters/female_person/femalePerson_idle.png"
            )
        
        try:
            #в покое влево
            idle_right_texture = self.textures_dict["idle_right"]
            self.textures_dict["idle_left"] = idle_right_texture
            print("Текстура покоя влево создана")
        except Exception as e:
            print(f"Ошибка создания текстуры покоя влево: {e}")
            self.textures_dict["idle_left"] = arcade.load_texture(
                ":resources:images/animated_characters/female_person/femalePerson_idle.png"
            )
        
        try:
            #движение вправо
            self.textures_dict["walk_right"] = arcade.load_texture(
                r"tiles/Elfright1.png"
            )
            print("Текстура движения вправо загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры движения вправо: {e}")
            self.textures_dict["walk_right"] = self.textures_dict["idle_right"]
        
        try:
            #движение влево
            self.textures_dict["walk_left"] = arcade.load_texture(
                r"tiles/Elfleft1.png"
            )
            print("Текстура движения влево загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры движения влево: {e}")
            self.textures_dict["walk_left"] = self.textures_dict["idle_left"]
        
        try:
            #прыжок вправо
            self.textures_dict["jump_right"] = arcade.load_texture(
                r"tiles/Elfright1.png"
            )
            print("Текстура прыжка вправо загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры прыжка вправо: {e}")
            self.textures_dict["jump_right"] = self.textures_dict["walk_right"]
        
        try:
            #прыжок влево
            self.textures_dict["jump_left"] = arcade.load_texture(
                r"tiles/Elfleft1.png"
            )
            print("Текстура прыжка влево загружена")
        except Exception as e:
            print(f"Ошибка загрузки текстуры прыжка влево: {e}")
            self.textures_dict["jump_left"] = self.textures_dict["walk_left"]
        
        #начальную текстуру
        self.texture = self.textures_dict["idle_right"]

    def update_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        #уровень земли
        self.ground_level = int(screen_height * 0.15)
        
        #позицию относительно земли
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
        
        #меняем анимацию перса в зависимости от состояния и направления
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