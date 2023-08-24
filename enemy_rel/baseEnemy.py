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

    def on_hit(self, player_ammo):
        collide_sprites: list[PlayerShot] = sprite.spritecollide(
            self, player_ammo, True, sprite.collide_mask
        )
        for ammo in collide_sprites:
            self.hp -= ammo.power
