from pico2d import *

import game_framework
from object import FireBall
import game_world
import time

history = []

# Mario Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 6.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Mario Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Mario Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, \
SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, SPACE, DOWN_DOWN, DOWN_UP = range(12)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SLEEP_TIMER', 'SHIFT_DOWN', 'SHIFT_UP',
              'DASH_TIMER', 'DEBUG_KEY', 'SPACE', 'DOWN_DOWN', 'DOWN_UP']

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
}


# Mario States
class DashState:

    def enter(mario, event):
        print('ENTER DASH')
        mario.dir = clamp(-1, mario.velocity, 1)
        mario.dash_timer = 100

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        print('EXIT DASH')
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        mario.dash_timer -= 1
        mario.x += mario.velocity * game_framework.frame_time * 2
        mario.x = clamp(25, mario.x, 1280 - 25)
        if mario.dash_timer == 0:
            mario.add_event(DASH_TIMER)


    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 128, 13 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame) * 128, 14 * 128, 128, 128, mario.x, mario.y)

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
            mario.fire_ball()
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        mario.timer -= 1
        if mario.timer == 0:
            mario.add_event(SLEEP_TIMER)

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 128, 3 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame) * 128, 4 * 128, 128, 128, mario.x, mario.y)


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
            mario.fire_ball()
        pass

    def do(mario):
        mario.frame =  (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        mario.timer -= 1
        mario.x += mario.velocity * game_framework.frame_time
        mario.x = clamp(25, mario.x, 1280 - 25)

    @staticmethod
    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 128, 11 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame) * 128, 12 * 128, 128, 128, mario.x, mario.y)


class SleepState:

    def enter(mario, event):
        mario.frame = 0

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 1

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_composite_draw(mario.frame * 128, 3 * 128, 128, 128, 3.141592 / 2, '', mario.x - 25, mario.y - 25, 128, 128)
        else:
            mario.image.clip_composite_draw(mario.frame * 128, 4 * 128, 128, 128, -3.141592 / 2, '', mario.x + 25, mario.y - 25, 128, 128)


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
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame + 1) * 128, 3 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame + 1) * 128, 4 * 128, 128, 128, mario.x, mario.y)

next_state_table = {
    DashState: {SHIFT_UP: RunState, DASH_TIMER: RunState,
                LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, RIGHT_DOWN: IdleState, SPACE: DashState,
                DOWN_DOWN: DuckState},
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState,
                SHIFT_UP: IdleState, SHIFT_DOWN: IdleState, SPACE: IdleState, DOWN_DOWN: DuckState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState, SPACE: RunState, DOWN_DOWN: DuckState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState},
    DuckState: {RIGHT_UP: DuckState, LEFT_UP: DuckState, RIGHT_DOWN: DuckState, LEFT_DOWN: DuckState,
                SHIFT_UP: DuckState, SHIFT_DOWN: DuckState, DOWN_UP: IdleState, SPACE: DuckState},
}


class Mario:

    def __init__(self):
        self.x, self.y = 1280 // 2, 120
        self.image = load_image('./res/image/Super Mario2.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.font1 = load_font('./res/font/SuperMario.TTF', 48)
        self.font2 = load_font('./res/font/SuperMario.TTF', 55)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
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

    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir) + '    State:' + self.cur_state.__name__)
        # self.font2.draw(1195, 650, '%d' % (400 - get_time()), (0, 0, 0))
        self.font1.draw(1185, 680, 'TIME', (255, 198, 41))
        self.font1.draw(1195, 640, '%d' % (400 - get_time()), (255, 198, 41))


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if (DEBUG_KEY == key_event):
                print(history[-4:])
            else:
                self.add_event(key_event)

    def fire_ball(self):
        print('FIRE BALL')
        fire_ball = FireBall(self.x, self.y, self.dir)
        game_world.add_object(fire_ball, 1)  # first layer

