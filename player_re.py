import pygame
import math
from pygame.math import Vector2

# 各类参数
# 窗口大小
WIDTH = 400
HEIGHT = 600
SIZE = WIDTH, HEIGHT
HEADLINE = 40
# 刷新率
FPS = 60
# 颜色
BackgroundColor = 255, 229, 204
Black = 0, 0, 0
White = 255, 255, 255
Red = 255, 0, 0

# 玩家子弹


class Player_shoot(pygame.sprite.Sprite):
    def __init__(self, power_level: int, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ammo.png")
        # 根据power额外射出子弹
        if power_level == 1:
            self.pos = Vector2(player.pos)
        elif power_level == 2:
            self.pos = Vector2(player.pos) + Vector2(-2 + index * 4, 0)
        else:
            del_y = 0
            if index != 1:
                del_y = 1
            self.pos = Vector2(player.pos) + Vector2(-4 + index * 4, del_y)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += Vector2(0, -4)  # 子弹速度
        self.rect.center = self.pos
        if(self.pos[1]) < -1:  # 离开屏幕后不再更新位置
            self.kill()

# 自机控制
# 返回的值决定了速度


def player_control():
    left = pygame.key.get_pressed()[pygame.K_LEFT]
    up = pygame.key.get_pressed()[pygame.K_UP]
    down = pygame.key.get_pressed()[pygame.K_DOWN]
    right = pygame.key.get_pressed()[pygame.K_RIGHT]
    # 按下shift可以加速，目前是三倍速
    shift = 2 * pygame.key.get_pressed()[pygame.K_LSHIFT] + 1
    del_x = right - left
    del_y = down - up
    # 限制玩家不能离开屏幕
    if player.pos[0] < 5 and del_x < 0:
        del_x = 0
    elif player.pos[0] > WIDTH - 6 and del_x > 0:
        del_x = 0
    if player.pos[1] < 5 and del_y < 0:
        del_y = 0
    elif player.pos[1] > HEIGHT - 6 and del_y > 0:
        del_y = 0
    return shift * Vector2(del_x, del_y)


# 自机

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.pos = Vector2(200, 560)
        self.rect = self.image.get_rect(center=self.pos)
        self.hp = 6  # 血量
        self.last_shoot = 0  # 用于计算射击间隔
        self.last_boom = 0  # 以下三条用于玩家的消弹技能
        self.boom = 3
        self.is_boom = False
        self.power = 1  # 攻击力

    def update(self):
        # boom只有一帧，update前先结束掉
        self.is_boom = False
        # 死亡判定
        if self.hp <= 0:
            self.kill()
        # 攻击力不会大于五
        if self.power > 5:
            self.power = 5
        # 移动
        self.pos += player_control()
        self.rect.center = self.pos
        current_time = pygame.time.get_ticks()
        # 根据间隔检测是否能打出子弹
        if pygame.key.get_pressed()[pygame.K_z] == 1 and current_time - self.last_shoot >= 100:
            self.last_shoot = current_time
            # 根据power射出多个子弹，每点攻击力加一颗子弹， 最多三个子弹
            power_Level = int(self.power)
            if self.power > 3:
                power_Level = 3
            for i in range(power_Level):
                ammo = Player_shoot(power_Level, i)
                player_ammo.add(ammo)
        # 检测是否可以boom，并在可以时激活
        if pygame.key.get_pressed()[pygame.K_x] == 1 and self.boom > 0 and current_time - self.last_boom >= 3000:
            self.last_boom = current_time
            self.is_boom = True
            self.boom -= 1

# 绘制血量图像


class Heart(pygame.sprite.Sprite):
    def __init__(self, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("heart.png")
        self.index = index
        self.pos = Vector2(10 + 20 * index, 10)  # 左上角
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.index >= player.hp:
            self.kill()

# 绘制大招图像


class Bomb(pygame.sprite.Sprite):
    def __init__(self, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bomb.png")
        self.index = index
        self.pos = Vector2(WIDTH - 10 - 20 * index, 10)  # 右上角
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.index >= player.boom:
            self.kill()

def get_player():
    return player

def get_player_re():
    return player_re

def get_player_ammo():
    return player_ammo

# 创造玩家
player = Player()
player_re = pygame.sprite.Group()
player_re.add(player)
for i in range(player.hp):
    hp = Heart(i)
    player_re.add(hp)
for i in range(player.boom):
    boom = Bomb(i)
    player_re.add(boom)
player_ammo = pygame.sprite.Group()