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
FRAMES_PER_ACTION = 5

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
        cx, cy = self.x - server.map.window_left, self.y - server.map.window_bottom
        self.spr.clip_draw(int(self.frame) * self.spr_w, 0, self.spr_w, self.spr_h, cx, cy)

        if server.IsDebugging:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.spr_w/2, self.y - self.spr_h/2, \
               self.x + self.spr_w/2, self.y + self.spr_h/2

class Arrow(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 24, 27
        self.frame = 0
        self.frame_amount = 2
        if Arrow.spr == None:
            Arrow.spr = load_image('./res/image/arrow.png')

    def draw(self):
        self.spr.clip_draw(self.frame * 24, 0, 24, 27, self.x, self.y)


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

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

        if collision.collide(server.mario, self):
            if server.mario.mario_mode == 'WhiteMario' or server.mario.mario_mode == 'Mario':
                mushroom = Super_Mushroom(self.x, self.y)
                game_world.add_object(mushroom, 1)  # first layer
                server.mushrooms.append(mushroom)

            else:
                coin_effect = Coin_Effect(self.x, self.y)
                game_world.add_object(coin_effect, 1)
                server.coin_effects.append(coin_effect)
                server.mario.coin_num += 1

            brick = EmptyBrick(self.x, self.y)
            game_world.add_object(brick, 1)  # first layer
            server.empty_bricks.append(brick)

            game_world.remove_object(self)


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
            if server.mario.mario_mode == 'Mario':
                print("collision")
                server.mario.mario_mode = "WhiteMario"
            elif server.mario.mario_mode == 'SuperMario':
                server.mario.mario_mode = "WhiteSuperMario"
            game_world.remove_object(self)



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
        self.spr_w, self.spr_h = 48, 48
        # self.spr = load_image('./res/image/super mushroom.png')
        self.frame = 0
        self.frame_amount = 1
        self.IsActivated = False
        self.rising_speed = RUN_SPEED_PPS / 13.0
        self.speed = RUN_SPEED_PPS
        self.origin_x, self.origin_y = self.x, self.y

        if Super_Mushroom.spr == None:
            Super_Mushroom.spr = load_image('./res/image/super mushroom.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

        cx, cy = self.x - server.map.window_left, self.y - server.map.window_bottom
        if cx < 0 or cy > 1280:
            game_world.remove_object(self)

        if self.y <= self.origin_y + 48:
            self.y += self.rising_speed * game_framework.frame_time
        else:
            if self.x <= self.origin_x + 48:
                self.x += self.rising_speed * game_framework.frame_time

        if self.x >= self.origin_x + 48 and self.y > 95 + 24:
            self.IsActivated = True
            self.y -= self.speed * game_framework.frame_time
            self.y = clamp(95 + 24, self.y, self.origin_y + 48)

        if self.y == 95 + 24:
            self.x += self.speed * game_framework.frame_time

        # mario - mushroom collision
        if collision.collide(server.mario, self) and self.IsActivated:
            if server.mario.mario_mode == 'Mario':
                server.mario.power_sound.play()
                server.mario.mario_mode = "SuperMario"
            elif server.mario.mario_mode == 'WhiteMario':
                server.mario.power_sound.play()
                server.mario.mario_mode = "WhiteSuperMario"
            game_world.remove_object(self)


class Coin_Effect(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 40, 32
        # self.spr = load_image('./res/image/coin effect.png')
        self.frame = 0
        self.frame_amount = 5
        if Coin_Effect.spr == None:
            Coin_Effect.spr = load_image('./res/image/coin effect.png')

    def update(self):
        # self.frame = (self.frame + 1) % self.frame_amount
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount
        if int(self.frame) == 4:
            game_world.remove_object(self)





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

        cx, cy = self.x - server.map.window_left, self.y - server.map.window_bottom
        if cx < 0 or cy > 1280:
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
        self.IsActivated = False
        if Brick.spr == None:
            Brick.spr = load_image('./res/image/brick.png')

    def update(self):
        # mario - block collision
        if collision.collide(server.mario, self):
            print("mario - block collision")
            coin_effect = Coin_Effect(self.x, self.y)
            game_world.add_object(coin_effect, 1)
            server.coin_effects.append(coin_effect)
            server.mario.coin_num += 1

            game_world.remove_object(self)


class EmptyBrick(Object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 48, 48
        self.frame = 0
        self.frame_amount = 1
        if EmptyBrick.spr == None:
            EmptyBrick.spr = load_image('./res/image/empty_brick.png')







