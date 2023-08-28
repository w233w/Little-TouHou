from .base_bullet import BaseBullet
from group_controller import player
from pygame import Vector2, time
from pygame.sprite import Group


# 三次贝塞尔曲线弹幕（自机狙）
# side决定子弹射出的方向，index和group决定了子弹运动的幅度，index决定宽度，group决定高度，pos是子弹射出的位置
# 子弹射出后会追踪射出时玩家的位置，仅一次。玩家在平行移动后理应可以轻松躲开子弹。
class CubicBezierCurve(BaseBullet):
    def __init__(self, pos: Vector2, side, index=0, group=0, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.p1 = Vector2(pos)
        if side == "l":
            self.p2 = Vector2(200 - 30 * group, 100 - 30 * group)
            self.p3 = Vector2(100 - 70 * index, 200 - 30 * index)
        else:
            self.p2 = Vector2(200 + 30 * group, 100 - 30 * group)
            self.p3 = Vector2(300 + 70 * index, 200 - 30 * index)
        self.p4 = Vector2(player.sprite.pos)

    def update(self):
        curr_time = time.get_ticks()
        time_pass = curr_time - self.ini_time
        t = time_pass / 3000
        sec1 = ((1 - t) ** 3) * self.p1
        sec2 = 3 * t * ((1 - t) ** 2) * self.p2
        sec3 = 3 * (1 - t) * (t**2) * self.p3
        sec4 = (t**3) * self.p4
        pos = sec1 + sec2 + sec3 + sec4
        self.rect.center = pos
        if self.out_of_bound():
            self.kill()
