import pygame
from player_rel.player_shot import PlayerShot
from utils.const import *
from group_controller import drop_items, player_ammo, bullets, player_re


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image: pygame.Surface = pygame.image.load("./images/player.png")
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)
        self.pos: pygame.Vector2 = pygame.Vector2(200, 560)
        self.rect: pygame.Rect = self.image.get_rect(center=self.pos)

        self.hp: int = 6  # 血量

        self.last_shoot: int = 0  # 用于两条用于计算射击间隔
        self.shoot_interval: int = 200  # ms

        self.last_bomb: int = 0  # 以下四条用于玩家的消弹技能
        self.bomb: int = 3
        self.is_bomb: bool = False
        self.bomb_interval: int = 3000  # ms

        self.power: int = 3  # 攻击力

        for i in range(self.hp):
            HeartImage(i, self, player_re)
        for i in range(self.bomb):
            BombImage(i, self, player_re)

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

    def use_bomb(self, bomb_radius):
        if bomb_radius == -1:
            all_bullets = bullets.sprites()
            bullets.empty()
            del all_bullets[:]
        else:
            pygame.sprite.spritecollide(
                BombEffect(self.pos, bomb_radius),
                bullets,
                True,
                pygame.sprite.collide_mask,
            )

    def update(self):
        # bomb会消掉所有屏幕上的子弹
        if self.is_bomb:  # 顺序不能变
            self.use_bomb(-1)
        # boom只有一帧，update前先结束掉
        self.is_bomb = False
        # 死亡判定
        if self.hp <= 0:
            # TODO change death behavior
            # self.kill()
            self.image.fill(BackgroundColor)
            return
        # 吃道具判定
        collided_items = pygame.sprite.spritecollide(
            self, drop_items, True, pygame.sprite.collide_mask
        )
        for item in collided_items:
            if item.type == "energy":
                self.power += 0.5
            elif item.type == "hp":
                HeartImage(self.hp, self, player_re)
                self.hp += 1
            elif item.type == "bomb":
                BombImage(self.hp, self, player_re)
                self.bomb += 1
        # 中弹判定
        collided_bullets = pygame.sprite.spritecollide(
            self, bullets, True, pygame.sprite.collide_mask
        )
        if len(collided_bullets) > 0:
            self.hp -= 1
            self.use_bomb(100)
        del collided_bullets[:]
        # 攻击力不会大于五
        if self.power > 5:
            self.power = 5
        # 移动
        self.pos += self._player_control()
        self.rect.center = self.pos
        # 根据间隔检测是否能打出子弹
        current_time = pygame.time.get_ticks()
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


# 绘制血量图像
class HeartImage(pygame.sprite.Sprite):
    def __init__(
        self, index, bounding_player: Player, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("./images/heart.png")
        self.player = bounding_player
        self.index = index
        self.pos = pygame.Vector2(10 + 20 * index, 10)  # 左上角
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.index >= self.player.hp:
            self.kill()


# 绘制大招图像
class BombImage(pygame.sprite.Sprite):
    def __init__(
        self, index, bounding_player: Player, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("./images/bomb.png")
        self.player = bounding_player
        self.index = index
        self.pos = pygame.Vector2(WIDTH - 10 - 20 * index, 10)  # 右上角
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.index >= self.player.bomb:
            self.kill()


class BombEffect(pygame.sprite.Sprite):
    def __init__(self, pos, bomb_radius) -> None:
        super().__init__()
        self.bomb_radius = bomb_radius
        self.image = pygame.Surface((2 * bomb_radius, 2 * bomb_radius))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        bomb_center = pygame.Vector2(bomb_radius, bomb_radius)
        pygame.draw.circle(self.image, Red, bomb_center, bomb_radius)
        self.mask = pygame.mask.from_surface(self.image)
