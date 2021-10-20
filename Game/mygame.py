import game_framework
import pico2d

import start_state
import main_state

MAP_WIDTH = 1284
MAP_HEIGHT = 780

pico2d.open_canvas(MAP_WIDTH, MAP_HEIGHT)
game_framework.run(main_state)
pico2d.close_canvas()
