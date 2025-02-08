import ball_track_bg_lib
import align
import comm
import time
import cv2
cap = cv2.VideoCapture(1)
ball_track_bg_lib.init(cap)

#input("press enter to start")
while True:
    pts = ball_track_bg_lib.run()
    r = str(align.align(pts[0][0], pts[0][1], pts[1][0], pts[1][1]))
    print("moving to:", r)
    comm.send_command(r)
    for i in range(40):
        cap.read()