import cv2
import numpy as np
import time

# load the video
video = cv2.VideoCapture("img/test/output.mp4")

_, background_frame = video.read()
_, background_frame = video.read()
background_frame = cv2.resize(background_frame, (0, 0), fx=0.5, fy=0.5)
background_frame = cv2.cvtColor(background_frame, cv2.COLOR_BGR2GRAY)

# Detect feature points in background frame
pts = cv2.goodFeaturesToTrack(
    background_frame, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3
)

subtractor = cv2.createBackgroundSubtractorMOG2()

PINK_THRESH_LOW = [328//2, 10, 10]
PINK_THRESH_HIGH = [378//2, 255, 255]

past_points = []

while True:
    ret, frame = video.read()
    if not ret:
        break
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
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
    #mask = cv2.dilate(mask, kernel, iterations=1)
    #mask = cv2.erode(mask, kernel, iterations=1)

    # contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            # convex hull
            contour = cv2.convexHull(contour)
            # circularity check
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / perimeter ** 2
            if circularity > 0.5:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), -1)
                # center
                M = cv2.moments(contour)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                # attempt to match with previous points
                for point_history in past_points:
                    if np.linalg.norm(np.array([cx, cy]) - point_history[0][-1]) < 100:
                        # either close enough to last point in the history,
                        # or along the line created by the last five points
                        N_LINE = 2
                        # best fit line for the last N_LINE points
                        if len(point_history[0]) > N_LINE:
                            x = [point[0] for point in point_history[0][-N_LINE:]]
                            y = [point[1] for point in point_history[0][-N_LINE:]]
                            A = np.vstack([x, np.ones(len(x))]).T
                            m, c = np.linalg.lstsq(A, y, rcond=None)[0]
                            # check if the point is close to the line, and moving in the right direction
                            distance = np.abs(m * cx - cy + c) / np.sqrt(m ** 2 + 1)
                            direction = np.sign(m * cx - cy + c)
                            if distance < 60: # and direction > 0:
                                traj_pts = np.array(point_history[0], np.int32)
                                traj_pts = traj_pts.reshape((-1,1,2))
                                cv2.polylines(frame, [traj_pts], isClosed=False, color=(255, 0, 0), thickness=5)
                                point_history[0].append([cx, cy])
                                break

                        elif np.linalg.norm(np.array([cx, cy]) - point_history[0][-1]) < 60:
                            traj_pts = np.array(point_history[0], np.int32)
                            traj_pts = traj_pts.reshape((-1,1,2))
                            cv2.polylines(frame, [traj_pts], isClosed=False, color=(255, 0, 0), thickness=5)
                            point_history[0].append([cx, cy])
                            point_history[1] += 1
                            break
                else:
                    past_points.append([[[cx, cy]], 20])
    
    for point_history in past_points:
        if point_history[1] == 0:
            past_points.remove(point_history)
        else:
            point_history[1] -= 1

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
    time.sleep(0.1)