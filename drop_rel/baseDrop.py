from pygame import sprite, Vector2
from pygame.sprite import Group


class BaseDrop(sprite.Sprite):
    def __init__(self, pos: Vector2, *groups: Group) -> None:
        super().__init__(*groups)
        self.pos = pos
