import game_framework
from pico2d import *
from object import Arrow
import main_state


name = "PauseState"
image = None
arrow = None

IsOnExit = None

MAP_WIDTH = 1280
MAP_HEIGHT = 720

# initialization code
# open_canvas(MAP_WIDTH, MAP_HEIGHT)


def enter():
    global image
    image = load_image('./res/image/paused.png')

    global arrow
    arrow = Arrow(454, 370)



def exit():
    global image, arrow

    del(image)
    del(arrow)


def update():
    pass


def draw():
    # clear_canvas()
    image.draw(1284 // 2, 780 // 2)
    arrow.draw()

    update_canvas()
    pass


def handle_events():
    global IsOnExit
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.pop_state()
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
                if not IsOnExit:
                    IsOnExit = True
                    arrow.y -= 60
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
                if IsOnExit:
                    IsOnExit = False
                    arrow.y += 60
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                if IsOnExit:
                    game_framework.quit()
                else:
                    game_framework.pop_state()



def pause(): pass


def resume(): pass




