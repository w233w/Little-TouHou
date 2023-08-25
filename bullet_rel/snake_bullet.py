from .base_bullet import BaseBullet
import math
from pygame import Vector2, time
from pygame.sprite import Group
from utils.const import *


# 蛇形弹幕（单个）
# 数个子弹从屏幕正上方落下，运动时左右摆动，遵从正弦函数曲线。
# total_num共有几个子弹下落，index代表从左数的第几个，speed代表速度和幅度
class SnakeBullet(BaseBullet):
    def __init__(
        self, pos: Vector2, total_num, index=0, speed=1, *groups: Group
    ) -> None:
        self.pos = Vector2(self.x, HEADLINE)
        super().__init__(pos, *groups)
        self.x = (WIDTH / (total_num - 1)) * index
        self.speed = speed

    def update(self, player):
        curr_time = time.get_ticks()
        time_pass = curr_time - self.ini_time
        del_x = math.sin(2 * math.pi * time_pass / (1000 * self.speed))
        del_y = self.speed
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        self.rect.center = self.pos
        if player.sprite.is_bomb:
            if self.pos.distance_to(player.sprite.pos) < 500:
                self.kill()
