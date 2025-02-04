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

PINK_THRESH_LOW = [328//2, 10, 10]
PINK_THRESH_HIGH = [378//2, 255, 255]

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

    m = cv2.estimateAffinePartial2D(prev_pts, curr_pts)[0]

    #background_frame = gray.copy()

    # Apply transformation
    rows, cols = frame.shape[:2]
    gray = cv2.warpAffine(gray, m, (cols, rows))

    # background subtraction
    fgmask = subtractor.apply(gray)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    frame_subtracted = cv2.bitwise_and(frame, frame, mask=fgmask)

    # color detection
    hsv = cv2.cvtColor(frame_subtracted, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(PINK_THRESH_LOW), np.array(PINK_THRESH_HIGH))

    # dilation erosion
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200:
            # circularity check
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / perimeter ** 2
            if circularity > 0.4:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), -1)

    '''
    frame_inrange = cv2.bitwise_and(frame_subtracted, frame_subtracted, mask=mask)
    gray_inrange = cv2.cvtColor(frame_inrange, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray_inrange, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    if circles is not None: 
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame_inrange, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(frame_inrange, (i[0], i[1]), 2, (0, 0, 255), 3)
    '''

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow("frame_subtracted", frame_subtracted)
    cv2.imshow("mask", mask)
    cv2.imshow("detection", frame)
    time.sleep(0.05)