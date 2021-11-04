from pico2d import *

# Mario Event
# key mapping with dictionary
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DOWN_DOWN, DOWN_UP = range(10) # 0, 1, 2, 3

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
}


# Mario States
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
        mario.timer = 100

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = 0
        mario.timer -= 1
        if mario.timer == 0:
            mario.add_event(SLEEP_TIMER)

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(0 * 128, 3 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(0 * 128, 4 * 128, 128, 128, mario.x, mario.y)

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
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 2
        mario.timer -= 1
        mario.x += mario.velocity * 10
        mario.x = clamp(0 + 32, mario.x, 1280 - 32)

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
        mario.frame = 0

    def draw(mario):
        delay(0.1)
        if mario.dir == 1:
            mario.image.clip_composite_draw(0 * 128, 3 * 128, 128, 128,
                                          3.141592 / 2, '', mario.x - 25, mario.y - 25, 128, 128)
        else:
            mario.image.clip_composite_draw(0 * 128, 4 * 128, 128, 128,
                                          -3.141592 / 2,'', mario.x + 25, mario.y - 25, 128, 128)


class DashState:

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
        mario.timer = 100

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 3
        mario.timer -= 1
        if mario.timer == 0:
            mario.add_event(DASH_TIMER)
        mario.x += mario.velocity * 20
        mario.x = clamp(0 + 32, mario.x, 1280 - 32)

    def draw(mario):
        if mario.velocity == 1:
            mario.image.clip_draw(mario.frame * 128, 13 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(mario.frame * 128, 14 * 128, 128, 128, mario.x, mario.y)


class DuckState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1

    def exit(mario, event):
        pass

    def do(mario):
        pass

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(1 * 128, 3 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(1 * 128, 4 * 128, 128, 128, mario.x, mario.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SHIFT_DOWN: IdleState, SHIFT_UP: IdleState,
                DOWN_DOWN: DuckState,
                SLEEP_TIMER: SleepState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState,
               DOWN_DOWN: DuckState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                 LEFT_UP: RunState, RIGHT_UP: RunState,
                 SHIFT_DOWN: IdleState, SHIFT_UP: IdleState},
    DashState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
                SHIFT_UP: RunState, SHIFT_DOWN: RunState,
                DOWN_DOWN: DuckState,
                DASH_TIMER: RunState},
    DuckState: {DOWN_UP: IdleState,
                RIGHT_UP: DuckState, LEFT_UP: DuckState,
                RIGHT_DOWN: DuckState, LEFT_DOWN: DuckState,
                SHIFT_UP: DuckState, SHIFT_DOWN: DuckState,
                }
}



class Mario:

    def __init__(self):
        self.x, self.y = 1280 // 2, 120
        self.image = load_image('./res/image/Super Mario2.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        pass


    def change_state(self, state):
        # fill here
        pass


    def add_event(self, event):
        self.event_que.insert(0, event)
        pass


    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        pass


    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity: ' + str(self.velocity) + '   Dir: ' + str(self.dir))
        pass


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass

