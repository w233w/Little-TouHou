from .base_drop import BaseDrop
from .bomb_drop import BombDrop
from .power_drop import PowerDrop
from .hp_drop import HPDrop

DROPS: dict[str, BaseDrop] = {
    "BombDrop": BombDrop,
    "PowerDrop": PowerDrop,
    "HPDrop": HPDrop,
}
