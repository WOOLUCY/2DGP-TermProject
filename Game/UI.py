from pico2d import *
import game_framework
import time

# UI Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3


class UI:
    spr = None

    def __init__(self, x = 400, y = 300):
        self.x, self.y = x, y
        self.spr_w = 0
        self.spr_h = 0
        self.frame = 0
        self.frame_amount = 0

    def update(self):
        # self.frame = (self.frame + 1) % self.frame_amount
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

    def draw(self):
        self.spr.clip_draw(int(self.frame) * self.spr_w, 0, self.spr_w, self.spr_h, self.x, self.y)


class CoinNum(UI):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 15, 24
        self.frame = 0
        self.frame_amount = 3

        if CoinNum.spr == None:
            CoinNum.spr = load_image('./res/image/HUD_coin.png')


class Top(UI):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 450, 60
        self.frame = 0
        self.frame_amount = 1

        if Top.spr == None:
            Top.spr = load_image('./res/image/top.png')


class Life(UI):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 66, 42
        self.frame = 0
        self.frame_amount = 1

        if Life.spr == None:
            Life.spr = load_image('./res/image/HUD_life.png')