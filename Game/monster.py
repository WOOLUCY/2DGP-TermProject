from pico2d import *


class Monster:
    spr = None

    def __init__(self):
        self.x, self.y = 1284 // 2, 780 // 2
        # self.spr = None
        self.spr_w, spr_h = 0, 0
        self.frame = 0
        self.frame_amount = 0

    def update(self):
        self.frame = (self.frame + 1) % self.frame_amount

    def draw(self):
        self.spr.clip_draw(self.frame * self.spr_w, 0, self.spr_w, self.spr_h, self.x, self.y)


class Goomba(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        # self.spr = load_image('./res/image/Goomba.png')
        self.spr_w, self.spr_h = 64, 64
        self.frame = 0
        self.frame_amount = 2
        if Goomba.spr == None:
            Goomba.spr = load_image('./res/image/Goomba.png')
        self.x_dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 2
        self.x += self.x_dir * 20
        if self.x < 1200:
            self.x_dir = 1


class Koopa_Troopa(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 48, 64
        self.frame = 0
        self.frame_amount = 2
        if Koopa_Troopa.spr == None:
            Koopa_Troopa.spr = load_image('./res/image/Koopa Troopa.png')

    def update(self):
        self.x -= 5
        self.frame = (self.frame + 1) % 2


class Koopa_Troopa_Shell(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 32, 32
        self.frame = 0
        self.frame_amount = 4
        if Koopa_Troopa_Shell.spr == None:
            Koopa_Troopa_Shell.spr = load_image('./res/image/Shell.png')



class Piranha_Plant(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 64, 64
        self.frame = 0
        self.frame_amount = 2
        if Piranha_Plant.spr == None:
            Piranha_Plant.spr = load_image('./res/image/Piranha Plant.png')


class Bowser(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 136, 168
        self.frame = 0
        self.frame_amount = 4
        if Bowser.spr == None:
            Bowser.spr = load_image('./res/image/Bowser.png')
