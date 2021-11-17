from pico2d import *

import game_framework
import pause_state

from mario import *
from background import *
import main_state
from object import *
from random import randint
from monster import *
from UI import *

name = "TestState"

timer = 0

# background
map = None
cloud = None
hill = None


# object
coins = []
flower = None
bricks = []
blocks = []

# UI
top = None
coin_num = None
life = None

# monster
koopa = None

# character
mario = None


def enter():
    global map, cloud, hill
    global flower, coins, bricks, blocks
    global top, coin_num, life
    global koopa
    global mario

    map = Map()
    cloud = Cloud()
    hill = Hill()

    flower = Flower(400, 88)
    coins = [Coin(300, 120), Coin(350, 120), Coin(400, 120), Coin(450, 120),]
    bricks = [Brick(983, 234), Brick(983 + 48 * 2, 234), Brick(983 + 48 * 3, 234), Brick(983 + 48 * 4, 234)]
    blocks = [Block(792, 234), Block(983 + 48, 234)]

    top = Top(1050, 660)
    coin_num = CoinNum(835, 648)
    life = Life(43, 670)

    koopa = Koopa_Troopa(900, 98)

    mario = Mario()

    # game_world.add_object(cloud, 0)
    # game_world.add_object(hill, 0)
    game_world.add_object(map, 0)
    game_world.add_object(koopa, 1)
    game_world.add_object(mario, 1)
    game_world.add_object(top, 1)
    game_world.add_object(coin_num, 1)
    game_world.add_object(life, 1)
    game_world.add_object(flower, 1)
    game_world.add_objects(coins, 1)
    game_world.add_objects(bricks, 0)
    game_world.add_objects(blocks, 0)



def exit():
    game_world.clear()


def pause(): pass


def resume(): pass


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
    global timer
    timer -= 1
    timer = clamp(0, timer, 1000)
    # print(timer)
    for game_object in game_world.all_objects():
        game_object.update()
    for coin in coins:
        if collide(mario, coin):
            print("mario-coin COLLISION")
            mario.coin_num += 1
            coins.remove(coin)
            game_world.remove_object(coin)

    if collide(mario, koopa) and timer == 0:
        print("mario-koopa COLLISION")
        mario.life -= 1
        timer = 100

    # if collide(mario, flower):
    #     print("mario-flower COLLISTION")
    #     mario.mario_mode = 'WhiteSuperMario'


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True