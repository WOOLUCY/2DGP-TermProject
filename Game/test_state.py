from pico2d import *

import game_framework
import game_world
import pause_state

from mario import *
from background import *
from back import TileBackground as Background
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

    server.map = Background()
    game_world.add_object(server.map, 0)


    # object
    server.flower = Flower(850, 140)
    game_world.add_object(server.flower, 1)
    #
    server.coins = [Coin(100, 140), Coin(200, 140), Coin(300, 140),Coin(400, 140),]
    game_world.add_objects(server.coins, 1)
    #
    server.bricks = [Brick(983, 350), Brick(983 + 48 * 2, 350), Brick(983 + 48 * 3, 350), Brick(983 + 48 * 4, 350)]
    game_world.add_objects(server.bricks, 0)
    #
    # server.blocks = [Block(792, 234), Block(983 + 48, 234)]
    # game_world.add_objects(server.blocks, 0)

    # Effects

    # UI
    server.top = Top(1050, 660)
    game_world.add_object(server.top, 1)

    server.coin_num = CoinNum(835, 648)
    game_world.add_object(server.coin_num, 1)

    server.life = Life(43, 670)
    game_world.add_object(server.life, 1)

    # monster
    server.goomba = Goomba(500, 95 + 32)
    game_world.add_object(server.goomba, 1)

    # server.koopa = Koopa_Troopa(300, 95 + 32)
    # game_world.add_object(server.koopa, 1)

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
            game_framework.push_state(pause_state)
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
