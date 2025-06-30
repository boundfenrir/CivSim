
import math


def polar_to_cartesian(q,r,size=1.0):
    x = size * 3/2 * q
    y = size * math.sqrt(3) * (r + q / 2)
    return x,y