import game_framework

from object import *
from effect import *
from monster import *
import main_state


name = "TestState"

coin = None
ce = None
block = None
mushroom = None
goomba = None
flower = None
star = None
bowser = None
koopa = None
koopa_shell = None
plant = None

def enter():
    global coin, ce, block, mushroom, flower, star
    global goomba, bowser, koopa, koopa_shell, plant

    coin = Coin()
    ce = Coin_Effect()
    block = Block()
    mushroom = Super_Mushroom()
    goomba = Goomba()
    flower = Flower()
    star = Star()
    bowser = Bowser()
    koopa = Koopa_Troopa()
    koopa_shell = Koopa_Troopa_Shell()
    plant = Piranha_Plant()

def exit():
    global coin, ce, block, mushroom, flower, star
    global goomba, bowser, koopa, koopa_shell, plant

    del(coin)
    del(ce)
    del(block)
    del(mushroom)
    del(flower)
    del(star)
    del(goomba)
    del(bowser)
    del(koopa)
    del(koopa_shell)
    del(plant)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_0):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()

    goomba.draw()
    coin.draw()
    ce.draw()
    block.draw()
    flower.draw()
    star.draw()
    mushroom.draw()
    bowser.draw()
    koopa.draw()
    koopa_shell.draw()
    plant.draw()


    update_canvas()

    delay(0.05)


def update():
    goomba.update()
    coin.update()
    ce.update()
    block.update()
    flower.update()
    star.update()
    mushroom.update()
    bowser.update()
    koopa.update()
    koopa_shell.update()
    plant.update()