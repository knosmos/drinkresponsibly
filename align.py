SCALE = 2
X_OFFSET = 0
X_MIN = 0
X_MAX = 34
Y = 0

def convert(x):
    if x < X_MIN or x > X_MAX:
        return -1
    return int((x - X_OFFSET) * SCALE)

def align(x1, y1, x2, y2):
    # get trajectory from x1, y1 to x2, y2 and calculate x position at y = Y
    x = x1 + (x2 - x1) * (Y - y1) / (y2 - y1)
    return convert(x)