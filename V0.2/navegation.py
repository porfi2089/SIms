from random import seed
from random import random as rnd

"""
noise_a = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
for x in noise_a:
    noise_a[x] = rnd()
    print(noise_a[x])
"""

def PID(p, i, d, e, le, ie, step):
    result = 0
    result = p * e + i * ie * step + d * (e - le) / step
    return result



