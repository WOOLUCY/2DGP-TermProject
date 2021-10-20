from pico2d import *


class Goomba:
    def __init__(self):
        self.x, self.y = 100, 300
        self.image = load_image('./res/image/Goomba.png')
        self.frame = 0

    def update(self):
        # self.x -= 5
        self.frame = (self.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)


class Bowser:
    def __init__(self):
        self.x, self.y = 200, 300
        self.image = load_image('./res/image/Bowser.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 136, 0, 136, 168, self.x, self.y)