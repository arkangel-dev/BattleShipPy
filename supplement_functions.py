import math

def CalculateDistance(tuplea, tupleb):
    xdiff = tuplea[0] - tupleb[0]
    ydiff = tuplea[1] - tupleb[1]
    xdiff = xdiff * xdiff
    ydiff = ydiff * ydiff
    diff = xdiff + ydiff
    result = math.sqrt(diff)
    return result

