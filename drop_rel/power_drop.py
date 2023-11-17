from .base_drop import BaseDrop
import pygame


# 能量点数
# 玩家触碰到后会增加power
class PowerDrop(BaseDrop):
    def __init__(self, pos: pygame.Vector2, *groups: pygame.sprite.Group) -> None:
        super().__init__(pos, *groups)
        self.image = pygame.image.load("./images/power.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.type = "energy"

    def update(self, player):
        if self.below_screen():
            self.kill()
        self.magnitude(player)
        del_v = self.speed
        self.pos += del_v
        self.rect.center = self.pos
