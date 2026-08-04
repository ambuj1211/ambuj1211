import math


def arc(cx, cy, r, start, end):

    x1 = cx + r * math.cos(start)

    y1 = cy + r * math.sin(start)

    x2 = cx + r * math.cos(end)

    y2 = cy + r * math.sin(end)

    large = 1 if end - start > math.pi else 0

    return f"""
M {x1} {y1}
A {r} {r}
0
{large}
1
{x2}
{y2}
"""