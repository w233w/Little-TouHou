from .base_enemy import BaseEnemy
from pygame import Vector2, image, mask, time
from pygame.sprite import Group
from bullet_rel import CubicBezierCurve
from group_controller import bullets, player_ammo


# 一号敌人
# 会不断发射两颗贝塞尔曲线弹幕
class BezierEnemy(BaseEnemy):
    def __init__(
        self, pos: Vector2, max_hp: int, drop_config: list[str], *groups: Group
    ) -> None:
        super().__init__(pos, max_hp, drop_config, *groups)
        self.image = image.load("./images/enemy_1.png")
        self.mask = mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        curr_time = time.get_ticks()
        if curr_time - self.init_time > 15 * 1000:
            self.pos += Vector2(0, -1)
        elif self.pos[1] < 200:
            self.pos += Vector2(0, 1)
        self.rect.center = self.pos
        time_pass = curr_time - self.last_shot
        if time_pass / 1000 >= 1:
            self.last_shot = curr_time
            for i in range(1):
                for j in range(1):
                    CubicBezierCurve(self.pos, "l", i, j, bullets)
                    CubicBezierCurve(self.pos, "r", i, j, bullets)
        self.on_hit(player_ammo)
        if self.dead:
            self.make_drop()
            self.kill()
