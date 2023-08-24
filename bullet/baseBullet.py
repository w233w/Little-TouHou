from pygame import Vector2, sprite
from pygame.sprite import Group


class BaseBullet(sprite.Sprite):
    def __init__(self, pos: Vector2, *groups: Group) -> None:
        super().__init__(*groups)
        self.pos = pos
