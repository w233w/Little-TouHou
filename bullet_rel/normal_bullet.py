from .base_bullet import BaseBullet
import math
from pygame import Vector2
from pygame.sprite import Group


# 常规直线射弹
# 根据弹数向下方发射直线弹幕,pos是起始点位,angle是扇形角度，dir_angle是发射角度
# dir_angle为0时指向正下，数据按逆时针变化
# total_num是弹幕总数，index是本实例顺时针数是弹幕中的第几个
# 需要通过循环来使用：
# for i in range(n):
#   NormalBullet(pos, n, i, ang, dir_ang, groups)
class NormalBullet(BaseBullet):
    def __init__(
        self, pos: Vector2, total_num, index, angle, dir_angle=0, *groups: Group
    ) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.degree = angle / (total_num - 1) * self.index - angle / 2 + dir_angle
        self.radian = math.radians(self.degree)

    def update(self):
        if any(self.out_of_bound()):
            self.kill()
        del_x = math.sin(self.radian) * 2
        del_y = math.cos(self.radian) * 2
        del_v = Vector2(del_x, del_y)
        self.pos = self.pos + del_v
        self.rect.center = self.pos
