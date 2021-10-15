from pico2d import *

MAP_WIDTH = 1284
MAP_HEIGHT = 780


# Game object class here
class Map:
    def __init__(self):
        self.x, self.y = 0, 0
        self.image1 = load_image('map1.png')
        self.image2 = load_image('map2.png')

    def update(self):
        self.x -= x_dir * 50
        self.y -= y_dir * 50

    def draw(self):
        self.image1.clip_draw(0, 0, 5136, 720, self.x + 2568, self.y + 330)


class Cloud:
    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('cloud1.png')

    def update(self):
        self.x -= x_dir * 6
        self.y -= y_dir * 6

    def draw(self):
        # self.image.draw(642, 420)
        self.image.clip_draw(0, 0, 5000, 720, self.x + 642, self.y + 420)


class Hill:
    def __init__(self):
        self.image = load_image('hills.png')

    def draw(self):
        self.image.draw(642, 400)

class Coin:
    def __init__(self):
        self.x, self.y = 100, 100
        self.image = load_image('coin.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 45, 0, 45, 48, self.x, self.y)


class Block:
    def __init__(self):
        self.x, self.y = 792, 234
        self.image = load_image('block.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 3

    def draw(self):
        self.image.clip_draw(self.frame * 48, 0, 48, 48, self.x, self.y)


class Super_Mushroom:
    def __init__(self):
        self.x, self.y = 1200, 90
        self.image = load_image('super mushroom.png')

    def update(self):
        self.x -= 3

    def draw(self):
        self.image.draw(self.x, self.y)


class Goomba:
    def __init__(self):
        self.x, self.y = 1200, 90
        self.image = load_image('Goomba.png')
        self.frame = 0

    def update(self):
        self.x -= 5
        self.frame = (self.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)


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




def handle_events():
    global running
    global x, y
    global x_dir, y_dir
    global jump_x, jump_y
    global jumping

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                x_dir += 1
            elif event.key == SDLK_LEFT:
                x_dir -= 1
            elif event.key == SDLK_SPACE:
                jumping = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                x_dir -= 1
            elif event.key == SDLK_LEFT:
                x_dir += 1
            elif event.key == SDLK_SPACE:
                jumping = False


# initialization code
open_canvas(MAP_WIDTH, MAP_HEIGHT)

x, y = MAP_WIDTH // 2, 120
x_dir, y_dir = 0, 0
jump_x, jump_y = 0, 0
jumping = False

base = Map()
cloud = Cloud()
hill = Hill()

coin = Coin()
block = Block()
mushroom = Super_Mushroom()
goomba = Goomba()
mario = Mario()

running = True
# game main loop code
while running:
    handle_events()

    # game logic
    base.update()
    cloud.update()
    goomba.update()
    mario.update()
    coin.update()
    block.update()
    mushroom.update()

    # game drawing
    clear_canvas()

    cloud.draw()
    hill.draw()
    base.draw()

    goomba.draw()
    mario.draw()
    coin.draw()
    block.draw()
    mushroom.draw()

    update_canvas()

    delay(0.05)

# finalization code
close_canvas()