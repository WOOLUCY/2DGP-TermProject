import game_framework
from pico2d import *
from background import *
import main_state


name = "StartState"
image2 = None
image3 = None

base = None
cloud = None
hill = None

MAP_WIDTH = 1284
MAP_HEIGHT = 780

# initialization code
open_canvas(MAP_WIDTH, MAP_HEIGHT)


def enter():
    global image2
    global image3

    image2 = load_image('./res/image/veil1.png')
    image3 = load_image('./res/image/veil2.png')

    global base, cloud, hill

    base = Map()
    cloud = Cloud()
    hill = Hill()



def exit():
    global image2
    global image3
    global base, cloud, hill

    del(base)
    del(cloud)
    del(hill)

    del(image2)
    del(image3)


def update():
    pass


def draw():
    clear_canvas()
    cloud.draw()
    hill.draw()
    base.draw()

    image2.clip_draw(0, 6 * 780, 1284, 780, 1284 / 2, 780 / 2)

    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.pop_state()
    pass


def pause(): pass


def resume(): pass




