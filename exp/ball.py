import cv2
import numpy as np
import time

# load the video
video = cv2.VideoCapture("img/test/test2.mov")

_, background_frame = video.read()
background_frame = cv2.cvtColor(background_frame, cv2.COLOR_BGR2GRAY)

# Detect feature points in background frame
pts = cv2.goodFeaturesToTrack(
    background_frame, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3
)

subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = video.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # IMAGE STABILIZATION
    # Optical flow
    curr_pts, status, err = cv2.calcOpticalFlowPyrLK(gray, background_frame, pts, None)
    idx = np.where(status==1)[0]
    curr_pts = curr_pts[idx]
    prev_pts = pts[idx]

    m = cv2.estimateAffinePartial2D(curr_pts, prev_pts)[0]

    background_frame = gray.copy()

    # Apply transformation
    rows, cols = frame.shape[:2]
    gray = cv2.warpAffine(gray, m, (cols, rows))

    # background subtraction
    fgmask = subtractor.apply(gray)
    gray = cv2.bitwise_and(gray, gray, mask=fgmask)
    gray = cv2.medianBlur(gray, 5)
    #cv2.imshow("diff", gray)

    # dilation erosion
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    gray = cv2.dilate(gray, kernel, iterations=2)
    gray = cv2.erode(gray, kernel, iterations=1)

    # hough circles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    if circles is not None: 
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(gray, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(gray, (i[0], i[1]), 2, (0, 0, 255), 3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow("diff", gray)