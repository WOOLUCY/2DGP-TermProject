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
        self.spr.clip_draw(self.frame * self.spr_w, 0, self.spr_w, self.spr_h, self.x, self.y)


class Arrow(Object):
    def __init__(self):
        self.x, self.y = 460, 370
        self.spr_w, self.spr_h = 24, 27
        self.spr = load_image('./res/image/arrow.png')
        self.frame = 0
        self.frame_amount = 2
        self.OnExit = False

    def draw(self):
        if not self.OnExit:
            self.spr.clip_draw(self.frame * 24, 0, 24, 27, self.x, self.y)
        else:
            self.spr.clip_draw(self.frame * 24, 0, 24, 27, self.x, self.y - 60)


class Coin(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr = load_image('./res/image/coin.png')
        self.spr_w = 45
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 4


class Block(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr = load_image('./res/image/block.png')
        self.spr_w = 48
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 3


class Flower(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr = load_image('./res/image/flower.png')
        self.spr_w = 48
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 4


class Star(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr = load_image('./res/image/star.png')
        self.spr_w = 48
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 4


class Super_Mushroom(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 64, 64
        self.spr = load_image('./res/image/super mushroom.png')
        self.frame = 0
        self.frame_amount = 1

