from pygame import Vector2, image, mask
from pygame.sprite import Sprite, Group
import pygame.time
from utils.const import *


# 敌机子弹类的基类，注意这个类每个实例一般表示一个子弹的实体。
class BaseBullet(Sprite):
    def __init__(self, pos: Vector2, *groups: Group) -> None:
        super().__init__(*groups)
        self.pos = Vector2(pos)
        self.image = image.load("./images/bullet.png")
        self.mask = mask.from_surface(self.image)
        self.ini_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(center=self.pos)

    def out_of_bound(self, img_bound: float = 4.5):
        return (
            self.pos.x < -img_bound or self.pos.x > WIDTH + img_bound,
            self.pos.y < -img_bound or self.pos.y > HEIGHT + img_bound,
        )
