from pygame import sprite
from pygame.sprite import Group


class BaseBullet(sprite.Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
