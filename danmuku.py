import pygame
import math
from pygame import Vector2
from pygame.sprite import Group
from utils.const import *
from player_rel import Player
from bullet_rel import NormalBullet, EllipseBullet, CubicBezierCurve, ButtonWave
from enemy_rel import BaseEnemy
from drop_rel import PowerDrop
from statistics import mean
from group_controller import *


# 血条
# test
def draw_hp_bar(pos, angle):
    # Center and (inner)radius of arc
    cx, cy, r, ir = pos[0], pos[1], 20, 17
    # Calculate the angle in degrees
    start = math.radians(135)
    # Start list of polygon points
    p = []
    for n in range(0, angle):
        x = cx + int(ir * math.cos((angle - n) * math.pi / 180 - start))
        y = cy + int(ir * math.sin((angle - n) * math.pi / 180 - start))
        p.append((x, y))
    for n in range(0, angle):
        x = cx + int(r * math.cos(n * math.pi / 180 - start))
        y = cy + int(r * math.sin(n * math.pi / 180 - start))
        p.append((x, y))
    # Draw
    if len(p) > 2:
        pygame.draw.polygon(screen, Red, p)


# 一号敌人
# 会不断发射两颗贝塞尔曲线弹幕
class Enemy_1(BaseEnemy):
    def __init__(self, pos: Vector2, max_hp: int, *groups: Group) -> None:
        super().__init__(pos, max_hp, *groups)
        self.image = pygame.image.load("./images/enemy_1.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.pos[1] < 200:
            self.pos += Vector2(0, 1)
        self.rect.center = self.pos
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.last_shot
        if time_pass / 1000 >= 1:
            self.last_shot = curr_time
            for i in range(1):
                for j in range(1):
                    CubicBezierCurve(self.pos, "l", i, j, bullets)
                    CubicBezierCurve(self.pos, "r", i, j, bullets)
        self.on_hit(player_ammo)
        if self.hp <= 0:
            self.kill()


# 二号敌人
# 会不断发射4颗普通子弹
class Enemy_2(BaseEnemy):
    def __init__(self, pos: Vector2, max_hp: int, *groups: Group) -> None:
        super().__init__(pos, max_hp, *groups)
        self.image = pygame.image.load("./images/enemy_2.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.pos[1] < 100:
            self.pos += Vector2(0, 1)
        self.rect.center = self.pos
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.last_shot
        if time_pass >= 1000:
            self.last_shot = curr_time
            for i in range(4):
                NormalBullet(self.pos, 4, i, 30, bullets)
        self.on_hit(player_ammo)
        if self.hp <= 0:
            PowerDrop(self.pos, drop_items)
            self.kill()


# 绘制血量图像
class Heart(pygame.sprite.Sprite):
    def __init__(self, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/heart.png")
        self.index = index
        self.pos = Vector2(10 + 20 * index, 10)  # 左上角
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.index >= player.sprite.hp:
            self.kill()


# 绘制大招图像
class Bomb(pygame.sprite.Sprite):
    def __init__(self, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/bomb.png")
        self.index = index
        self.pos = Vector2(WIDTH - 10 - 20 * index, 10)  # 右上角
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.index >= player.sprite.bomb:
            self.kill()


# 创造玩家相关内容
player.add(Player())
for i in range(player.sprite.hp):
    hp = Heart(i)
    player_re.add(hp)
for i in range(player.sprite.bomb):
    boom = Bomb(i)
    player_re.add(boom)

for i in range(1000):
    ButtonWave(None, 100, i, 1, -1, bullets)

for i in range(6):
    EllipseBullet(Vector2(200, 200), 6, i, 100, bullets)


# Init pygame & Crate screen
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("测试")
clock = pygame.time.Clock()
# 状态栏
# setting the pygame font style(1st parameter)
# and size of font(2nd parameter)
Font = pygame.font.SysFont("timesnewroman", 30)
try:
    Font = pygame.font.SysFont("得意黑斜体", 30)
except:
    Font = pygame.font.SysFont("timesnewroman", 30)
# 时间线
# 之后改用SQL
timeline = {
    "wave1": {"time": 3000, "done": False},
    "wave2": {"time": 15000, "done": False},
}

running = True

smooth_fps = [60] * 60

# 主体
while running:
    # 决定游戏刷新率
    clock.tick(FPS)
    delay = 1000 / clock.get_time()
    smooth_fps.append(delay)
    smooth_fps.pop(0)
    real_fps = round(mean(smooth_fps))
    Info1 = Font.render("YOU WIN!!", False, Red, White)
    Info2 = Font.render("NO BOOM!", False, Black, White)
    Info3 = Font.render(str(real_fps), False, Black, None)
    if (
        player.sprite.bomb > 0
        and pygame.time.get_ticks() - player.sprite.last_bomb >= 3000
    ):
        Info2 = Font.render("BOOM!", False, Black, White)
    # 点×时退出。。
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # 根据时间线创建敌人波次
    # 第一波
    if (
        pygame.time.get_ticks() > timeline["wave1"]["time"]
        and timeline["wave1"]["done"] == False
    ):
        for i in range(3):
            Enemy_1(Vector2(100 + 100 * i, 0), 20, enemys)
        for i in range(2):
            Enemy_2(Vector2(150 + 100 * i, 0), 10, enemys)
        timeline["wave1"]["done"] = True
    # 2
    if (
        pygame.time.get_ticks() > timeline["wave2"]["time"]
        and timeline["wave2"]["done"] == False
    ):
        for i in range(3):
            Enemy_1(Vector2(125 + 100 * i, 0), 20, enemys)
        for i in range(2):
            Enemy_2(Vector2(175 + 100 * i, 0), 10, enemys)
        timeline["wave2"]["done"] = True

    # 先铺背景再画sprites
    screen.fill(pygame.Color(BackgroundColor))
    if len(enemys.sprites()) == 0 and pygame.time.get_ticks() > 5000:
        screen.blit(Info1, (100, 0))
    screen.blit(Info2, (260, 0))
    screen.blit(Info3, (340, 50))
    # 更新sprites
    # 永远先更新玩家
    player.update()
    player_re.update()
    bullets.update(player)
    enemys.update()
    player_ammo.update()
    drop_items.update(player_pos=player.sprite.pos)  # 所有drop_item只有一个入参，即玩家位置
    # 不会有重叠，所以画不分先后
    player.draw(screen)
    bullets.draw(screen)
    player_re.draw(screen)
    enemys.draw(screen)
    player_ammo.draw(screen)
    drop_items.draw(screen)
    for en in enemys:
        if en.hp < en.max_hp:
            draw_hp_bar(en.pos, int(90 * en.hp / en.max_hp))
    # 更新画布
    pygame.display.flip()
