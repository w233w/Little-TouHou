from .base_bullet import BaseBullet
import math
from pygame import Vector2, time
from pygame.sprite import Group


# 椭圆形环绕射弹
# ref:https://www.tiktok.com/@zakslab/video/6998525847296544006?_d=secCgYIASAHKAESPgo8SZe%2Fu4XTclFurcuEF0%2FkL147NxpLBJ2FCrJpWYTPhELOsZcu8ZkXTYFAOMEy7tP71iFB45MZ9OmFikv5GgA%3D&checksum=459a2b85cc6b6a50c31179982ede4c737029566aadb5979aa1f42e0c7bf8eb1b&language=en&preview_pb=0&sec_user_id=MS4wLjABAAAA-eranv3NR2ui2P79L5-HjN4oNRcWeeDCY1AD47zu6uxx1so4B-e4-vB6uOspMRIG&share_app_id=1233&share_item_id=6998525847296544006&share_link_id=4952D1C4-A915-4C20-9A87-2E550031C632&source=h5_m&timestamp=1629602102&tt_from=copy&u_code=dk0db1feehg16m&user_id=6991323682690466821&utm_campaign=client_share&utm_medium=ios&utm_source=copy&_r=1&is_copy_url=1&is_from_webapp=v1
# 几何中心在椭圆长轴和端州的焦点上
class EllipseBullet(BaseBullet):
    def __init__(self, pos: Vector2, total_num, index, radius, *groups: Group) -> None:
        super().__init__(pos, *groups)
        self.index = index
        self.radius = radius
        self.radian = math.radians(360 / total_num * self.index)

    def update(self, player):
        curr_time = time.get_ticks()
        time_pass = curr_time - self.ini_time
        # 计算动圆相对于原点的半径
        running_circle_radius = self.radius / 2
        # 计算动圆相对于原点的角度
        running_circle_radian = math.radians(360 * time_pass / 5000)
        # 利用角度计算位置
        running_circle_pos_x = self.pos[0] + running_circle_radius * math.sin(
            running_circle_radian
        )
        running_circle_pos_y = self.pos[1] + running_circle_radius * math.cos(
            running_circle_radian
        )
        # 动圆的圆心位置
        running_circle_pos = Vector2(running_circle_pos_x, running_circle_pos_y)

        # 计算子弹相对于圆心的半径
        bullets_radius = 0.75 * self.radius
        # 计算子弹相对于圆心的角度
        bullets_radian = math.radians(360 * time_pass / 3000) + self.radian
        # 利用角度计算位置
        bullets_pos_x = running_circle_pos[0] + bullets_radius * math.sin(
            bullets_radian
        )
        bullets_pos_y = running_circle_pos[1] + bullets_radius * math.cos(
            bullets_radian
        )
        # 子弹的坐标
        bullet_pos = Vector2(bullets_pos_x, bullets_pos_y)

        self.rect.center = bullet_pos
        if self.pos.distance_to(player.sprite.pos) < 7:
            player.sprite.hp -= 1
            self.kill()
        if player.sprite.is_bomb:
            if self.pos.distance_to(player.sprite.pos) < 500:
                self.kill()
