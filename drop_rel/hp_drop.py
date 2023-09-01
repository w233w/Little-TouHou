from .base_drop import BaseDrop
import pygame


# 生命点数
# 玩家触碰到后会增加hp
class HPDrop(BaseDrop):
    def __init__(self, pos: pygame.Vector2, *groups: pygame.sprite.Group) -> None:
        super().__init__(pos, *groups)
        self.image = pygame.image.load("./images/hp_drop.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.type = "hp"

    def update(self, player):
        if self.below_screen():
            self.kill()
        self.magnite(player)
        del_v = self.speed
        self.pos += del_v
        self.rect.center = self.pos
