import pygame
import json
from pygame import Vector2
from utils.const import *
from utils.debug import draw_hp_bar
from player_rel import Player
from enemy_rel import *
from statistics import mean
from group_controller import *


# 创造玩家相关内容
player.add(Player())

# Init pygame & Crate screen
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("测试")
clock = pygame.time.Clock()
# 状态栏
# setting the pygame font style(1st parameter)
# and size of font(2nd parameter)
if "得意黑斜体" in pygame.font.get_fonts():
    Font = pygame.font.SysFont("得意黑斜体", 30)
else:
    Font = pygame.font.SysFont("timesnewroman", 30)
win_info = Font.render("YOU WIN!!", True, Red, None)
lose_info = Font.render("YOU LOSE", True, Red, None)
welcome = Font.render("Little-Touhou", True, Red, None)
start_info = Font.render("Click to start", True, Black, None)
restart_info = Font.render("Click to restart", True, Black, None)

smooth_fps = [60.0] * 60

state = 0  # 0:开机; 1：游戏中; 2：replay
last_wave = 0

# 主体
while running := True:
    # 决定游戏刷新率
    clock.tick(FPS)
    delay = 1000 / clock.get_time()
    smooth_fps.append(delay)
    smooth_fps.pop(0)
    real_fps = round(mean(smooth_fps))
    fps_text = Font.render(f"FPS: {real_fps}", True, Black, None)
    # 点×时退出。。
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if state == 0:
        screen.fill(pygame.Color(BackgroundColor))
        screen.blit(welcome, (180, 50))
        screen.blit(start_info, (120, 400))
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            # 时间线
            with open("./utils/timeline.json") as f:
                text = f.read()
                timeline = json.loads(text)
            last_wave = pygame.time.get_ticks()  # start from 0
            state = 1
    elif state == 1:
        if player.sprite.hp <= 0:
            state = 2
        # 先铺背景
        screen.fill(pygame.Color(BackgroundColor))
        screen.blit(fps_text, (310, 50))

        # 根据时间线创建敌人波次
        if timeline:
            next_wave = timeline[0]
            if (
                not next_wave["boss"]
                and pygame.time.get_ticks() - next_wave["time"] >= last_wave
            ):
                wave_enemys = next_wave["enemys"]
                for enemy_name, enemy_prop in wave_enemys.items():
                    for i in range(enemy_prop["num"]):
                        pos_x, pos_y = enemy_prop["pos"]
                        inter_x, inter_y = enemy_prop["interval"]
                        hp = enemy_prop["hp"]
                        spawning_enemy_class: BaseEnemy = globals()[enemy_name]
                        spawning_enemy_class(
                            Vector2(pos_x + inter_x * i, pos_y + inter_y * i),
                            hp,
                            enemys,
                        )
                timeline.pop(0)
                last_wave = pygame.time.get_ticks()
            elif next_wave["boss"] and len(enemys.sprites()) == 0:
                wave_enemys = next_wave["enemys"]
                for enemy_name, enemy_prop in wave_enemys.items():
                    pos_x, pos_y = enemy_prop["pos"]
                    time_wait = next_wave["time"]
                    spawning_enemy_class = globals()[enemy_name]
                    spawning_enemy_class(Vector2(pos_x, pos_y), time_wait, enemys)
                timeline.pop(0)
                last_wave = pygame.time.get_ticks()
        elif len(enemys.sprites()) == 0:
            screen.blit(win_info, (200, 100))
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                # 时间线
                with open("./utils/timeline.json") as f:
                    text = f.read()
                    timeline = json.loads(text)
                last_wave = pygame.time.get_ticks()  # start from 0
                state = 0

        # 更新sprites
        # 永远先更新玩家
        player.update()
        player_re.update()
        bullets.update()
        enemys.update()
        player_ammo.update()
        drop_items.update(player)  # 所有drop_item只有一个入参，即玩家位置
        # 不会有重叠，所以画不分先后
        player.draw(screen)
        bullets.draw(screen)
        player_re.draw(screen)
        enemys.draw(screen)
        player_ammo.draw(screen)
        drop_items.draw(screen)
        for en in enemys:
            if en.hp < en.max_hp:
                draw_hp_bar(screen, en.pos, int(90 * en.hp / en.max_hp), Red)
    elif state == 2:
        # screen.fill(pygame.Color(BackgroundColor))
        screen.blit(lose_info, (180, 50))
        screen.blit(restart_info, (120, 400))
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            # 时间线
            with open("./utils/timeline.json") as f:
                text = f.read()
                timeline = json.loads(text)
            last_wave = pygame.time.get_ticks()  # start from 0
            state = 1
            player_re.empty()
            bullets.empty()
            enemys.empty()
            player_ammo.empty()
            drop_items.empty()
            player.add(Player())
    # 更新画布
    pygame.display.flip()
