from pico2d import *
import game_framework

# Monster Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 7.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Monster Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

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
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.spr_w/2, self.y - self.spr_h/2, \
               self.x + self.spr_w/2, self.y + self.spr_h/2

class Goomba(Monster):
    def __init__(self, x, y, velocity = 0):
        self.x, self.y, self.velocity = x, y, velocity
        # self.spr = load_image('./res/image/Goomba.png')
        self.spr_w, self.spr_h = 64, 64
        self.frame = 0
        self.frame_amount = 2
        if Goomba.spr == None:
            Goomba.spr = load_image('./res/image/Goomba.png')
        self.velocity += RUN_SPEED_PPS
        self.dir = 1
        self.font = load_font('./res/font/ENCR10B.TTF', 16)


class Koopa_Troopa(Monster):
    def __init__(self, x, y, velocity = 0):
        self.x, self.y, self.velocity = x, y, velocity
        # self.spr = load_image('./res/image/Goomba.png')
        self.spr_w, self.spr_h = 48, 64
        self.frame = 0
        self.frame_amount = 2
        if Koopa_Troopa.spr == None:
            Koopa_Troopa.spr = load_image('./res/image/Koopa Troopa.png')
        self.velocity += RUN_SPEED_PPS
        self.dir = 1
        self.font = load_font('./res/font/ENCR10B.TTF', 16)

    def update(self):
        if clamp(800, self.x, 1200) == 1200:
            self.velocity -= RUN_SPEED_PPS
        elif clamp(800, self.x, 1200) == 800:
            self.velocity += RUN_SPEED_PPS
        self.dir = clamp(-1, self.velocity, 1)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount
        self.x += self.velocity * game_framework.frame_time

    def draw(self):
        if self.dir == -1:
            self.spr.clip_draw(int(self.frame) * self.spr_w, 64, self.spr_w, self.spr_h, self.x, self.y)
        else:
            self.spr.clip_composite_draw(int(self.frame) * self.spr_w, 64,self.spr_w, self.spr_h, 0, 'h', self.x, self.y,self.spr_w, self.spr_h)
        # debug_print('Velocity :' + str(self.velocity) + '   Dir :' + str(self.dir))
        self.font.draw(self.x - 32, self.y + 50, 'Dir :' + str(self.dir), (255, 0, 255))
        draw_rectangle(*self.get_bb())

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
