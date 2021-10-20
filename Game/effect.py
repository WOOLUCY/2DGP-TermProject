from pico2d import *


class Coin_Effect:
    def __init__(self):
        self.x, self.y = 100, 500
        self.image = load_image('./res/image/coin effect.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 5

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 32, self.x, self.y)