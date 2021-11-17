from pico2d import *
import game_world
import game_framework
import time

# BG Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# BG Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class BackGround:
    spr = None
    def __init__(self):
        self.x, self.y = 1284 // 2, 780 // 2
        # self.spr = None
        self.spr_w = 0
        self.spr_h = 0
        self.frame = 0
        self.frame_amount = 0

    def update(self):
        # self.frame = (self.frame + 1) % self.frame_amount
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

    def draw(self):
        self.spr.clip_draw(int(self.frame) * self.spr_w, 0, self.spr_w, self.spr_h, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.spr_w/2, self.y - self.spr_h/2, \
               self.x + self.spr_w/2, self.y + self.spr_h/2


class Map(BackGround):
    def __init__(self):
        self.x, self.y = 0, 0
        self.spr_w = 5136
        self.spr_h = 720
        self.frame = 0
        self.frame_amount = 1

        if Map.spr == None:
            Map.spr = load_image('./res/image/map1.png')

    def update(self):
        pass

    def draw(self):
        self.spr.clip_draw(0, 0, 5136, 720, self.x + 2568, self.y + 330)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.spr_w/2, self.y - self.spr_h/2, \
               self.x + self.spr_w/2, 65


class Cloud(BackGround):
    def __init__(self):
        self.x, self.y = 0, 0
        self.spr_w = 5000
        self.spr_h = 720
        self.frame = 0
        self.frame_amount = 1

        if Cloud.spr == None:
            Cloud.spr = load_image('./res/image/cloud1.png')

    def update(self):
        pass

    def draw(self):
        # self.image.draw(642, 420)
        self.spr.clip_draw(0, 0, 5000, 720, self.x + 642, self.y + 420)


class Hill:
    def __init__(self):
        self.image = load_image('./res/image/hills.png')

    def draw(self):
        self.image.draw(642, 400)

    def update(self):
        pass