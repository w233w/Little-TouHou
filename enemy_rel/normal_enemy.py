from .base_enemy import BaseEnemy
from bullet_rel import NormalBullet
from drop_rel import PowerDrop
from group_controller import bullets, player_ammo, drop_items
import pygame


# 二号敌人
# 会不断发射4颗普通子弹
class NormalEnemy(BaseEnemy):
    def __init__(
        self, pos: pygame.Vector2, max_hp: int, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(pos, max_hp, *groups)
        self.image = pygame.image.load("./images/enemy_2.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.pos[1] < 100:
            self.pos += pygame.Vector2(0, 1)
        self.rect.center = self.pos
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.last_shot
        if time_pass >= 1000:
            self.last_shot = curr_time
            for i in range(4):
                NormalBullet(self.pos, 4, i, 30, 0, bullets)
        self.on_hit(player_ammo)
        if self.dead:
            PowerDrop(self.pos, drop_items)
            self.kill()
