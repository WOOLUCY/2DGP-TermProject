from pico2d import *

import game_framework
import game_world
import pause_state

from mario import *
from background import *
import main_state
from object import *
from random import randint
from monster import *
from UI import *
import server

name = "TestState"


def enter():
    # background
    server.cloud = Cloud()
    game_world.add_object(server.cloud, 0)

    server.hill = Hill()
    game_world.add_object(server.hill, 0)

    server.map = Map()
    game_world.add_object(server.map, 0)


    # object
    server.flower = Flower(850, 88)
    game_world.add_object(server.flower, 1)

    server.coins = [Coin(550, 120), Coin(600, 120), Coin(650, 120), Coin(700, 120),]
    game_world.add_objects(server.coins, 1)

    server.bricks = [Brick(983, 234), Brick(983 + 48 * 2, 234), Brick(983 + 48 * 3, 234), Brick(983 + 48 * 4, 234)]
    game_world.add_objects(server.bricks, 0)

    server.blocks = [Block(792, 234), Block(983 + 48, 234)]
    game_world.add_objects(server.blocks, 0)

    # UI
    server.top = Top(1050, 660)
    game_world.add_object(server.top, 1)

    server.coin_num = CoinNum(835, 648)
    game_world.add_object(server.coin_num, 1)

    server.life = Life(43, 670)
    game_world.add_object(server.life, 1)

    # monster
    server.goomba = Goomba(1100, 65 + 32)
    game_world.add_object(server.goomba, 1)

    # mario
    server.mario = Mario()
    game_world.add_object(server.mario, 1)


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
            server.mario.handle_event(event)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def update():
    for game_object in game_world.all_objects():
        game_object.update()



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True