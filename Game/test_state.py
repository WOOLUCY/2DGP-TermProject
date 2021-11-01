from pico2d import *

import game_framework

from mario import Super_Mario
from background import *
import main_state



name = "TestState"

base = None
cloud = None
hill = None

mario = None

def enter():
    global base, cloud, hill
    global mario

    base = Map()
    cloud = Cloud()
    hill = Hill()

    mario = Super_Mario()


def exit():
    global base, cloud, hill
    global mario

    del base
    del cloud
    del hill

    del mario


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_0):
            game_framework.change_state(main_state)
        else:
            mario.handle_event(event)


def draw():
    clear_canvas()

    cloud.draw()
    hill.draw()
    base.draw()

    mario.draw()

    update_canvas()

    delay(0.05)


def update():
    mario.update()