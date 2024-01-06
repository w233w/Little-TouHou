from .precise_bullet import PreciseBullet
from pygame import Vector2
from pygame.sprite import Group
import numpy as np


# 子弹会从右上角按一定间隔出发，终点在（30，500）。
# 路径是从右上到左下的二次曲线
# 路径会穿过左边缘，再从右边缘回来
# 函数为y=K(x-30)^2 + 100
######################
#  import numpy as np
#  import matplotlib.pyplot as plt
#
#  fig = plt.figure(figsize=(10, 10))
#  plt.ylim(0, 600)
#  plt.xlim(0, 400)
#
#  Ks = (0.00085, 0.00105, 0.00130, 0.00160, 0.00195, 0.00235, 0.00285)
#  c = ('r', '#ff7f0e', 'y', 'g', 'c', 'b', 'm')
#
#  for i, k in enumerate(Ks):
#      x1 = np.linspace(30, 400, 800, endpoint=False)
#      x2= np.linspace(400, 800, 800, endpoint=False)
#      y1 = (k * (x1 - 30) ** 2 + 100)
#      y2 = (k * (x2 - 30) ** 2 + 100)
#      plt.plot(x1, y1, color=c[i])
#      plt.plot(x2-400, y2, color=c[i])
#  plt.show()
########################
class SP_one_controller:
    Ks = (0.00085, 0.00105, 0.00130, 0.00160, 0.00195, 0.00235, 0.00285)

    def __init__(self, *groups: Group) -> None:
        self.speed = 100
        self.bullets_route: list[tuple[Vector2]] = []
        for i in range(40):
            for j in range(7):
                x = np.linspace(30 + i * 20, 400 + i * 20, self.speed, endpoint=False)
                y = SP_one_controller.Ks[j] * (x - 50) ** 2 + 100
                route: list[Vector2] = []
                for a in range(self.speed):
                    route.append(Vector2(x[a] % 400, 600 - y[a]))
                route.reverse()
                self.bullets_route.append(tuple(route))
        for b_route in self.bullets_route:
            PreciseBullet(b_route, *groups)
