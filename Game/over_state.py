import game_framework
from pico2d import *
import main_state
import test_state
from object import Arrow
import server


name = "OverState"
image = None
sound = None
arrow = None
IsOnExit = False

def enter():
    sound = load_wav('./res/sound/over.mp3')
    sound.set_volume(64)
    sound.play()
    server.hill.bgm.stop()
    global image, arrow
    image = load_image('./res/image/over.png')
    arrow = Arrow(438, 342)


def exit():
    global image, arrow
    del image
    del arrow


def handle_events():
    global IsOnExit
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(test_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN) and not IsOnExit:
                arrow.y -= 70
                IsOnExit = True
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP) and IsOnExit:
                arrow.y += 70
                IsOnExit = False
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                if not IsOnExit: game_framework.change_state(test_state)
                else: game_framework.quit()


def draw():
    clear_canvas()
    image.draw(1280//2, 720//2)
    arrow.draw()
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






