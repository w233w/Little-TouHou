from pygame import Vector2
import pygame
from pygame.sprite import Group
from .base_enemy import BaseEnemy
from bullet_rel import ArcBullet, NormalBullet
from group_controller import bullets, player_ammo
from utils.const import *


class LevelOneBoss(BaseEnemy):
    def __init__(self, pos: Vector2, time_wait: int, *groups: Group) -> None:
        super().__init__(
            pos, 1, *groups
        )  #  Boss always start with 1 hp, it will change/refill between stages
        self.image = pygame.image.load("./images/enemy_1.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.time_wait = time_wait
        self.shot_shift = 0
        self.hp = 0
        self.stage = 0
        self.stage_2_flag = 0

    def update(self):
        if self.stage == 0:
            self.stage_0_action()
        elif self.stage == 1:
            self.stage_1_action()
        elif self.stage == 2:
            self.stage_2_action()
        elif self.stage == 3:
            self.stage_3_action()
        elif self.stage == 4:
            self.stage_4_action()

    def stage_0_action(self):
        self.on_hit(player_ammo, 99999)
        if self.time_wait > 0:
            self.time_wait -= 1000 / 60
        elif self.pos.y < 200:
            self.pos += Vector2(0, 1)
            self.rect.center = self.pos
        else:
            self.stage += 1

    def stage_1_action(self):
        self.max_hp = 120
        if self.hp < self.max_hp:
            self.hp += self.max_hp / FPS
        else:
            self.stage += 1
            self.last_shot = pygame.time.get_ticks()

    def stage_2_action(self):
        self.on_hit(player_ammo)
        if self.dead:
            self.stage += 1
        if pygame.time.get_ticks() - self.last_shot >= 500:
            num = 5 - self.stage_2_flag
            for i in range(num):
                NormalBullet(self.pos, num, i, 30, 0, bullets)
            self.stage_2_flag = 1 - self.stage_2_flag
            self.last_shot = pygame.time.get_ticks()

    def stage_3_action(self):
        self.max_hp = 1200
        if self.hp < self.max_hp:
            self.hp += self.max_hp / FPS
        else:
            self.stage += 1
            self.last_shot = pygame.time.get_ticks()

    def stage_4_action(self):
        self.on_hit(player_ammo)
        self.on_time(1)
        if self.dead:
            self.kill()
        if pygame.time.get_ticks() - self.last_shot >= 400:
            radius = 250
            inner_r = 30
            for ang in range(0 + self.shot_shift, 360 + self.shot_shift, 20):
                far_center = Vector2(200, 200) + Vector2(radius, 0).rotate(ang)
                init = Vector2(200, 200) + Vector2(inner_r, 0).rotate(ang)
                ArcBullet(init, far_center, 0.6, False, bullets)
                ArcBullet(init, far_center, 0.6, True, bullets)
            self.last_shot = pygame.time.get_ticks()
            self.shot_shift += 3
