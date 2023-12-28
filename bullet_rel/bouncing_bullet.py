from .base_bullet import BaseBullet
import math
from pygame import Vector2
from pygame.sprite import Group


class BouncingBullet(BaseBullet):
    def __init__(
        self,
        pos: Vector2,
        dir_angle: int,
        *groups: Group,
        bouncing_limit: int = 3,
    ) -> None:
        super().__init__(pos, *groups)
        self.dir = dir_angle
        self.radian = math.radians(self.dir)
        del_x = math.sin(self.radian)
        del_y = math.cos(self.radian)
        self.del_v = Vector2(del_x, del_y) * 2
        self.bouncing_limit = bouncing_limit

    def update(self) -> None:
        # 处理边缘反弹
        if self.bouncing_limit >= 1:
            ver, hor = self.out_of_bound(0)
            if ver:
                self.del_v[0] = -self.del_v[0]
            if hor:
                self.del_v[1] = -self.del_v[1]
            if any((ver, hor)):
                self.bouncing_limit -= 1

        self.pos += self.del_v
        self.rect.center = self.pos
