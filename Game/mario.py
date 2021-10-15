from pico2d import *

class Mario:
    global x, y
    global x_dir, y_dir
    global jumping

    def __init__(self):
        self.x, self.y = x, y
        self.image = load_image('white mario.png')
        self.frame = 0

    def update(self):
        self.x += x_dir * 7
        self.y += y_dir * 7
        self.frame = (self.frame + 1) % 2
        x, y = self.x, self.y

    def draw(self):
        if x_dir > 0:
            self.image.clip_draw(self.frame * 128, 11 * 128, 128, 128, self.x, self.y)
        elif x_dir < 0:
            self.image.clip_draw(self.frame * 128, 12 * 128, 128, 128, self.x, self.y)
        else:
            self.image.clip_draw(0, 4 * 128, 128, 128, self.x, self.y)