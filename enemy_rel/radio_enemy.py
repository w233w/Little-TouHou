from pygame import Vector2, image, mask, time
from pygame.sprite import Group
from .base_enemy import BaseEnemy
from bullet_rel import NormalBullet
from group_controller import bullets, player_ammo
from utils.const import HEIGHT


class RadioEnemy(BaseEnemy):
    def __init__(
        self, pos: Vector2, max_hp: int, drop_config: list[str], *groups: Group
    ) -> None:
        super().__init__(pos, max_hp, drop_config, *groups)
        self.image = image.load("./images/enemy_radio.png")
        self.mask = mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.side = "left"

    def update(self):
        self.pos += Vector2(0, 2)
        self.rect.center = self.pos
        curr_time = time.get_ticks()
        time_pass = curr_time - self.last_shot
        if time_pass >= 800:
            self.last_shot = curr_time
            if self.side == "left":
                for i in range(5):
                    NormalBullet(self.pos, 5, i, 90, -90, bullets)
                self.side = "right"
            else:
                for i in range(5):
                    NormalBullet(self.pos, 5, i, 90, 90, bullets)
                self.side = "left"
        self.on_hit(player_ammo)
        if self.dead:
            self.make_drop()
            self.kill
        if self.pos.y > HEIGHT + self.image.get_height():
            self.kill()
