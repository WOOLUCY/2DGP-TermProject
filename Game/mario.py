from pico2d import *

import game_framework
from object import FireBall
import game_world
import time
import test_state
import server
import collision

history = []

# Mario Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 7.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Mario Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Mario Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, \
SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, SPACE, DOWN_DOWN, DOWN_UP, ZERO_DOWN, ZERO_UP = range(14)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SLEEP_TIMER', 'SHIFT_DOWN', 'SHIFT_UP',
              'DASH_TIMER', 'DEBUG_KEY', 'SPACE', 'DOWN_DOWN', 'DOWN_UP', 'ZERO_DOWN', 'ZERO_UP']

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): DEBUG_KEY,

    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,

    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYDOWN, SDLK_KP_0): ZERO_DOWN,
    # (SDL_KEYUP, SDLK_KP_0): ZERO_UP
}


# Mario States
class DashState:

    def enter(mario, event):
        print('ENTER DASH')
        mario.dir = clamp(-1, mario.velocity, 1)
        mario.dash_timer = 1000

    def exit(mario, event):
        if event == SPACE:
            if mario.mario_mode == 'WhiteSuperMario' or mario.mario_mode == 'WhiteMario':
                mario.fire_ball()
        print('EXIT DASH')

        mario.prev_state = mario.cur_state
        pass

    def do(mario):
        if mario.mario_mode == ('SuperMario' or 'WhiteSuperMario'):
            mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        else:
            mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        mario.dash_timer -= 1
        mario.x += mario.velocity * game_framework.frame_time * 2
        # mario.x = clamp(25, mario.x, 1280 - 25)
        if mario.dash_timer == 0:
            mario.add_event(DASH_TIMER)
            pass


    def draw(mario):
        cx, cy = mario.x - server.map.window_left, mario.y - server.map.window_bottom

        # mario.font2.draw(cx - 40, cy + 60, '%d    %d' % (mario.x, mario.y), (0, 0, 0))
        if mario.dir == 1:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(int(mario.frame) * 128, 13 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(int(mario.frame) * 128, 13 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(int(mario.frame) * 128, 8 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(int(mario.frame) * 128, 8 * 128, 128, 128, cx, cy)
        else:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(int(mario.frame) * 128, 14 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(int(mario.frame) * 128, 14 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(int(mario.frame) * 128, 9 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(int(mario.frame) * 128, 9 * 128, 128, 128, cx, cy)

class IdleState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS
        mario.timer = 1000

    def exit(mario, event):
        if event == SPACE:
            if mario.mario_mode == 'WhiteSuperMario' or mario.mario_mode == 'WhiteMario':
                mario.fire_ball()

        mario.prev_state = mario.cur_state
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        mario.timer -= 1
        if mario.timer == 0:
            mario.add_event(SLEEP_TIMER)

    def draw(mario):
        cx, cy = mario.x - server.map.window_left, mario.y - server.map.window_bottom

        # mario.font2.draw(cx - 40, cy + 60, '%d    %d' % (mario.x, mario.y), (0, 0, 0))

        if mario.dir == 1:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(0 * 128, 3 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(5 * 128, 3 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(0 * 128, 10 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(0 * 128, 10 * 128, 128, 128, cx, cy)
        else:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(0, 4 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(0, 4 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(0 * 128, 11 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(0 * 128, 11 * 128, 128, 128, cx, cy)


class RunState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS
        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):
        if event == SPACE:
            if mario.mario_mode == 'WhiteSuperMario' or mario.mario_mode == 'WhiteMario':
                mario.fire_ball()

        mario.prev_state = mario.cur_state
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        mario.timer -= 1
        mario.x += mario.velocity * game_framework.frame_time
        # mario.x = clamp(25, mario.x, 1280 - 25)

    # @staticmethod
    def draw(mario):
        cx, cy = mario.x - server.map.window_left, mario.y - server.map.window_bottom
        # cx, cy = server.map.canvas_width // 2, 95 + 64 #server.map.canvas_height//2
        # mario.font2.draw(cx - 40, cy + 60, '%d    %d' % (mario.x, mario.y), (0, 0, 0))

        if mario.dir == 1:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(int(mario.frame) * 128, 11 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(int(mario.frame) * 128, 11 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(int(mario.frame) * 128, 10 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(int(mario.frame) * 128, 10 * 128, 128, 128, cx, cy)
        else:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(int(mario.frame) * 128, 12 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(int(mario.frame) * 128, 12 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(int(mario.frame) * 128, 11 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(int(mario.frame) * 128, 11 * 128, 128, 128, cx, cy)

class SleepState:

    def enter(mario, event):
        mario.frame = 0

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 1

    def draw(mario):
        cx, cy = mario.x - server.map.window_left, mario.y - server.map.window_bottom
        # mario.font2.draw(cx - 40, cy + 60, '%d    %d' % (mario.x, mario.y), (0, 0, 0))

        if mario.dir == 1:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_composite_draw(mario.frame * 128, 3 * 128, 128, 128, 3.141592 / 2, '', cx - 25, cy - 40, 128, 128)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_composite_draw(5 * 128, 3 * 128, 128, 128, 3.141592 / 2, '', cx - 25, cy - 40, 128, 128)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_composite_draw(0 * 128, 10 * 128, 128, 128, 3.141592 / 2, '', cx - 25, cy - 40, 128, 128)
            else:
                mario.white_image.clip_composite_draw(0 * 128, 10 * 128, 128, 128, 3.141592 / 2, '', cx - 25, cy - 40, 128, 128)
        else:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_composite_draw(mario.frame * 128, 4 * 128, 128, 128, -3.141592 / 2, '', cx + 25, cy - 40, 128, 128)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_composite_draw(mario.frame * 128, 4 * 128, 128, 128, -3.141592 / 2, '', cx + 25, cy - 40, 128, 128)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_composite_draw(0 * 128, 11 * 128, 128, 128, -3.141592 / 2, '', cx + 25, cy - 40, 128, 128)
            else:
                mario.white_image.clip_composite_draw(0 * 128, 11 * 128, 128, 128, -3.141592 / 2, '', cx + 25, cy - 40, 128, 128)

class DuckState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1

    def draw(mario):
        cx, cy = mario.x - server.map.window_left, mario.y - server.map.window_bottom

        # mario.font2.draw(cx - 40, cy + 60, '%d    %d' % (mario.x, mario.y), (0, 0, 0))

        if mario.dir == 1:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(1 * 128, 3 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(4 * 128, 3 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(0 * 128, 10 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(0 * 128, 10 * 128, 128, 128, cx, cy)

        else:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(1 * 128, 4 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(1 * 128, 4 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(0 * 128, 11 * 128, 128, 128, cx, cy)
            else:
                mario.white_image.clip_draw(0 * 128, 11 * 128, 128, 128, cx, cy)



class JumpState:
    def enter(mario, event):
        mario.jump_sound.play()
        if mario.dir > 0:
            mario.prev_x, mario.prev_y = mario.x, mario.y
            mario.jumping_x, mario.jumping_y = mario.x + 80, mario.y + 150
            mario.landing_x, mario.landing_y = mario.x + 160, mario.y
        elif mario.dir < 0:
            mario.prev_x, mario.prev_y = mario.x, mario.y
            mario.jumping_x, mario.jumping_y = mario.x - 80, mario.y + 150
            mario.landing_x, mario.landing_y = mario.x - 160, mario.y
        else:
            mario.prev_x, mario.prev_y = mario.x, mario.y
            mario.jumping_x, mario.jumping_y = mario.x, mario.y + 150
            mario.landing_x, mario.landing_y = mario.x, mario.y

    def exit(mario, event):
        pass

    def do(mario):
        mario.x = (2 * mario.t ** 2 - 3 * mario.t + 1) * mario.prev_x + (-4 * mario.t ** 2 + 4 * mario.t) * mario.jumping_x + (
                    2 * mario.t ** 2 - mario.t) * mario.landing_x
        mario.y = (2 * mario.t ** 2 - 3 * mario.t + 1) * mario.prev_y + (-4 * mario.t ** 2 + 4 * mario.t) * mario.jumping_y + (
                    2 * mario.t ** 2 - mario.t) * mario.landing_y


        if mario.t <= 1:
            mario.t += 0.01

            if int(mario.t) == 1:
                mario.cur_state = mario.prev_state
                mario.y = 95 + 64
                mario.t = 0.0

    def draw(mario):
        cx, cy = mario.x - server.map.window_left, mario.y - server.map.window_bottom
        # mario.font2.draw(cx - 40, cy + 60, '%d    %d' % (mario.x, mario.y), (0, 0, 0))

        if mario.dir == 1:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(3 * 128, 3 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(2 * 128, 3 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteMario':
                mario.white_image.clip_draw(1 * 128, 2 * 128, 128, 128, cx, cy + 32)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(1 * 128, 2 * 128, 128, 128, cx, cy + 32)
        else:
            if mario.mario_mode == 'SuperMario':
                mario.super_image.clip_draw(3 * 128, 4 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteSuperMario':
                mario.white_super_image.clip_draw(3 * 128, 4 * 128, 128, 128, cx, cy)
            elif mario.mario_mode == 'WhiteMario':
                mario.white_image.clip_draw(1 * 128, 3 * 128, 128, 128, cx, cy + 32)
            elif mario.mario_mode == 'Mario':
                mario.mario_image.clip_draw(1 * 128, 3 * 128, 128, 128, cx, cy + 32)

next_state_table = {
    DashState: {SHIFT_UP: RunState, DASH_TIMER: RunState,
                LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, RIGHT_DOWN: IdleState, SPACE: DashState,
                DOWN_DOWN: DuckState, ZERO_DOWN: JumpState},
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState,
                SHIFT_UP: IdleState, SHIFT_DOWN: IdleState, SPACE: IdleState, DOWN_DOWN: DuckState, ZERO_DOWN: JumpState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState, SPACE: RunState, DOWN_DOWN: DuckState, ZERO_DOWN: JumpState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState, ZERO_DOWN: IdleState},
    DuckState: {RIGHT_UP: DuckState, LEFT_UP: DuckState, RIGHT_DOWN: DuckState, LEFT_DOWN: DuckState,
                SHIFT_UP: DuckState, SHIFT_DOWN: DuckState, DOWN_UP: IdleState, SPACE: DuckState},
    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState,
                SHIFT_UP: JumpState, SHIFT_DOWN: JumpState, DOWN_UP: IdleState, SPACE: JumpState, ZERO_DOWN: ZERO_DOWN}

}


class Mario:
    def __init__(self):
        self.x, self.y = server.map.canvas_width // 2, 95 + 64  # initial place
        self.mario_mode = 'Mario'
        self.mario_image = load_image('./res/image/Mario2.png') # mario
        self.super_image = load_image('./res/image/Super Mario2.png')   # super mario
        self.white_image = load_image('./res/image/white mario2.png')   # white mario
        self.white_super_image = load_image('./res/image/white mario.png')  # white super mario

        # if self.mario_mode == 'SuperMario':
        #     self.image = load_image('./res/image/Super Mario2.png')
        # elif self.mario_mode == 'WhiteSuperMario':
        #     self.image = load_image('./res/image/white mario.png')
        # elif self.mario_mode == 'Mario':
        #     self.image = load_image('./res/image/Mario2.png')
        # elif self.mario_mode == 'WhiteMario':
        #     self.image = load_image('./res/image/white mario2.png')

        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.prev_state = self.cur_state
        self.cur_state.enter(self, None)
        self.font1 = load_font('./res/font/SuperMarioBros3.ttf', 25)
        self.font2 = load_font('./res/font/SuperMarioBros3.ttf', 16)
        self.IsJumping = False
        self.prev_x, self.prev_y = 0, 0
        self.jumping_x, self.jumping_y = 0, 0
        self.landing_x, self.landing_y = 0, 0
        self.t = 0.0
        self.coin_num = 0
        self.life = 1
        self.IsDebugging = False

        # Mario Sound
        self.jump_sound = load_wav('./res/sound/jump.mp3')
        self.jump_sound.set_volume(20)

        self.coin_sound = load_wav('./res/sound/coin.mp3')
        self.coin_sound.set_volume(64)

        self.fire_sound = load_wav('./res/sound/fireball.wav')
        self.fire_sound.set_volume(64)

        self.power_sound = load_wav('./res/sound/powerup.wav')
        self.power_sound.set_volume(64)

        self.over_sound = load_wav('./res/sound/over.mp3')
        self.over_sound.set_volume(64)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.life = clamp(0, self.life, 5)
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                history.append((self.cur_state.__name__, event_name[event]))
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('cur state: ', self.cur_state.__name__, 'event ', event_name[event])
                exit(-1)

            self.cur_state.enter(self, event)

        # mario - coin collision
        for coin in server.coins.copy():
            if collision.collide(self, coin):
                print("mario-coin COLLISION")
                self.coin_num += 1
                game_world.remove_object(coin)
                server.coins.remove(coin)
                self.coin_sound.play()

        self.x = clamp(0, self.x, server.map.w - 1)
        self.y = clamp(0, self.y, server.map.h - 1)

        if not self.y == 95 + 64:
            self.IsJumping = True
        else:
            self.IsJumping = False

        # print(self.IsJumping)

    def draw(self):
        self.cur_state.draw(self)
        if server.IsDebugging:
            debug_print('Velocity :' + str(int(self.velocity)) + '  Dir:' + str(self.dir) +
                        '    State:' + self.cur_state.__name__ + '      ' + self.mario_mode + '    ' +
                        str(int(self.x)) + ' ' + str(int(self.y)) + ' ' + str(self.t))
            draw_rectangle(*self.get_bb())
        # self.font2.draw(1195, 650, '%d' % (400 - get_time()), (0, 0, 0))
        self.font1.draw(1183, 650, '%d' % (100 - get_time()), (255, 255, 255))
        self.font1.draw(888, 650, '%d' % self.coin_num, (255, 255, 255))
        self.font1.draw(85, 670, '%d' % self.life, (255, 255, 255))


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]

            # debug mode
            if (DEBUG_KEY == key_event):
                print(history[-4:])
                if server.IsDebugging: server.IsDebugging = False
                else: server.IsDebugging = True
            else:
                self.add_event(key_event)

    def fire_ball(self):
        self.fire_sound.play()
        print('FIRE BALL')
        if self.mario_mode == 'WhiteMario':
            fire_ball = FireBall(self.x, self.y - 20, self.dir)
        else:
            fire_ball = FireBall(self.x, self.y, self.dir)
        game_world.add_object(fire_ball, 1)  # first layer
        server.fireballs.append(fire_ball)


    def get_bb(self):
        left, bottom, right, top = 0, 0, 0, 0
        if self.cur_state.__name__ == 'RunState':
            left, bottom, right, top = self.x - 32, self.y - 64, self.x + 32, self.y + 44
        elif self.cur_state.__name__ == 'IdleState' and self.dir == -1:
            left, bottom, right, top = self.x - 32, self.y - 64, self.x + 24, self.y + 44
        elif self.cur_state.__name__ == 'IdleState' and self.dir == 1:
            left, bottom, right, top = self.x - 24, self.y - 64, self.x + 32, self.y + 44
        elif self.cur_state.__name__ == 'DashState' and self.dir == -1:
            left, bottom, right, top = self.x - 32, self.y - 64, self.x + 46, self.y + 44
        elif self.cur_state.__name__ == 'DashState' and self.dir == 1:
            left, bottom, right, top = self.x - 44, self.y - 64, self.x + 32, self.y + 44
        elif self.cur_state.__name__ == 'DuckState' and self.dir == -1:
            left, bottom, right, top = self.x - 36, self.y - 64, self.x + 24, self.y + 12
        elif self.cur_state.__name__ == 'DuckState' and self.dir == 1:
            left, bottom, right, top = self.x - 24, self.y - 64, self.x + 36, self.y + 12
        elif self.cur_state.__name__ == 'JumpState':
            left, bottom, right, top = self.x - 32, self.y - 64, self.x + 32, self.y + 44

        # SleepState fill here
        return left, bottom, right, top

