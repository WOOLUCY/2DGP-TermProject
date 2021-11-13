from pico2d import *
from object import FireBall
import game_world
import time

history = []

# Mario Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, \
SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, SPACE = range(10)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SLEEP_TIMER', 'SHIFT_DOWN', 'SHIFT_UP', 'DASH_TIMER', 'DEBUG_KEY', 'SPACE']

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
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Mario States
class DashState:

    def enter(mario, event):
        print('ENTER DASH')
        mario.dir = mario.velocity
        mario.dash_timer = 100

    def exit(mario, event):
        print('EXIT DASH')
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 3
        mario.dash_timer -= 1
        mario.x += mario.velocity * 5
        mario.x = clamp(25, mario.x, 1280 - 25)
        if mario.dash_timer == 0:
            mario.add_event(DASH_TIMER)

    def draw(mario):
        if mario.velocity == 1:
            mario.image.clip_draw(mario.frame * 128, 13 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(mario.frame * 128, 14 * 128, 128, 128, mario.x, mario.y)

class IdleState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1
        mario.timer = 1000

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 1
        mario.timer -= 1
        if mario.timer == 0:
            mario.add_event(SLEEP_TIMER)

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(mario.frame * 128, 3 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(mario.frame * 128, 4 * 128, 128, 128, mario.x, mario.y)


class RunState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1
        mario.dir = mario.velocity

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 2
        mario.timer -= 1
        mario.x += mario.velocity * 3
        mario.x = clamp(25, mario.x, 1280 - 25)

    def draw(mario):
        if mario.velocity == 1:
            mario.image.clip_draw(mario.frame * 128, 11 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(mario.frame * 128, 12 * 128, 128, 128, mario.x, mario.y)


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


next_state_table = {
    DashState: {SHIFT_UP: RunState, DASH_TIMER: RunState,
                LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, RIGHT_DOWN: IdleState},
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState,
                SHIFT_UP: IdleState, SHIFT_DOWN: IdleState, SPACE: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState, SPACE: RunState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState}
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
        self.font1 = load_font('SuperMario.TTF', 48)
        self.font2 = load_font('SuperMario.TTF', 55)


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
        self.font2.draw(1200, 650 + 2, '%d' % get_time(), (0, 0, 0))
        self.font1.draw(1200, 650, '%d' % get_time(), (255, 198, 41))


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if (DEBUG_KEY == key_event):
                print(history[-4:])
            else:
                self.add_event(key_event)

    def fire_ball(self):
        print('FIRE BALL')
        fire_ball = FireBall(self.x, self.y, self.dir * 3)
        game_world.add_object(fire_ball, 1)  # first layer

