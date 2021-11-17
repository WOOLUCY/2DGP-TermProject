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

class Map:
    # global x_dir

    def __init__(self):
        self.x, self.y = 0, 0
        self.image1 = load_image('./res/image/map1.png')
        self.image2 = load_image('./res/image/map2.png')

    def update(self):
        # self.x -= x_dir * 50
        pass

    def draw(self):
        self.image1.clip_draw(0, 0, 5136, 720, self.x + 2568, self.y + 330)


class Cloud:
    # global x_dir

    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('./res/image/cloud1.png')

    def update(self):
        # self.x -= x_dir * 6
        pass

    def draw(self):
        # self.image.draw(642, 420)
        self.image.clip_draw(0, 0, 5000, 720, self.x + 642, self.y + 420)


class Hill:
    def __init__(self):
        self.image = load_image('./res/image/hills.png')

    def draw(self):
        self.image.draw(642, 400)

    def update(self):
        pass