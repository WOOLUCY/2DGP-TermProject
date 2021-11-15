import game_framework
from pico2d import *
from monster import *
from random import randint


name = "MonsterState"

goombas = None
koopa = None
shell = None
plant = None
bowser = None


def enter():
    global goombas, koopa, shell, plant, bowser
    goombas = [Goomba(randint(100, 1200), 100) for i in range(10)]
    koopa = Koopa_Troopa(1200, 200)
    shell = Koopa_Troopa_Shell(100, 300)
    plant = Piranha_Plant(200, 300)
    bowser = Bowser(300, 300)


def exit():
    global goombas, koopa, shell, plant, bowser

    del goombas
    del koopa
    del shell
    del plant
    del bowser


def update():
    for goomba in goombas:
        goomba.update()
    koopa.update()
    shell.update()
    plant.update()
    bowser.update()


def draw():
    clear_canvas()

    for goomba in goombas:
        goomba.draw()
    koopa.draw()
    shell.draw()
    plant.draw()
    bowser.draw()

    update_canvas()

    delay(0.05)
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()


def pause(): pass


def resume(): pass




