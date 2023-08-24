from pygame import sprite, time, Vector2
from pygame.sprite import Group


class BaseEnemy(sprite.Sprite):
    def __init__(self, pos: Vector2, *groups: Group) -> None:
        super().__init__(*groups)
        self.ini_time = time.get_ticks()
        self.last_shot = self.ini_time
        self.pos = pos
