from pico2d import *

import game_framework
import title_state

from object import *
from effect import *
from monster import *
from background import *

name = "MainState"

base = None
cloud = None
hill = None

coin = None
ce = None
block = None
mushroom = None
goomba = None
mario = None
flower = None
star = None
bowser = None

MAP_WIDTH = 1284
MAP_HEIGHT = 780

# initialization code
open_canvas(MAP_WIDTH, MAP_HEIGHT)

x, y = MAP_WIDTH // 2, 120
x_dir, y_dir = 0, 0
# prev_x, prev_y = 0, 0
# jumping_x, jumping_y = 0, 0
# landing_x, landing_y = 0, 0

jumping = False
ducking = False

# Game object class here
class Mario:
    global x, y
    global x_dir, y_dir
    global jumping, ducking
    # global prev_x, prev_y, jumping_x, jumping_y, landing_x, landing_y

    def __init__(self):
        self.x, self.y = x, y
        self.t = 0.0
        self.image = load_image('./res/image/white mario.png')
        self.IsJumping = jumping
        self.frame = 0
        self.prev_x, self.prev_y = 0, 0
        self.jumping_x, self.jumping_y = 0, 0
        self.landing_x, self.landing_y = 0, 0
        self.dir = 0

    def update(self):
        global x, y
        global x_dir, y_dir
        if jumping:
            self.IsJumping = True
            if self.dir > 0:
                self.prev_x, self.prev_y = x, y
                self.jumping_x, self.jumping_y = x + 60, y + 200
                self.landing_x, self.landing_y = x + 120, y
            elif self.dir < 0:
                self.prev_x, self.prev_y = x, y
                self.jumping_x, self.jumping_y = x - 60, y + 200
                self.landing_x, self.landing_y = x - 120, y
            else:
                self.prev_x, self.prev_y = x, y
                self.jumping_x, self.jumping_y = x, y + 200
                self.landing_x, self.landing_y = x, y

        if self.IsJumping:
            self.x = (2 * self.t ** 2 - 3 * self.t + 1) * self.prev_x + (-4 * self.t ** 2 + 4 * self.t) * self.jumping_x + (2 * self.t ** 2 - self.t) * self.landing_x
            self.y = (2 * self.t ** 2 - 3 * self.t + 1) * self.prev_y + (-4 * self.t ** 2 + 4 * self.t) * self.jumping_y + (2 * self.t ** 2 - self.t) * self.landing_y
            if self.t >= 1:
                self.IsJumping = False
                self.t = 0
            else:
                self.t += 0.05
        else:
            self.x += x_dir * 7
            self.y += y_dir * 7
            self.frame = (self.frame + 1) % 2
            if x_dir != 0:
                self.dir = x_dir
            x, y = self.x, self.y
        print(x_dir, y_dir)

    def draw(self):
        if not self.IsJumping:
            if not ducking:
                if x_dir > 0:   # walking right
                    self.image.clip_draw(self.frame * 128, 11 * 128, 128, 128, self.x, self.y)
                elif x_dir < 0:     # walking left
                    self.image.clip_draw(self.frame * 128, 12 * 128, 128, 128, self.x, self.y)
                else:   # idle
                    if self.dir < 0:    # left
                        self.image.clip_draw(0 * 128, 4 * 128, 128, 128, self.x, self.y)
                    elif self.dir >= 0:     # right
                        self.image.clip_draw(5 * 128, 3 * 128, 128, 128, self.x, self.y)
            else:
                if self.dir >= 0:  # right
                    self.image.clip_draw(4 * 128, 3 * 128, 128, 128, self.x, self.y)
                elif self.dir < 0:  # left
                    self.image.clip_draw(1 * 128, 4 * 128, 128, 128, self.x, self.y)
        else:       # jumping
            if self.dir >= 0:   # right
                self.image.clip_draw(2 * 128, 3 * 128, 128, 128, self.x, self.y)
            elif self.dir < 0:  # left
                self.image.clip_draw(3 * 128, 4 * 128, 128, 128, self.x, self.y)


