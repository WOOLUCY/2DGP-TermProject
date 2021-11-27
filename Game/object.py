from pico2d import *
import game_world
import game_framework
import time
import server
import collision

# Object Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Object Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Object:
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

class Arrow(Object):
    def __init__(self):
        self.x, self.y = 460, 370
        self.spr_w, self.spr_h = 24, 27
        self.frame = 0
        self.frame_amount = 2
        self.OnExit = False
        if Arrow.spr == None:
            Arrow.spr = load_image('./res/image/arrow.png')

    def draw(self):
        if not self.OnExit:
            self.spr.clip_draw(self.frame * 24, 0, 24, 27, self.x, self.y)
        else:
            self.spr.clip_draw(self.frame * 24, 0, 24, 27, self.x, self.y - 60)


class Coin(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        # self.spr = load_image('./res/image/coin.png')
        self.spr_w = 45
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 4
        if Coin.spr == None:
            Coin.spr = load_image('./res/image/coin.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

class Block(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        # self.spr = load_image('./res/image/block.png')
        self.spr_w = 48
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 3
        if Block.spr == None:
            Block.spr = load_image('./res/image/block.png')


class Flower(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        # self.spr = load_image('./res/image/flower.png')
        self.spr_w = 48
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 4
        if Flower.spr == None:
            Flower.spr = load_image('./res/image/flower.png')


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

        # mario - flower collision
        if collision.collide(server.mario, self):
            # print("mario-flower COLLISION")
            server.mario.mario_mode = "WhiteSuperMario"
            game_world.remove_object(server.flower)


class Star(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        # self.spr = load_image('./res/image/star.png')
        self.spr_w = 48
        self.spr_h = 48
        self.frame = 0
        self.frame_amount = 4
        if Star.spr == None:
            Star.spr = load_image('./res/image/star.png')


class Super_Mushroom(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 64, 64
        # self.spr = load_image('./res/image/super mushroom.png')
        self.frame = 0
        self.frame_amount = 1
        if Super_Mushroom.spr == None:
            Super_Mushroom.spr = load_image('./res/image/super mushroom.png')


class Coin_Effect(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 40, 32
        # self.spr = load_image('./res/image/coin effect.png')
        self.frame = 0
        self.frame_amount = 5
        if Coin_Effect.spr == None:
            Coin_Effect.spr = load_image('./res/image/coin effect.png')


class FireBall(Object):
    def __init__(self, x = 400, y = 300, velocity = 10):
        self.spr_w, self.spr_h = 32, 52
        self.frame = 0
        self.frame_amount = 4

        if FireBall.spr == None:
            FireBall.spr = load_image('./res/image/fireball.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.velocity *= RUN_SPEED_PPS

    def update(self):
        self.x += self.velocity * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)


    def get_bb(self):
        return self.x - self.spr_w/2, self.y - self.spr_h/2, \
               self.x + self.spr_w/2, self.y + 14

class Brick(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 48, 48
        self.frame = 0
        self.frame_amount = 1
        if Brick.spr == None:
            Brick.spr = load_image('./res/image/brick.png')






