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

# 常规直线射弹
# 根据弹数向下方发射直线弹幕,pos是起始点位


class Normal_Bullet(pygame.sprite.Sprite):
    def __init__(self, total_num, index, angle, pos=Vector2(200, 200)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect(center=pos)
        self.index = index
        self.pos = pos
        self.degree = angle / (total_num - 1) * self.index - angle / 2
        self.radian = math.radians(self.degree)

    def update(self):
        del_x = math.sin(self.radian) * 2
        del_y = math.cos(self.radian) * 2
        del_v = Vector2(del_x, del_y)
        self.pos = self.pos + del_v
        self.rect.center = self.pos
        if self.pos.distance_to(player.pos) < 7:
            player.hp -= 1
            self.kill()
        if player.is_boom:
            if self.pos.distance_to(player.pos) < 500:
                self.kill()


# 椭圆形环绕射弹
# ref:https://www.tiktok.com/@zakslab/video/6998525847296544006?_d=secCgYIASAHKAESPgo8SZe%2Fu4XTclFurcuEF0%2FkL147NxpLBJ2FCrJpWYTPhELOsZcu8ZkXTYFAOMEy7tP71iFB45MZ9OmFikv5GgA%3D&checksum=459a2b85cc6b6a50c31179982ede4c737029566aadb5979aa1f42e0c7bf8eb1b&language=en&preview_pb=0&sec_user_id=MS4wLjABAAAA-eranv3NR2ui2P79L5-HjN4oNRcWeeDCY1AD47zu6uxx1so4B-e4-vB6uOspMRIG&share_app_id=1233&share_item_id=6998525847296544006&share_link_id=4952D1C4-A915-4C20-9A87-2E550031C632&source=h5_m&timestamp=1629602102&tt_from=copy&u_code=dk0db1feehg16m&user_id=6991323682690466821&utm_campaign=client_share&utm_medium=ios&utm_source=copy&_r=1&is_copy_url=1&is_from_webapp=v1
# 几何中心在椭圆长轴和端州的焦点上

class Ellipse_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, total_num, index, radius):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect(center=pos)
        self.index = index
        self.radius = radius
        self.pos = pos
        self.ini_time = pygame.time.get_ticks()
        self.radian = math.radians(360 / total_num * self.index)

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        # 计算动圆相对于原点的半径
        running_circle_radius = self.radius / 2
        # 计算动圆相对于原点的角度
        running_circle_radian = math.radians(360 * time_pass / 5000)
        # 利用角度计算位置
        running_circle_pos_x = self.pos[0] + running_circle_radius * math.sin(running_circle_radian)
        running_circle_pos_y = self.pos[1] + running_circle_radius * math.cos(running_circle_radian)
        # 动圆的圆心位置
        running_circle_pos = Vector2(running_circle_pos_x, running_circle_pos_y)

        # 计算子弹相对于圆心的半径
        bullets_radius = 0.75 * self.radius
        # 计算子弹相对于圆心的角度
        bullets_radian = math.radians(360 * time_pass / 3000) + self.radian
        # 利用角度计算位置
        bullets_pos_x = running_circle_pos[0] + bullets_radius * math.sin(bullets_radian)
        bullets_pos_y = running_circle_pos[1] + bullets_radius * math.cos(bullets_radian)
        # 子弹的坐标
        bullet_pos = Vector2(bullets_pos_x, bullets_pos_y)

        self.rect.center = bullet_pos
        if self.pos.distance_to(player.pos) < 7:
            player.hp -= 1
            self.kill()
        if player.is_boom:
            if self.pos.distance_to(player.pos) < 500:
                self.kill()

# 开花型环绕子弹（一圈）
# 几何中心在椭圆长轴的一个端点上
# total_num表示每圈一共有几个，index代表环上的第几个，group表示层数，pos表示子弹射出的位置


