import pygame
import math
from pygame import Vector2
from pygame.sprite import Group
from utils.const import *
from player_rel import Player
from bullet_rel import BaseBullet
from enemy_rel import BaseEnemy
from drop_rel import PowerDrop
from statistics import mean
from group_controller import *


# 常规直线射弹
# 根据弹数向下方发射直线弹幕,pos是起始点位
class NormalBullet(BaseBullet):
    def __init__(self, pos: Vector2, total_num, index, angle, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.degree = angle / (total_num - 1) * self.index - angle / 2
        self.radian = math.radians(self.degree)

    def update(self):
        if self.out_of_bound():
            self.kill()
        del_x = math.sin(self.radian) * 2
        del_y = math.cos(self.radian) * 2
        del_v = Vector2(del_x, del_y)
        self.pos = self.pos + del_v
        self.rect.center = self.pos
        if self.pos.distance_to(player.sprite.pos) < 7:
            player.sprite.hp -= 1
            self.kill()
        if player.sprite.is_bomb:
            if self.pos.distance_to(player.sprite.pos) < 500:
                self.kill()


# 椭圆形环绕射弹
# ref:https://www.tiktok.com/@zakslab/video/6998525847296544006?_d=secCgYIASAHKAESPgo8SZe%2Fu4XTclFurcuEF0%2FkL147NxpLBJ2FCrJpWYTPhELOsZcu8ZkXTYFAOMEy7tP71iFB45MZ9OmFikv5GgA%3D&checksum=459a2b85cc6b6a50c31179982ede4c737029566aadb5979aa1f42e0c7bf8eb1b&language=en&preview_pb=0&sec_user_id=MS4wLjABAAAA-eranv3NR2ui2P79L5-HjN4oNRcWeeDCY1AD47zu6uxx1so4B-e4-vB6uOspMRIG&share_app_id=1233&share_item_id=6998525847296544006&share_link_id=4952D1C4-A915-4C20-9A87-2E550031C632&source=h5_m&timestamp=1629602102&tt_from=copy&u_code=dk0db1feehg16m&user_id=6991323682690466821&utm_campaign=client_share&utm_medium=ios&utm_source=copy&_r=1&is_copy_url=1&is_from_webapp=v1
# 几何中心在椭圆长轴和端州的焦点上
class EllipseBullet(BaseBullet):
    def __init__(self, pos: Vector2, total_num, index, radius, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.radius = radius
        self.radian = math.radians(360 / total_num * self.index)

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        # 计算动圆相对于原点的半径
        running_circle_radius = self.radius / 2
        # 计算动圆相对于原点的角度
        running_circle_radian = math.radians(360 * time_pass / 5000)
        # 利用角度计算位置
        running_circle_pos_x = self.pos[0] + running_circle_radius * math.sin(
            running_circle_radian
        )
        running_circle_pos_y = self.pos[1] + running_circle_radius * math.cos(
            running_circle_radian
        )
        # 动圆的圆心位置
        running_circle_pos = Vector2(running_circle_pos_x, running_circle_pos_y)

        # 计算子弹相对于圆心的半径
        bullets_radius = 0.75 * self.radius
        # 计算子弹相对于圆心的角度
        bullets_radian = math.radians(360 * time_pass / 3000) + self.radian
        # 利用角度计算位置
        bullets_pos_x = running_circle_pos[0] + bullets_radius * math.sin(
            bullets_radian
        )
        bullets_pos_y = running_circle_pos[1] + bullets_radius * math.cos(
            bullets_radian
        )
        # 子弹的坐标
        bullet_pos = Vector2(bullets_pos_x, bullets_pos_y)

        self.rect.center = bullet_pos
        if self.pos.distance_to(player.sprite.pos) < 7:
            player.sprite.hp -= 1
            self.kill()
        if player.sprite.is_bomb:
            if self.pos.distance_to(player.sprite.pos) < 500:
                self.kill()


# 开花型环绕子弹（一圈）
# 几何中心在椭圆长轴的一个端点上
# total_num表示每圈一共有几个，index代表环上的第几个，group表示层数，pos表示子弹射出的位置
class AtomBullet(BaseBullet):
    def __init__(self, pos: Vector2, total_num, index, group=0, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.group = group
        self.degree = 360 / total_num * self.index

    def update(self):
        self.degree += 2 + self.group * 2
        radian = math.radians(self.degree)
        del_x = math.sin(radian) * 2
        del_y = math.cos(radian) * 2
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        if self.pos.distance_to(player.sprite.pos) < 7:
            player.sprite.hp -= 1
            self.kill()
        if player.sprite.is_bomb:
            if self.pos.distance_to(player.sprite.pos) < 500:
                self.kill()
        self.rect.center = self.pos


# 蛇形弹幕（单个）
# 数个子弹从屏幕正上方落下，运动时左右摆动，遵从正弦函数曲线。
# total_num共有几个子弹下落，index代表从左数的第几个，speed代表速度和幅度
class SnakeBullet(BaseBullet):
    def __init__(
        self, pos: Vector2, total_num, index=0, speed=1, *groups: Group
    ) -> None:
        self.pos = Vector2(self.x, HEADLINE)
        super().__init__(pos, *groups)
        self.x = (WIDTH / (total_num - 1)) * index
        self.speed = speed

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        del_x = math.sin(2 * math.pi * time_pass / (1000 * self.speed))
        del_y = self.speed
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        self.rect.center = self.pos
        if player.sprite.is_bomb:
            if self.pos.distance_to(player.sprite.pos) < 500:
                self.kill()


# 三次贝塞尔曲线弹幕（自机狙）
# side决定子弹射出的方向，index和group决定了子弹运动的幅度，index决定宽度，group决定高度，pos是子弹射出的位置
# 子弹射出后会追踪射出时玩家的位置，仅一次。玩家在平行移动后理应可以轻松躲开子弹。
class CubicBezierCurve(BaseBullet):
    def __init__(self, pos: Vector2, side, index=0, group=0, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.p1 = Vector2(pos)
        if side == "l":
            self.p2 = Vector2(200 - 30 * group, 100 - 30 * group)
            self.p3 = Vector2(100 - 70 * index, 200 - 30 * index)
        else:
            self.p2 = Vector2(200 + 30 * group, 100 - 30 * group)
            self.p3 = Vector2(300 + 70 * index, 200 - 30 * index)
        self.p4 = Vector2(player.sprite.pos)

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        t = time_pass / 3000
        sec1 = ((1 - t) ** 3) * self.p1
        sec2 = 3 * t * ((1 - t) ** 2) * self.p2
        sec3 = 3 * (1 - t) * (t**2) * self.p3
        sec4 = (t**3) * self.p4
        pos = sec1 + sec2 + sec3 + sec4
        self.rect.center = pos
        if self.out_of_bound():
            self.kill()
        if pos.distance_to(player.sprite.pos) < 7:
            player.sprite.hp -= 1
            self.kill()
        if player.sprite.is_bomb:
            if pos.distance_to(player.sprite.pos) < 500:
                self.kill()


# 波浪形弹幕
# 子弹在板底以海浪型波动
# total_num是密度，index可以大于total_num（如果需要平移的话）,shift是偏移量
# total_num应该是一个大数字，否则不会有连贯的视觉效果
class ButtonWave(BaseBullet):
    def __init__(
        self, pos: Vector2, total_num, index, height=1, shift=0, *groups: Group
    ) -> None:
        self.x = (WIDTH / (total_num - 1)) * index
        pos = Vector2(self.x, HEIGHT + 10)
        super().__init__(pos, *groups)
        self.index = index
        self.x = (WIDTH / (total_num - 1)) * index
        self.height = height
        self.shift = shift

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        del_x = self.shift
        del_y = self.height * math.sin(
            2 * math.pi * time_pass / (1500) + self.index / 3
        )
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        self.rect.center = self.pos
        if self.pos[0] <= 0 and self.shift < 0:
            self.kill()
        if self.pos[0] >= WIDTH and self.shift > 0:
            self.kill()


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
    bullets.update()
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
