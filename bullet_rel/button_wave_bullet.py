from .base_bullet import BaseBullet
import math
from pygame import Vector2, time
from pygame.sprite import Group
from utils.const import *


# 波浪形弹幕
# 子弹在板底以海浪型波动
# total_num是密度，index可以大于total_num（如果需要平移的话）,shift是偏移量
# total_num应该是一个大数字，否则不会有连贯的视觉效果
class ButtonWave(BaseBullet):
    def __init__(
        self, pos: Vector2, total_num, index, height=1, shift=0, *groups: Group
    ) -> None:
        self.x = (WIDTH / (total_num - 1)) * index
        pos = Vector2(self.x, HEIGHT + 10)
        super().__init__(pos, *groups)
        self.index = index
        self.x = (WIDTH / (total_num - 1)) * index
        self.height = height
        self.shift = shift

    def update(self):
        curr_time = time.get_ticks()
        time_pass = curr_time - self.ini_time
        del_x = self.shift
        del_y = self.height * math.sin(
            2 * math.pi * time_pass / 1500 + self.index / 3
        )
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        self.rect.center = self.pos
        if self.pos[0] <= 0 and self.shift < 0:
            self.kill()
        if self.pos[0] >= WIDTH and self.shift > 0:
            self.kill()
