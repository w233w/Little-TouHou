from .base_enemy import BaseEnemy
from .bezier_enemy import BezierEnemy
from .normal_enemy import NormalEnemy
from .level_one_boss import LevelOneBoss
from .radio_enemy import RadioEnemy
from .ring_enemy import RingEnemy

ENEMYS: dict[str, BaseEnemy] = {
    "BezierEnemy": BezierEnemy,
    "NormalEnemy": NormalEnemy,
    "LevelOneBoss": LevelOneBoss,
    "RadioEnemy": RadioEnemy,
    "RingEnemy": RingEnemy,
}
