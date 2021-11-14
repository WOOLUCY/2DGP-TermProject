from pico2d import *
import game_framework

# Monster Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 15.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Monster Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Monster:
    spr = None

    def __init__(self):
        self.x, self.y = 1284 // 2, 780 // 2
        # self.spr = None
        self.spr_w, spr_h = 0, 0
        self.frame = 0
        self.frame_amount = 0

    def update(self):
        # self.frame = (self.frame + 1) % self.frame_amount
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

    def draw(self):
        self.spr.clip_draw(int(self.frame) * self.spr_w, 0, self.spr_w, self.spr_h, self.x, self.y)


class Goomba(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        # self.spr = load_image('./res/image/Goomba.png')
        self.spr_w, self.spr_h = 64, 64
        self.frame = 0
        self.frame_amount = 2
        if Goomba.spr == None:
            Goomba.spr = load_image('./res/image/Goomba.png')
        self.velocity = 1

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount
        self.x += self.velocity * game_framework.frame_time
        if self.x < 1200:
            self.velocity = 1

    def draw(self):
        self.spr.clip_draw(int(self.frame) * self.spr_w, 0, self.spr_w, self.spr_h, self.x, self.y)
        debug_print('Velocity :' + str(self.velocity))


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
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount


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
