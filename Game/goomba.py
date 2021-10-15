from pico2d import *

class Goomba:
    def __init__(self):
        self.x, self.y = 1200, 90
        self.image = load_image('Goomba.png')
        self.frame = 0

    def update(self):
        self.x -= 5
        self.frame = (self.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)
