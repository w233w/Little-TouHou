from .base_enemy import BaseEnemy
from group_controller import bullets, player_ammo
from pygame import Vector2, image, mask, time
from pygame.sprite import Group
from bullet_rel import AtomBullet


class RingEnemy(BaseEnemy):
    def __init__(
        self, pos: Vector2, max_hp: int, drop_config: list[str], *groups: Group
    ) -> None:
        super().__init__(pos, max_hp, drop_config, *groups)
        self.image = image.load("./images/enemy_ring.png")
        self.mask = mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self) -> None:
        curr_time = time.get_ticks()
        if curr_time - self.init_time > 12 * 1000:
            self.pos += Vector2(0, -1)
            self.rect.center = self.pos
        elif self.pos[1] < 50:
            self.pos += Vector2(0, 1)
            self.rect.center = self.pos
        else:
            curr_time = time.get_ticks()
            time_pass = curr_time - self.last_shot
            if time_pass >= 2000:
                self.last_shot = curr_time
                for i in range(3):
                    AtomBullet(self.pos, 3, i, bullets)
        self.on_hit(player_ammo)
        if self.dead:
            self.make_drop()
            self.kill()
