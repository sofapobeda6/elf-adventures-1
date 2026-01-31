import arcade
import random
import math

class Obstacle(arcade.Sprite):
    def __init__(self, image_path, scale=1.5, speed=300, difficulty="medium", obstacle_type="ground"):
        super().__init__(image_path, scale=scale)
        
        self.obstacle_type = obstacle_type
        self.difficulty = difficulty
        
        self.oscillation_amplitude = 0
        self.oscillation_speed = 0
        self.oscillation_time = random.uniform(0, math.pi * 2)
        self.original_y = 0
        
        if obstacle_type == "ground":
            if difficulty == "easy":
                self.speed = speed
                self.scale = scale * 0.9
                self.damage = 1
            elif difficulty == "medium":
                self.speed = speed * 1.4
                self.scale = scale
                self.damage = 1
            elif difficulty == "hard":
                self.speed = speed * 1.4
                self.scale = scale * 1.3
                self.damage = 1
        else:
            if difficulty == "easy":
                self.speed = speed
                self.scale = scale * 0.9
                self.damage = 1
                self.oscillation_amplitude = random.uniform(10, 30)
                self.oscillation_speed = random.uniform(0.5, 1.5)
            elif difficulty == "medium":
                self.speed = speed * 1.4
                self.scale = scale
                self.damage = 1
                self.oscillation_amplitude = random.uniform(20, 50)
                self.oscillation_speed = random.uniform(1.0, 2.0)
            elif difficulty == "hard":
                self.speed = speed * 1.5
                self.scale = scale * 1.3
                self.damage = 1
                self.oscillation_amplitude = random.uniform(30, 80)
                self.oscillation_speed = random.uniform(1.5, 3.0)
        
    def update(self, delta_time):
        self.center_x -= self.speed * delta_time

        if self.obstacle_type == "flying":
            self.oscillation_time += self.oscillation_speed * delta_time
            self.center_y = self.original_y + math.sin(self.oscillation_time) * self.oscillation_amplitude