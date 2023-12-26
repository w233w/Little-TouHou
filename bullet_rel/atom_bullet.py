from .base_bullet import BaseBullet
import math
from pygame import Vector2
from pygame.sprite import Group


# 开花型环绕子弹（一圈）
# 几何中心在椭圆长轴的一个端点上
# total_num表示每圈一共有几个，index代表环上的第几个，pos表示子弹射出的位置
class AtomBullet(BaseBullet):
    def __init__(self, pos: Vector2, total_num, index, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.degree = 360 / total_num * self.index
        self.init_degree = self.degree
        self.power = 1

    def update(self):
        self.degree += 5
        if (self.degree - self.init_degree) % 360 == 0:
            self.power += 1
        radian = math.radians(self.degree)
        del_x = math.sin(radian)
        del_y = math.cos(radian)
        del_v = Vector2(del_x, del_y) * (self.power / 2)
        self.pos += del_v
        self.pos += Vector2(0, 1 + self.power // 2)
        self.rect.center = self.pos
