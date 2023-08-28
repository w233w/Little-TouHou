from .base_bullet import BaseBullet
import math
from pygame import Vector2, time
from pygame.sprite import Group


# 开花型环绕子弹（一圈）
# 几何中心在椭圆长轴的一个端点上
# total_num表示每圈一共有几个，index代表环上的第几个，group表示层数，pos表示子弹射出的位置
class AtomBullet(BaseBullet):
    def __init__(self, pos: Vector2, total_num, index, group=0, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.group = group
        self.degree = 360 / total_num * self.index

    def update(self):
        self.degree += 2 + self.group * 2
        radian = math.radians(self.degree)
        del_x = math.sin(radian) * 2
        del_y = math.cos(radian) * 2
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        self.rect.center = self.pos
