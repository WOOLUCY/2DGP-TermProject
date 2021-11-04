import game_framework
import pico2d

import start_state
import main_state
import test_state
import pause_state
import object_state
import monster_state

MAP_WIDTH = 1280
MAP_HEIGHT = 700

pico2d.open_canvas(MAP_WIDTH, MAP_HEIGHT)
game_framework.run(test_state)
pico2d.close_canvas()
