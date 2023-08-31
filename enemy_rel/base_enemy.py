from typing import Any
from pygame import sprite, time, Vector2
from pygame.sprite import Group
from player_rel import PlayerShot


class BaseEnemy(sprite.Sprite):
    def __init__(self, pos: Vector2, max_hp: int, *groups: Group) -> None:
        super().__init__(*groups)
        self.ini_time = time.get_ticks()
        self.last_shot = self.ini_time
        self.pos = pos
        self.max_hp = max_hp
        self.hp = self.max_hp

    def update(self, op: sprite.Group, *args: Any, **kwargs: Any) -> None:  # as dummy
        if sprite.spritecollide(self, op, False, sprite.collide_mask):
            self.kill()

    def on_hit(self, player_ammo, defence: int = 0):
        collide_sprites: list[PlayerShot] = sprite.spritecollide(
            self, player_ammo, True, sprite.collide_mask
        )
        for ammo in collide_sprites:
            self.hp -= max(0, ammo.power - defence)
        del collide_sprites[:]

    def on_time(self):
        self.hp -= 1
