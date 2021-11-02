import game_framework
from pico2d import *
from object import *


name = "ObjectState"

coin = None
block = None
flower = None
star = None
mushroom = None
effect = None


def enter():
    global coin, block, flower, star, mushroom, effect
    coin = Coin(100, 100)
    block = Block(200, 100)
    flower = Flower(300, 100)
    star = Star(400, 100)
    mushroom = Super_Mushroom(500, 100)
    effect = Coin_Effect(600, 100)


def exit():
    global coin, block, flower, star, mushroom, effect

    del coin
    del block
    del flower
    del star
    del mushroom
    del effect


def update():
    coin.update()
    block.update()
    flower.update()
    star.update()
    mushroom.update()
    effect.update()


def draw():
    clear_canvas()

    coin.draw()
    block.draw()
    flower.draw()
    star.draw()
    mushroom.draw()
    effect.draw()

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




