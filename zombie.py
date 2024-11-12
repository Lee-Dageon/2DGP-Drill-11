import random
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.size = 1.0
        self.hit_count = 0
        self.is_deleted = False  # 삭제 상태 플래그 추가

    def update(self):
        if not self.is_deleted:  # 삭제된 상태라면 업데이트하지 않음
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
            if self.x > 1600:
                self.dir = -1
            elif self.x < 800:
                self.dir = 1
            self.x = clamp(800, self.x, 1600)

    def draw(self):
        if not self.is_deleted:  # 삭제된 상태라면 그리지 않음
            if self.dir < 0:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 200 * self.size,
                                                                      200 * self.size)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 200 * self.size, 200 * self.size)
            draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        # fill here
        # 네 개의 값, x1, y1, x2, y2
        return self.x-60, self.y-75, self.x+60, self.y+75   #네 개의 값으로 구성된 하나의 튜플
        pass


    def handle_collision(self, group, other):
        if group == 'zombie:ball' and not self.is_deleted:
            if self.hit_count == 0:  # 첫 번째 충돌 시
                self.size = 0.5
                self.hit_count += 1
            elif self.hit_count == 1:  # 두 번째 충돌 시
                self.is_deleted = True  # 삭제 상태로 변경
                game_world.remove_object(self)  # 게임 월드에서 좀비 삭제

        elif group == 'boy:zombie' and not self.is_deleted:
            delay(1)
            game_framework.quit()  # 게임 종료


        pass


