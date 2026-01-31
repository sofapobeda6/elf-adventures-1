import arcade

class Spike(arcade.Sprite):
    def __init__(self, scale=1.1, speed=300, difficulty="medium"):
        super().__init__(":resources:images/tiles/spikes.png", scale=scale)
        self.difficulty = difficulty
        self.speed = speed * 1.2
        self.damage = 1
        
    def update(self, delta_time):
        self.center_x -= self.speed * delta_time