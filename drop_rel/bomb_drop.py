from .base_drop import BaseDrop
import pygame


# 大招点数
# 玩家触碰到后会增加bomb
class BombDrop(BaseDrop):
    def __init__(self, pos: pygame.Vector2, *groups: pygame.sprite.Group) -> None:
        super().__init__(pos, *groups)
        self.image = pygame.image.load("./images/bomb_drop.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.type = "bomb"

    def update(self, player_pos):
        if self.below_screen():
            self.kill()
        self.magnite(player_pos)
        del_v = self.speed
        self.pos += del_v
        self.rect.center = self.pos
