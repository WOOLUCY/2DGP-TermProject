import random
import server

from pico2d import *


class TileBackground:

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = 5136 * 2  # tile size
        self.h = 720 * 1

        # fill here
        self.tiles =[[load_image('./res/image/map%d%d.png' % (x, y)) for x in range(2)] for y in range(1)]
        print("map loaded")


    def update(self):
        pass

    def draw(self):
        self.window_left = clamp(0,
                                 int(server.mario.x) - self.canvas_width // 2,
                                 self.w - self.canvas_width)
        self.window_bottom = clamp(0,
                                   int(server.mario.y) - self.canvas_height // 2,
                                   self.h - self.canvas_height)

        # fill here
        tile_left = self.window_left // 5136 # 타일 크기
        tile_right = min((self.window_left + self.canvas_width) // 5136 + 1, 2)
        left_offset = self.window_left % 5136 # 타일 크기

        tile_bottom = self.window_bottom // 720 # 타일 크기
        tile_top = min((self.window_bottom + self.canvas_height) // 720 + 1, 1)
        bottom_offset = self.window_bottom % 720 # 타일 크기

        for ty in range(tile_bottom, tile_top):
            for tx in range(tile_left, tile_right):
                self.tiles[ty][tx].draw_to_origin(-left_offset+(tx-tile_left)*5136, -bottom_offset+(ty-tile_bottom)*720)


class FixedBackground:

    def __init__(self):
        self.image = load_image('./res/image/map1.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h


    def draw(self):
        # fill here
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)
        pass

    def update(self):
        # fill here
        # 맵상에서의 윈도우의 왼쪽 좌표, 오른쪽 좌표
        self.window_left = clamp(0, int(server.mario.x) - server.background.canvas_width // 2, server.background.w - server.background.canvas_width)
        self.window_bottom = clamp(0, int(server.mario.y) - server.background.canvas_height // 2, server.background.h - server.background.canvas_height)

    def handle_event(self, event):
        pass





