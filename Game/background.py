from pico2d import *

class Map:
    # global x_dir

    def __init__(self):
        self.x, self.y = 0, 0
        self.image1 = load_image('./res/image/map1.png')
        self.image2 = load_image('./res/image/map2.png')

    def update(self):
        # self.x -= x_dir * 50
        pass

    def draw(self):
        self.image1.clip_draw(0, 0, 5136, 720, self.x + 2568, self.y + 330)


class Cloud:
    # global x_dir

    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('./res/image/cloud1.png')

    def update(self):
        # self.x -= x_dir * 6
        pass

    def draw(self):
        # self.image.draw(642, 420)
        self.image.clip_draw(0, 0, 5000, 720, self.x + 642, self.y + 420)


class Hill:
    def __init__(self):
        self.image = load_image('./res/image/hills.png')

    def draw(self):
        self.image.draw(642, 400)