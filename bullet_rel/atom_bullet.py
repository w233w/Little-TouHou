from .base_bullet import BaseBullet
import math
from pygame import Vector2
from pygame.sprite import Group


# 开花型环绕子弹（一圈）
# 几何中心在椭圆长轴的一个端点上
# total_num表示每圈一共有几个，index代表环上的第几个，pos表示子弹射出的位置
class AtomBullet(BaseBullet):
    def __init__(
        self,
        pos: Vector2,
        total_num,
        index,
        *groups: Group,
        init_pow=1,
        incrs_pow=1,
        incrs_pow_rate=0.5,
        incrs_pow_rotate=1,
        incrs_speed=0.5,
    ) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.degree = 360 / total_num * self.index
        self.init_degree = self.degree
        self.power = init_pow
        self.incrs_pow = incrs_pow
        self.incrs_pow_rate = incrs_pow_rate
        self.incrs_pow_rotate = incrs_pow_rotate
        self.incrs_speed = incrs_speed

    def update(self):
        if any(self.out_of_bound()):
            self.kill()
        self.degree += 5
        if (self.degree - self.init_degree) % (360 * self.incrs_pow_rotate) == 0:
            self.power += self.incrs_pow
        radian = math.radians(self.degree)
        del_x = math.sin(radian)
        del_y = math.cos(radian)
        del_v = Vector2(del_x, del_y) * (self.power * self.incrs_pow_rate)
        self.pos += del_v
        self.pos += Vector2(0, self.power * self.incrs_speed)
        self.rect.center = self.pos
