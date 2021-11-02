import game_framework
from pico2d import *
import title_state


name = "StartState"
image = None
image2 = None
image3 = None

logo_time = 0.0
frame = 0


def enter():
    global image
    global image2
    global image3

    image = load_image('./res/image/kpu_logo.png')
    image2 = load_image('./res/image/veil1.png')
    image3 = load_image('./res/image/veil2.png')



def exit():
    global image
    global image2
    global image3

    del image
    del image2
    del image3

def update():
    global logo_time
    global frame

    frame += 1

    if (logo_time > 0.5):
        logo_time = 0
        # game_framework.quit()
        game_framework.change_state(title_state)
    delay(0.02)
    logo_time += 0.01




def draw():
    global image
    global image2
    global image3
    global frame

    clear_canvas()
    image.draw(642, 390)
    if frame < 20:
        if frame < 10:
            image2.clip_draw(0, (9 - frame) * 780, 1284, 780, 1284 / 2, 780 / 2)
        else:
            image3.clip_draw(0, (19 - frame) * 780, 1284, 780, 1284 / 2, 780 / 2)
            print(frame)
    else:
        pass
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()


def pause(): pass


def resume(): pass




