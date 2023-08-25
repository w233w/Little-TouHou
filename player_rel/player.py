import pygame
from player_rel.playerShot import PlayerShot
from utils.const import *
from group_controller import drop_items, player_ammo


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load("./images/player.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(200, 560)
        self.rect = self.image.get_rect(center=self.pos)

        self.hp = 6  # 血量

        self.last_shoot = 0  # 用于两条用于计算射击间隔
        self.shoot_interval = 200  # ms

        self.last_bomb = 0  # 以下四条用于玩家的消弹技能
        self.bomb = 3
        self.is_bomb = False
        self.bomb_interval = 3000  # ms

        self.power = 3  # 攻击力

    # 自机控制
    # 返回的值决定了速度

    def _player_control(self):
        left = pygame.key.get_pressed()[pygame.K_LEFT]
        up = pygame.key.get_pressed()[pygame.K_UP]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        # 按下shift可以加速，目前是三倍速
        shift = 1 + 2 * pygame.key.get_pressed()[pygame.K_LSHIFT]
        del_x = right - left
        del_y = down - up
        # 限制玩家不能离开屏幕
        if self.pos.x < 5 and del_x < 0:
            del_x = 0
            self.pos.x = 4
        elif self.pos.x > WIDTH - 6 and del_x > 0:
            del_x = 0
            self.pos.x = WIDTH - 5
        if self.pos.y < 5 and del_y < 0:
            del_y = 0
            self.pos.y = 4
        elif self.pos.y > HEIGHT - 6 and del_y > 0:
            del_y = 0
            self.pos.y = HEIGHT - 5
        return shift * pygame.Vector2(del_x, del_y)

    def update(self):
        print(self.power)
        # boom只有一帧，update前先结束掉
        self.is_bomb = False
        # 死亡判定
        if self.hp <= 0:
            self.kill()
            return
        # 吃道具判定
        collided_items = pygame.sprite.spritecollide(
            self, drop_items, True, pygame.sprite.collide_mask
        )
        for item in collided_items:
            if item.type == "energy":
                self.power += 0.5
            elif item.type == "hp":
                self.hp += 1
            elif item.type == "bomb":
                self.bomb += 1
        # 攻击力不会大于五
        if self.power > 5:
            self.power = 5
        # 移动
        self.pos += self._player_control()
        self.rect.center = self.pos
        current_time = pygame.time.get_ticks()
        # 根据间隔检测是否能打出子弹
        if (
            pygame.key.get_pressed()[pygame.K_z] == 1
            and current_time - self.last_shoot >= self.shoot_interval
        ):
            self.last_shoot = current_time
            # 根据power射出多个子弹，每两点攻击力加一颗子弹， 最多三个子弹
            ammo_num = int((self.power + 1) // 2)
            for i in range(ammo_num):
                PlayerShot(self.power, i, self.pos, player_ammo)
        # 检测是否可以boom，并在可以时激活
        if (
            self.bomb > 0
            and pygame.key.get_pressed()[pygame.K_x] == 1
            and current_time - self.last_bomb >= self.bomb_interval
        ):
            self.last_bomb = current_time
            self.is_bomb = True
            self.bomb -= 1
