from pico2d import *


class Goomba:
    def __init__(self):
        self.x, self.y = 100, 300
        self.image = load_image('./res/image/Goomba.png')
        self.frame = 0
        self.x_dir = 0

    def update(self):
        self.frame = (self.frame + 1) % 2
        if self.x <= 300:
            self.x_dir += 1
        else:
            self.x_dir -= 1

        self.x += self.x_dir * 3

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)


class Koopa_Troopa:
    def __init__(self):
        self.x, self.y = 1000, 200
        self.image = load_image('./res/image/Koopa Troopa.png')
        self.frame = 0

    def update(self):
        self.x -= 5
        self.frame = (self.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.frame * 48, 0, 48, 64, self.x, self.y)


class Koopa_Troopa_Shell:
    def __init__(self):
        self.x, self.y = 300, 400
        self.image = load_image('./res/image/Shell.png')
        self.frame = 0

    def update(self):
        # self.x -= 5
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y)

class Piranha_Plant:
    def __init__(self):
        self.x, self.y = 400, 400
        self.image = load_image('./res/image/Piranha Plant.png')
        self.frame = 0

    def update(self):
        # self.x -= 5
        self.frame = (self.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.frame * 64, 64, 64, 64, self.x, self.y)


class Bowser:
    def __init__(self):
        self.x, self.y = 700, 400
        self.image = load_image('./res/image/Bowser.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 136, 0, 136, 168, self.x, self.y)