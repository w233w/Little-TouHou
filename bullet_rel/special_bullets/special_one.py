from .precise_bullet import PreciseBullet
from pygame import Vector2
from pygame.sprite import Group


# 子弹会从右上角按一定间隔出发，终点在（30，500）。
# 路径是从右上到左下的二次曲线
# 路径会穿过左边缘，再从右边缘回来
class SP_one_controller:
    def __init__(self, *groups: Group) -> None:
        self.init_pos = Vector2
        self.bullets_route = list[list[Vector2]]
        if groups:
            self.groups = groups

    def start(self):
        for b_route in self.bullets_route:
            PreciseBullet(b_route, self.groups)
