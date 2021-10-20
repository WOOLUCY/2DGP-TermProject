from pico2d import *


class Coin:
    def __init__(self):
        self.x, self.y = 100, 100
        self.image = load_image('./res/image/coin.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 45, 0, 45, 48, self.x, self.y)


class Block:
    def __init__(self):
        self.x, self.y = 200, 100
        self.image = load_image('./res/image/block.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 3

    def draw(self):
        self.image.clip_draw(self.frame * 48, 0, 48, 48, self.x, self.y)

class Flower:
    def __init__(self):
        self.x, self.y = 300, 100
        self.image = load_image('./res/image/flower.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 48, 0, 48, 48, self.x, self.y)


class Star:
    def __init__(self):
        self.x, self.y = 400, 100
        self.image = load_image('./res/image/star.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 48, 0, 48, 48, self.x, self.y)


class Super_Mushroom:
    def __init__(self):
        self.x, self.y = 500, 100
        self.image = load_image('./res/image/super mushroom.png')

    def update(self):
        # self.x -= 3
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
