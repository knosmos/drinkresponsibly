import cv2
import numpy as np
import time


def init(cap):
    global video, background_frame
    video = cap
    # load the video
    _, background_frame = video.read()
    _, background_frame = video.read()
    #background_frame = cv2.resize(background_frame, (0, 0), fx=0.75, fy=0.75)
    background_frame = cv2.cvtColor(background_frame, cv2.COLOR_BGR2GRAY)
    background_frame = background_frame[0:350, 0:int(background_frame.shape[1] * 0.6)]

subtractor = cv2.createBackgroundSubtractorMOG2()

PINK_THRESH_LOW = [328//2, 10, 10]
PINK_THRESH_HIGH = [378//2, 255, 255]

past_points = []

def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

cv2.namedWindow('detection')
cv2.setMouseCallback('detection',draw_circle)

def run():
    global past_points, subtractor, background_frame
    ret, frame = video.read()
    if not ret:
        return False
    #frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
    # crop right side
    frame = frame[0:350, 0:int(frame.shape[1] * 0.6)]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 2, 75, 75) 

    # background subtraction
    fgmask = subtractor.apply(gray)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #fgmask = cv2.erode(fgmask, kernel, iterations=1)
    frame_subtracted = cv2.bitwise_and(frame, frame, mask=fgmask)
    # contours
    contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) <= 5:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:
                # convex hull
                contour = cv2.convexHull(contour)
                # circularity check
                #perimeter = cv2.arcLength(contour, True)
                #circularity = 4 * np.pi * area / perimeter ** 2
                if True:
                    cv2.drawContours(frame, [contour], -1, (0, 255, 0), -1)
                    # center
                    M = cv2.moments(contour)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    # attempt to match with previous points
                    for point_history in past_points:
                        if np.linalg.norm(np.array([cx, cy]) - point_history[0][-1]) < 300:
                            traj_pts = np.array(point_history[0], np.int32)
                            traj_pts = traj_pts.reshape((-1,1,2))
                            cv2.polylines(frame, [traj_pts], isClosed=False, color=(255, 0, 0), thickness=5)
                            point_history[0].append([cx, cy])
                            point_history[1] += 1
                            if len(point_history[0]) > 3:
                                # fit parabola and draw
                                p = np.polyfit(np.array(point_history[0])[:, 0], np.array(point_history[0])[:, 1], 2)
                                x = np.arange(0, frame.shape[1], 1)
                                if p[0] > 0:
                                    y = p[0] * x ** 2 + p[1] * x + p[2]
                                    cv2.polylines(frame, [np.array([np.array([x, y]).T], np.int32)], isClosed=False, color=(0, 255, 255), thickness=5)
                                    #cv2.imshow("frame_subtracted", frame_subtracted)
                                    cv2.imshow("mask", fgmask)
                                    cv2.imshow("detection", frame)
                                    cv2.waitKey(1)
                                    return p
                            break
                    else:
                        past_points.append([[[cx, cy]], 5])
    
    new_past_points = []
    for point_history in past_points:
        if point_history[1] != 0:
            new_past_points.append([point_history[0], point_history[1] - 1])
    past_points = new_past_points

    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()
    
    #cv2.imshow("frame_subtracted", frame_subtracted)
    cv2.imshow("mask", fgmask)
    cv2.imshow("detection", frame)

    return False