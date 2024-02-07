from .base_enemy import BaseEnemy
from bullet_rel import NormalBullet
from group_controller import bullets, player_ammo
from pygame import Vector2, image, mask, time
from pygame.sprite import Group


# 二号敌人
# 会不断发射4颗普通子弹
class NormalEnemy(BaseEnemy):
    def __init__(
        self, pos: Vector2, max_hp: int, drop_config: list[str], *groups: Group
    ) -> None:
        super().__init__(pos, max_hp, drop_config, *groups)
        self.image = image.load("./images/enemy_2.png")
        self.mask = mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        curr_time = time.get_ticks()
        if curr_time - self.init_time > 15 * 1000:
            self.pos += Vector2(0, -1)
        elif self.pos[1] < 100:
            self.pos += Vector2(0, 1)
        self.rect.center = self.pos
        time_pass = curr_time - self.last_shot
        if time_pass >= 1000:
            self.last_shot = curr_time
            for i in range(4):
                NormalBullet(self.pos, 4, i, 30, 0, bullets)
        self.on_hit(player_ammo)
        if self.dead:
            self.make_drop()
            self.kill()
