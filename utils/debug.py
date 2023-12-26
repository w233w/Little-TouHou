import math
from pygame import draw


# 血条
# test
def draw_hp_bar(screen, pos, angle, color):
    # Center and (inner)radius of arc
    cx, cy, r, ir = pos[0], pos[1], 20, 17
    # Calculate the angle in degrees
    start = math.radians(135)
    # Start list of polygon points
    p = []
    for n in range(0, angle):
        x = cx + int(ir * math.cos((angle - n) * math.pi / 180 - start))
        y = cy + int(ir * math.sin((angle - n) * math.pi / 180 - start))
        p.append((x, y))
    for n in range(0, angle):
        x = cx + int(r * math.cos(n * math.pi / 180 - start))
        y = cy + int(r * math.sin(n * math.pi / 180 - start))
        p.append((x, y))
    # Draw
    if len(p) > 2:
        draw.polygon(screen, color, p)
