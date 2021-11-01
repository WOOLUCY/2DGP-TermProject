from pico2d import *

# Mario Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
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
        mario.timer = 1000

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 1
        mario.timer -= 1

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
        mario.x = clamp(25, mario.x, 800 - 25)

    def draw(mario):
        if mario.velocity == 1:
            mario.image.clip_draw(mario.frame * 128, 11 * 128, 128, 128, mario.x, mario.y)
        else:
            mario.image.clip_draw(mario.frame * 128, 12 * 128, 128, 128, mario.x, mario.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState},
}


class Super_Mario:

    def __init__(self):
        self.x, self.y = 70, 120
        self.image = load_image('./res/image/Super Mario2.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        pass


    def change_state(self,  state):
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
        pass


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass

