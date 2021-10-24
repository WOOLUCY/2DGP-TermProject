from pico2d import *

class Object:
    def __init__(self):
        self.x, self.y = 1284 // 2, 780 // 2
        self.spr = None
        self.spr_w = 0
        self.spr_h = 0
        self.frame = 0
        self.frame_amount = 0

    def update(self):
        self.frame = (self.frame + 1) % self.frame_amount
        
    def draw(self):
        self.image.clip_draw(self.frame * self.spr_w, 0, self.spr_w, self.spr_h)


class Arrow:

    def __init__(self):
        self.x, self.y = 460, 370
        self.image = load_image('./res/image/arrow.png')
        self.frame = 0
        self.OnExit = False

    def update(self):
        self.frame = (self.frame + 1) % 2

    def draw(self):
        if not self.OnExit:
            self.image.clip_draw(self.frame * 24, 0, 24, 27, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 24, 0, 24, 27, self.x, self.y - 60)


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
        self.x_dir = 0;
        self.image = load_image('./res/image/super mushroom.png')

    def update(self):
        if self.x <= 900:
            self.x_dir += 1
        else:
            self.x_dir -= 1
        self.x += self.x_dir * 1
        pass

    def draw(self):
        self.image.draw(self.x, self.y)


