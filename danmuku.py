import pygame
import math
import json
from pygame import Vector2
from utils.const import *
from utils.debug import draw_hp_bar
from player_rel import Player
from enemy_rel import BezierEnemy, NormalEnemy  #  有用，详见124行
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
try:
    Font = pygame.font.SysFont("得意黑斜体", 30)
except:
    Font = pygame.font.SysFont("timesnewroman", 30)
# 时间线
with open("./utils/timeline.json") as f:
    text = "".join(f.readlines())
    timeline = json.loads(text)

smooth_fps = [60] * 60

# 主体
while running := True:
    # 决定游戏刷新率
    clock.tick(FPS)
    delay = 1000 / clock.get_time()
    smooth_fps.append(delay)
    smooth_fps.pop(0)
    real_fps = round(mean(smooth_fps))
    win_info = Font.render("YOU WIN!!", False, Red, White)
    fps_text = Font.render(f"FPS: {real_fps}", False, Black, None)
    # 点×时退出。。
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # 根据时间线创建敌人波次
    if timeline:
        next_wave = timeline[0]
        if pygame.time.get_ticks() >= next_wave["time"]:
            wave_enemys = next_wave["enemys"]
            for enemy_name, enemy_prop in wave_enemys.items():
                for i in range(enemy_prop["num"]):
                    pos_x, pos_y = enemy_prop["pos"]
                    inter_x, inter_y = enemy_prop["interval"]
                    hp = enemy_prop["hp"]
                    spawning_enemy_class = globals()[enemy_name]
                    spawning_enemy_class(
                        Vector2(pos_x + inter_x * i, pos_y + inter_y * i), hp, enemys
                    )
            timeline.pop(0)
    else:
        screen.blit(win_info, (100, 0))

    # 先铺背景再画sprites
    screen.fill(pygame.Color(BackgroundColor))
    screen.blit(fps_text, (310, 50))
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
            draw_hp_bar(screen, en.pos, int(90 * en.hp / en.max_hp))
    # 更新画布
    pygame.display.flip()
