def PID(p, i, d, e, le, ie, step):
    result = 0
    result = p * e + i * ie * step + d * (e - le) / step
    return result