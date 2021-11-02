import game_framework
from pico2d import *
import main_state


name = "TitleState"
image = None
press_button = None



class Press_Button:
    def __init__(self):
        self.x, self.y = 1284 / 2, 200
        self.image = load_image('./res/image/press.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 2
        delay(0.1)

    def draw(self):
        self.image.clip_draw(0, self.frame * 45, 560, 45, self.x, self.y)


def enter():
    global image, press_button
    image = load_image('./res/image/title.png')
    press_button = Press_Button()


def exit():
    global image, press_button
    del image
    del press_button


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    image.draw(642, 390)
    press_button.draw()
    update_canvas()


def update():
    press_button.update()


def pause():
    pass


def resume():
    pass






