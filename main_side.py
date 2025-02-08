import ball_track_side_lib
import comm
import time
import cv2
import numpy as np
cap = cv2.VideoCapture(1)
ball_track_side_lib.init(cap)

print("starting")

X1 = 0
X2 = 70
X1_R = 0
X2_R = 20
Y = 314

#input("press enter to start")
while True:
    p = ball_track_side_lib.run()
    if type(p) != bool:
        # solve quadratic for given y
        p[2] -= Y
        roots = np.roots(p)
        cand = []
        for root in roots:
            if np.isreal(root):
                cand.append(int(root.real))
        if len(cand) == 0:
            continue
        r = min(cand)
        # convert to real coordinates
        r = X2_R - int((r - X1) * (X2_R - X1_R) / (X2 - X1))

        print("moving to:", r)
        if r > 0 and r < 20:
            comm.send_command(str(r))
        for i in range(50):
            cap.read()