class Super_Mario:  # duck
    global x, y
    global x_dir, y_dir
    global jumping

    # global prev_x, prev_y, jumping_x, jumping_y, landing_x, landing_y

    def __init__(self):
        self.x, self.y = x, y
        self.t = 0.0
        self.image = load_image('./res/image/Super Mario2.png')
        self.IsJumping = jumping
        self.frame = 0
        self.prev_x, self.prev_y = 0, 0
        self.jumping_x, self.jumping_y = 0, 0
        self.landing_x, self.landing_y = 0, 0
        self.dir = 0

    def update(self):
        global x, y
        global x_dir, y_dir
        if jumping:
            self.IsJumping = True
            if self.dir > 0:
                self.prev_x, self.prev_y = x, y
                self.jumping_x, self.jumping_y = x + 60, y + 200
                self.landing_x, self.landing_y = x + 120, y
            elif self.dir < 0:
                self.prev_x, self.prev_y = x, y
                self.jumping_x, self.jumping_y = x - 60, y + 200
                self.landing_x, self.landing_y = x - 120, y
            else:
                self.prev_x, self.prev_y = x, y
                self.jumping_x, self.jumping_y = x, y + 200
                self.landing_x, self.landing_y = x, y

        if self.IsJumping:
            self.x = (2 * self.t ** 2 - 3 * self.t + 1) * self.prev_x + (
                        -4 * self.t ** 2 + 4 * self.t) * self.jumping_x + (
                                 2 * self.t ** 2 - self.t) * self.landing_x
            self.y = (2 * self.t ** 2 - 3 * self.t + 1) * self.prev_y + (
                        -4 * self.t ** 2 + 4 * self.t) * self.jumping_y + (
                                 2 * self.t ** 2 - self.t) * self.landing_y
            if self.t >= 1:
                self.IsJumping = False
                self.t = 0
            else:
                self.t += 0.05
        else:
            self.x += x_dir * 7
            self.y += y_dir * 7
            self.frame = (self.frame + 1) % 2
            if x_dir != 0:
                self.dir = x_dir
            x, y = self.x, self.y
        print(x_dir, y_dir)

    def draw(self):
        if not self.IsJumping:
            if x_dir > 0:   # walking right
                self.image.clip_draw(self.frame * 128, 11 * 128, 128, 128, self.x, self.y)
            elif x_dir < 0:     # walking left
                self.image.clip_draw(self.frame * 128, 12 * 128, 128, 128, self.x, self.y)
            else:   # idle
                if self.dir < 0:    # left
                    self.image.clip_draw(0 * 128, 4 * 128, 128, 128, self.x, self.y)
                elif self.dir >= 0:     # right
                    self.image.clip_draw(0 * 128, 3 * 128, 128, 128, self.x, self.y)

        else:       # jumping
            if self.dir >= 0:   # right
                self.image.clip_draw(3 * 128, 3 * 128, 128, 128, self.x, self.y)
            elif self.dir < 0:  # left
                self.image.clip_draw(3 * 128, 4 * 128, 128, 128, self.x, self.y)

def enter():
    global base, cloud, hill
    global coin, ce, block, mushroom, flower, star
    global goomba, bowser
    global mario

    base = Map()
    cloud = Cloud()
    hill = Hill()

    coin = Coin()
    ce = Coin_Effect()
    block = Block()
    mushroom = Super_Mushroom()
    goomba = Goomba()
    # mario = Super_Mario()
    mario = Mario()
    flower = Flower()
    star = Star()
    bowser = Bowser()

def exit():
    global base, cloud, hill
    global coin, ce, block, mushroom, flower, star
    global goomba, bowser
    global mario

    del(base)
    del(cloud)
    del(hill)
    del(coin)
    del(ce)
    del(block)
    del(mushroom)
    del(flower)
    del(star)
    del(goomba)
    del(bowser)
    del(mario)

def pause():
    pass

def resume():
    pass

def handle_events():
    global running
    global x, y
    global x_dir, y_dir
    # global prev_x, prev_y, jumping_x, jumping_y, landing_x, landing_y
    global jumping, ducking

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                x_dir += 1
            elif event.key == SDLK_LEFT:
                x_dir -= 1
            elif event.key == SDLK_DOWN:
                ducking = True
            elif event.key == SDLK_SPACE:
                # x_dir += 1
                # y_dir += 1
                # prev_x, prev_y = x, y
                # jumping_x, jumping_y = x + 40, y + 200
                # landing_x, landing_y = x + 80, y
                jumping = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                x_dir -= 1
            elif event.key == SDLK_LEFT:
                x_dir += 1
            elif event.key == SDLK_DOWN:
                ducking = False
            elif event.key ==SDLK_SPACE:
                jumping = False
                # x_dir = 0
                # y_dir = 0


def update():
    cloud.update()
    goomba.update()
    mario.update()
    coin.update()
    ce.update()
    block.update()
    flower.update()
    star.update()
    mushroom.update()
    bowser.update()

def draw():
    clear_canvas()

    cloud.draw()
    hill.draw()
    base.draw()

    goomba.draw()
    mario.draw()
    coin.draw()
    ce.draw()
    block.draw()
    flower.draw()
    star.draw()
    mushroom.draw()
    bowser.draw()

    update_canvas()

    # delay(0.05)



