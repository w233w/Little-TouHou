from pygame import sprite, image, Vector2
from pygame.sprite import Group


# 玩家子弹
class PlayerShoot(sprite.Sprite):
    def __init__(self, power: int, index: int, init_pos: Vector2, *groups: Group):
        super().__init__(*groups)
        self.image = image.load("./images/ammo.png")
        self.power = power
        # 根据power决定额外子弹的数量和位置
        if power <= 2:
            self.pos = Vector2(init_pos)
        elif power <= 4:
            self.pos = Vector2(init_pos) + Vector2(-2 + index * 4, 0)
        else:
            del_y = 0
            if index != 1:
                del_y = 1
            self.pos = Vector2(init_pos) + Vector2(-4 + index * 4, del_y)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += Vector2(0, -4)  # 子弹速度
        self.rect.center = self.pos
        if (self.pos.y) < -1:  # 离开屏幕后不再更新位置
            self.kill()
