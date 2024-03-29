from pygame import sprite, Vector2
from pygame.sprite import Group
from utils.const import *


class BaseDrop(sprite.Sprite):
    def __init__(self, pos: Vector2, *groups: Group) -> None:
        super().__init__(*groups)
        self.pos = pos
        self.speed = Vector2(0, 1)

    def below_screen(self):
        return self.pos.y > HEIGHT + 5

    def magnitude(self, player):
        player_pos = player.sprite.pos
        if 1 < self.pos.distance_to(player_pos) < 36:
            self.speed = (player_pos - self.pos).normalize()
        else:
            self.speed = Vector2(0, 1)
