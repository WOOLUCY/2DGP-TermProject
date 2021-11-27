from pico2d import *
import game_framework
import game_world
import server
import collision
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

# Monster Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 7.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Monster Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

animation_names = ['Walk', 'Idle']

class Monster:
    spr = None

    def load_sprites(self):
        if Monster.spr == None:
            Monster.spr = load_image('./res/image/Goomba.png')

    def __init__(self, x, y):
        # variables
        self.x, self.y = x, y
        self.spr_w, spr_h = 0, 0
        self.frame = 0
        self.frame_amount = 0
        self.timer = 10.0
        self.attack_timer = 0.0
        self.wait_timer = 2.0
        self.dir = 1
        self.speed = 0

        # functions
        self.load_sprites()
        self.build_behavior_tree()

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 10.0
            self.dir *= -1
            print("Wander Success")
            return BehaviorTree.SUCCESS
        return BehaviorTree.SUCCESS

    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 2.0
            print("Wait Success")
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode('Wander', self.wander)
        wait_node = LeafNode('Wait', self.wait)
        wander_wait_node = SequenceNode('WanderAndWait')
        wander_wait_node.add_children(wander_node, wait_node)

        self.bt = BehaviorTree(wander_wait_node)

    def get_bb(self):
        return self.x - self.spr_w/2, self.y - self.spr_h/2, \
               self.x + self.spr_w/2, self.y + self.spr_h/2

    def update(self):
        self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount

        self.x += self.speed * self.dir * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)


        # collision
        if self.attack_timer > 0:
            self.timer -= game_framework.frame_time
            self.attack_timer = int(self.attack_timer)
            # print(self.timer)

        if collision.collide(server.mario, self) and self.attack_timer == 0:
            print("mario-goomba COLLISION")
            server.mario.life -= 1
            self.attack_timer = 500.0

        for fire_ball in server.fireballs.copy():
            if collision.collide(self, fire_ball):
                game_world.remove_object(fire_ball)
                server.fireballs.remove(fire_ball)

                game_world.remove_object(self)

    def draw(self):
        self.spr.clip_draw(int(self.frame) * self.spr_w, 0, self.spr_w, self.spr_h, self.x, self.y)
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        pass

class Goomba(Monster):
    def __init__(self, x, y):
        # variables
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 64, 64
        self.frame = 0
        self.frame_amount = 2
        self.timer = 10.0
        self.attack_timer = 0.0
        self.wait_timer = 2.0
        self.dir = 1
        self.speed = 0

        # functions
        self.load_sprites()
        self.build_behavior_tree()


class Koopa_Troopa(Monster):
    def __init__(self, x, y, velocity = 0):
        self.x, self.y, self.velocity = x, y, velocity
        # self.spr = load_image('./res/image/Goomba.png')
        self.spr_w, self.spr_h = 48, 64
        self.frame = 0
        self.frame_amount = 2
        if Koopa_Troopa.spr == None:
            Koopa_Troopa.spr = load_image('./res/image/Koopa Troopa.png')
        self.velocity += RUN_SPEED_PPS
        self.dir = 1
        self.font = load_font('./res/font/ENCR10B.TTF', 16)

    def update(self):
        if clamp(800, self.x, 1200) == 1200:
            self.velocity -= RUN_SPEED_PPS
        elif clamp(800, self.x, 1200) == 800:
            self.velocity += RUN_SPEED_PPS
        self.dir = clamp(-1, self.velocity, 1)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_amount
        self.x += self.velocity * game_framework.frame_time

    def draw(self):
        if self.dir == -1:
            self.spr.clip_draw(int(self.frame) * self.spr_w, 64, self.spr_w, self.spr_h, self.x, self.y)
        else:
            self.spr.clip_composite_draw(int(self.frame) * self.spr_w, 64,self.spr_w, self.spr_h, 0, 'h', self.x, self.y,self.spr_w, self.spr_h)
        # debug_print('Velocity :' + str(self.velocity) + '   Dir :' + str(self.dir))
        self.font.draw(self.x - 32, self.y + 50, 'Dir :' + str(self.dir), (255, 0, 255))
        draw_rectangle(*self.get_bb())

class Koopa_Troopa_Shell(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 32, 32
        self.frame = 0
        self.frame_amount = 4
        if Koopa_Troopa_Shell.spr == None:
            Koopa_Troopa_Shell.spr = load_image('./res/image/Shell.png')



class Piranha_Plant(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 64, 64
        self.frame = 0
        self.frame_amount = 2
        if Piranha_Plant.spr == None:
            Piranha_Plant.spr = load_image('./res/image/Piranha Plant.png')


class Bowser(Monster):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spr_w, self.spr_h = 136, 168
        self.frame = 0
        self.frame_amount = 4
        if Bowser.spr == None:
            Bowser.spr = load_image('./res/image/Bowser.png')
