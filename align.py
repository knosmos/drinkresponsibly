X1 = 35
X2 = 200-145
X_MIN = 0
X_MAX = 34
SCALE = X_MAX/(200-X1-X2)
X_OFFSET = X1
Y = 475

def convert(x):
    r = int((x - X_OFFSET) * SCALE)
    r = max(min(r, X_MAX), X_MIN)
    return r

def align(x1, y1, x2, y2):
    # get trajectory from x1, y1 to x2, y2 and calculate x position at y = Y
    x = x1 + (x2 - x1) * (Y - y1) / (y2 - y1)
    return convert(x)