class Atom_Bullet(pygame.sprite.Sprite):
    def __init__(self, total_num, index, group=0, pos=Vector2(200, 200)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect(center=pos)
        self.index = index
        self.group = group
        self.pos = pos
        self.degree = 360 / total_num * self.index

    def update(self):
        self.degree += 2 + self.group * 2
        radian = math.radians(self.degree)
        del_x = math.sin(radian) * 2
        del_y = math.cos(radian) * 2
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        if self.pos.distance_to(player.pos) < 7:
            player.hp -= 1
            self.kill()
        if player.is_boom:
            if self.pos.distance_to(player.pos) < 500:
                self.kill()
        self.rect.center = self.pos

# 蛇形弹幕（单个）
# 数个子弹从屏幕正上方落下，运动时左右摆动，遵从正弦函数曲线。
# total_num共有几个子弹下落，index代表从左数的第几个，speed代表速度和幅度


class Snake_Bullet(pygame.sprite.Sprite):
    def __init__(self, total_num, index=0, speed=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.x = (WIDTH / (total_num-1)) * index
        self.pos = Vector2(self.x, HEADLINE)
        self.rect = self.image.get_rect(center=self.pos)
        self.ini_time = pygame.time.get_ticks()
        self.speed = speed

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        del_x = math.sin(2 * math.pi * time_pass/(1000*self.speed))
        del_y = self.speed
        del_v = Vector2(del_x, del_y)
        self.pos += del_v
        self.rect.center = self.pos
        if player.is_boom:
            if self.pos.distance_to(player.pos) < 500:
                self.kill()

# 三次贝塞尔曲线弹幕（自机狙）
# side决定子弹射出的方向，index和group决定了子弹运动的幅度，index决定宽度，group决定高度，pos是子弹射出的位置
# 子弹射出后会追踪射出时玩家的位置，仅一次。玩家在平行移动后理应可以轻松躲开子弹。


class Cubic_Bezier_Curve(pygame.sprite.Sprite):
    def __init__(self, side, index=0, group=0, pos=Vector2(200, 200)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect(center=pos)
        self.ini_time = pygame.time.get_ticks()
        self.p1 = Vector2(pos)
        if side == 'l':
            self.p2 = Vector2(200 - 30 * group, 100 - 30 * group)
            self.p3 = Vector2(100 - 70 * index, 200 - 30 * index)
        else:
            self.p2 = Vector2(200 + 30 * group, 100 - 30 * group)
            self.p3 = Vector2(300 + 70 * index, 200 - 30 * index)
        self.p4 = Vector2(player.pos)

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        t = time_pass / 3000
        sec1 = ((1 - t) ** 3) * self.p1
        sec2 = 3 * t * ((1 - t) ** 2) * self.p2
        sec3 = 3 * (1 - t) * (t ** 2) * self.p3
        sec4 = (t ** 3) * self.p4
        pos = sec1 + sec2 + sec3 + sec4
        self.rect.center = pos
        if self.rect.x < -4.5 or self.rect.x > WIDTH + 4.5 or self.rect.y < -4.5 or self.rect.y > HEIGHT + 4.5:
            self.kill()
        if pos.distance_to(player.pos) < 7:
            player.hp -= 1
            self.kill()
        if player.is_boom:
            if pos.distance_to(player.pos) < 500:
                self.kill()

# 波浪形弹幕
# 子弹在板底以海浪型波动
# total_num是密度，index可以大于total_num（如果需要平移的话）,shift是偏移量
# total_num应该是一个大数字，否则不会有连贯的视觉效果


class Button_Wave(pygame.sprite.Sprite):
    def __init__(self, total_num, index, height=1, shift=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.index = index
        self.x = (WIDTH / (total_num-1)) * index
        self.pos = Vector2(self.x, HEIGHT + 10)
        self.rect = self.image.get_rect(center=self.pos)
        self.ini_time = pygame.time.get_ticks()
        self.height = height
        self.shift = shift

    def update(self):
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        del_x = self.shift
        del_y = self.height * \
            math.sin(2 * math.pi * time_pass/(1500) + self.index / 3)
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
        x = cx + int(ir * math.cos((angle - n) *
                                   math.pi/180 - start))
        y = cy + int(ir * math.sin((angle - n) *
                                   math.pi/180-start))
        p.append((x, y))
    for n in range(0, angle):
        x = cx + int(r * math.cos(n*math.pi/180 - start))
        y = cy + int(r * math.sin(n*math.pi/180 - start))
        p.append((x, y))
    # Draw
    if len(p) > 2:
        pygame.draw.polygon(screen, Red, p)


# 一号敌人
# 会不断发射两颗贝塞尔曲线弹幕

class Enemy_1(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy_1.png")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.ini_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.maxhp = 20
        self.hp = self.maxhp

    def update(self):
        if self.pos[1] < 200:
            self.pos += Vector2(0, 1)
        self.rect.center = self.pos
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.last_shot
        if time_pass / 1000 >= 1:
            self.last_shot = pygame.time.get_ticks()
            for i in range(1):
                for j in range(1):
                    curve_l = Cubic_Bezier_Curve('l', i, j, self.pos)
                    bullets.add(curve_l)
                    curve_r = Cubic_Bezier_Curve('r', i, j, self.pos)
                    bullets.add(curve_r)
        for ammo in player_ammo:
            if self.pos.distance_to(ammo.pos) < 7:
                ammo.kill()
                self.hp -= player.power
        if self.hp <= 0:
            self.kill()

# 二号敌人
# 会不断发射4颗普通子弹


class Enemy_2(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy_1.png")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.ini_time = pygame.time.get_ticks()
        self.maxhp = 10
        self.hp = self.maxhp

    def update(self):
        if self.pos[1] < 100:
            self.pos += Vector2(0, 1)
        self.rect.center = self.pos
        curr_time = pygame.time.get_ticks()
        time_pass = curr_time - self.ini_time
        if time_pass % 1000 <= 16 and time_pass >= 1000:
            for i in range(4):
                normal = Normal_Bullet(4, i, 30, self.pos)
                bullets.add(normal)
        for ammo in player_ammo:
            if self.pos.distance_to(ammo.pos) < 7:
                ammo.kill()
                self.hp -= player.power
        if self.hp <= 0:
            items.add(Power_Node(self.pos))
            self.kill()

# 能量点数
# 玩家触碰到后会增加power


class Power_Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.ini_time = pygame.time.get_ticks()

    def update(self):
        del_v = Vector2(0, 1)
        self.pos += del_v
        self.rect.center = self.pos
        if self.pos.distance_to(player.pos) < 7:
            player.power += 0.5
            self.kill()

# 生命点数
# 玩家触碰到后会增加power


class Hp_Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.ini_time = pygame.time.get_ticks()

    def update(self):
        del_v = Vector2(0, 1)
        self.pos += del_v
        self.rect.center = self.pos
        if self.pos.distance_to(player.pos) < 7 and player.hp < 6:
            player.hp += 1
            self.kill()

# 大招点数
# 玩家触碰到后会增加power


class Bomb_Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.ini_time = pygame.time.get_ticks()

    def update(self):
        del_v = Vector2(0, 1)
        self.pos += del_v
        self.rect.center = self.pos
        if self.pos.distance_to(player.pos) < 7 and player.boom < 4:
            player.boom += 1
            self.kill()

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

    # 自机控制
    # 返回的值决定了速度


    def _player_control(self):
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

    def update(self):
        # boom只有一帧，update前先结束掉
        self.is_boom = False
        # 死亡判定
        if self.hp <= 0:
            self.kill()
            return
        # 攻击力不会大于五
        if self.power > 5:
            self.power = 5
        # 移动
        self.pos += self._player_control()
        self.rect.center = self.pos
        current_time = pygame.time.get_ticks()
        # 根据间隔检测是否能打出子弹
        if pygame.key.get_pressed()[pygame.K_z] == 1 and current_time - self.last_shoot >= 200:
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

enemy = pygame.sprite.Group()

# 创造初始子弹
bullets = pygame.sprite.Group()
# for i in range(3):
#     for j in range(4):
#         atom = Atom_Bullet(3, i, j, (200, 200))
#         bullets.add(atom)

for i in range(1000):
    wave = Button_Wave(100, i, 1, -1)
    bullets.add(wave)

for i in range(6):
    atom = Ellipse_Bullet(Vector2(200,200), 6, i, 100)
    bullets.add(atom)

items = pygame.sprite.Group()

# Init pygame & Crate screen
pygame.init()
screen = pygame.display.set_mode(SIZE)
gameplay = pygame.Surface((10, 10), 0, screen)
pygame.display.set_caption("测试")
clock = pygame.time.Clock()
# 状态栏
# setting the pygame font style(1st parameter)
# and size of font(2nd parameter)
Font = pygame.font.SysFont('timesnewroman',  30)

# 时间线
# 之后改用SQL
timeline = {
            'wave1': {'time': 3000, 'do': False},
            'wave2': {'time': 15000, 'do': False}
            }

running = True

count17 = 0
countall = 0

# 主体
while running:
    # 决定游戏刷新率
    clock.tick(FPS)
    delay = int(1000 / clock.get_time())
    Info1 = Font.render("YOU WIN!!", False, Red, White)
    Info2 = Font.render("NO BOOM!", False, Black, White)
    Info3 = Font.render(str(delay), False, White, Black)
    if player.boom > 0 and pygame.time.get_ticks() - player.last_boom >= 3000:
        Info2 = Font.render("BOOM!", False, Black, White)
    # 点×时退出。。
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    # 根据时间线创建敌人波次
    # 第一波
    if pygame.time.get_ticks() > timeline['wave1']['time'] and timeline['wave1']['do'] == False:
        for i in range(3):
            enemy_1 = Enemy_1(Vector2(100 + 100 * i, 0))
            enemy.add(enemy_1)
        for i in range(2):
            enemy_2 = Enemy_2(Vector2(150 + 100 * i, 0))
            enemy.add(enemy_2)
        timeline['wave1']['do'] = True
    # 2
    if pygame.time.get_ticks() > timeline['wave2']['time'] and timeline['wave2']['do'] == False and timeline['wave1']['do'] == True:
        for i in range(3):
            enemy_1 = Enemy_1(Vector2(125 + 100 * i, 0))
            enemy.add(enemy_1)
        for i in range(2):
            enemy_2 = Enemy_2(Vector2(175 + 100 * i, 0))
            enemy.add(enemy_2)
        timeline['wave2']['do'] = True

    # 先铺背景再画sprites
    screen.fill(pygame.Color(BackgroundColor))
    gameplay.fill(pygame.Color(White))
    if len(enemy.sprites()) == 0 and pygame.time.get_ticks() > 5000:
        screen.blit(Info1, (100, 0))
    screen.blit(Info2, (260, 0))
    screen.blit(Info3, (260, 50))
    # 更新sprites
    # 永远先更新玩家
    player_re.update()
    bullets.update()
    enemy.update()
    player_ammo.update()
    items.update()
    # 画不分先后
    bullets.draw(screen)
    player_re.draw(screen)
    enemy.draw(screen)
    player_ammo.draw(screen)
    items.draw(screen)
    for en in enemy:
        draw_hp_bar(en.pos, int(90*en.hp/en.maxhp))
    # 更新画布
    pygame.display.flip()
