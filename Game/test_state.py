from pico2d import *

import game_framework

from mario import *
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

    mario = Mario()

    game_world.add_object(cloud, 0)
    game_world.add_object(hill, 0)
    game_world.add_object(base, 0)
    game_world.add_object(mario, 1)

def exit():
    game_world.clear()


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
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def update():
    for game_object in game_world.all_objects():
        game_object.update()