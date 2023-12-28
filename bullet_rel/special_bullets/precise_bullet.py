from pygame import Vector2, image, mask
from pygame.sprite import Sprite, Group
import pygame.time
from utils.const import *


# 特殊的敌机子弹类的基类，注意这个类每个实例一般表示一个子弹的实体。
# 这种子弹只会根据入参的轨迹移动
# route是由坐标构成的列表
class PreciseBullet(Sprite):
    def __init__(self, route: tuple[Vector2], *groups: Group) -> None:
        super().__init__(*groups)
        self.route = route
        self.step = 0
        self.pos = self.route[self.step]
        self.image = image.load("./images/bullet.png")
        self.mask = mask.from_surface(self.image)
        self.ini_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos = self.route[self.step]
        self.rect.center = self.pos
