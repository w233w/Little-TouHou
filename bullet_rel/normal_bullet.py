from .base_bullet import BaseBullet
import math
from pygame import Vector2
from pygame.sprite import Group


# 常规直线射弹
# 根据弹数向下方发射直线弹幕,pos是起始点位
class NormalBullet(BaseBullet):
    def __init__(self, pos: Vector2, total_num, index, angle, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.degree = angle / (total_num - 1) * self.index - angle / 2
        self.radian = math.radians(self.degree)

    def update(self, player):
        if self.out_of_bound():
            self.kill()
        del_x = math.sin(self.radian) * 2
        del_y = math.cos(self.radian) * 2
        del_v = Vector2(del_x, del_y)
        self.pos = self.pos + del_v
        self.rect.center = self.pos
        if self.pos.distance_to(player.sprite.pos) < 7:
            player.sprite.hp -= 1
            self.kill()
        if player.sprite.is_bomb:
            if self.pos.distance_to(player.sprite.pos) < 500:
                self.kill()
