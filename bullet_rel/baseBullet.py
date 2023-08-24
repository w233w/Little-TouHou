from pygame import Vector2, image, mask
from pygame.sprite import Sprite, Group
import pygame.time
from utils.const import *


class BaseBullet(Sprite):
    def __init__(self, pos: Vector2, *groups: Group) -> None:
        super().__init__(*groups)
        self.pos = pos
        self.image = image.load("./images/bullet.png")
        self.mask = mask.from_surface(self.image)
        self.ini_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(center=self.pos)

    def out_of_bound(self):
        return (
            self.rect.x < -4.5
            or self.rect.x > WIDTH + 4.5
            or self.rect.y < -4.5
            or self.rect.y > HEIGHT + 4.5
        )
