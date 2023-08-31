from pygame import Vector2
import pygame
from pygame.sprite import Group
from .base_enemy import BaseEnemy
from bullet_rel import ArcBullet
from group_controller import bullets, player_ammo


class LevelOneBoss(BaseEnemy):
    def __init__(self, pos: Vector2, max_hp: int, *groups: Group) -> None:
        super().__init__(pos, max_hp, *groups)
        self.image = pygame.image.load("./images/enemy_1.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.shot_shift = 0

    def update(self):
        self.on_hit(player_ammo)
        if self.hp <= 0:
            self.kill()
        if pygame.time.get_ticks() - self.last_shot >= 500:
            radius = 250
            inner_r = 30
            for ang in range(0 + self.shot_shift, 360 + self.shot_shift, 20):
                far_center = Vector2(200, 200) + Vector2(radius, 0).rotate(ang)
                init = Vector2(200, 200) + Vector2(inner_r, 0).rotate(ang)
                ArcBullet(init, far_center, 0.6, False, bullets)
                ArcBullet(init, far_center, 0.6, True, bullets)
            self.last_shot = pygame.time.get_ticks()
            self.shot_shift += 3
