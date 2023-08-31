from pygame import Vector2
from pygame.sprite import Group
from .base_bullet import BaseBullet
from math import sin, cos, radians


# 圆弧轨迹的子弹
# 入参包括，init_pos起始位置，center_pos圆心位置，angle_speed角速度，clock_wise是否顺时针旋转
class ArcBullet(BaseBullet):
    def __init__(
        self,
        init_pos: Vector2,
        center_pos: Vector2,
        angle_speed: int,
        clock_wise: bool,
        *groups: Group,
    ) -> None:
        super().__init__(init_pos, *groups)
        self.center_pos = center_pos
        clock = [1, -1][clock_wise]
        self.angle_speed = clock * angle_speed
        self.radius = init_pos.distance_to(center_pos)
        self.angle = Vector2(1, 0).angle_to(init_pos - center_pos)
        self.radians = radians(self.angle)

    def update(self) -> None:
        if any(self.out_of_bound()):
            self.kill()
        self.angle += self.angle_speed
        self.radians = radians(self.angle)
        dx = cos(self.radians) * self.radius
        dy = sin(self.radians) * self.radius
        delta = Vector2(dx, dy)
        self.pos = self.center_pos + delta
        self.rect.center = self.pos


# 使用例example
# radius = 250
# inner_r = 30
# start = Vector2(200, 200)
# for ang in range(0, 360, 10):
#             far_center = Vector2(200, 200) + Vector2(radius, 0).rotate(ang)
#             init = Vector2(200, 200) + Vector2(inner_r, 0).rotate(ang)
#             ArcBullet(init, far_center, 0.6, False, bullets)
#             ArcBullet(init, far_center, 0.6, True, bullets)
