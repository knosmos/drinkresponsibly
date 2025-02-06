# apriltag homography
import numpy as np
import cv2

SIZE_W = 2 * 100
SIZE_H = 6 * 100

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920//8)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080//8)

while True:
    # load image
    ret, img = cap.read()

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    (corners, ids, rejected) = detector.detectMarkers(img)  
    cv2.aruco.drawDetectedMarkers(img, corners, ids)
    cv2.imshow("img", img)

    if len(corners) != 4:
        cv2.waitKey(1)
        continue

    detected = [[ids[i], corners[i]] for i in range(4)]
    detected.sort(key = lambda x: x[0])
    # print(detected)
    bounding_box = [
        detected[0][1][0][2],
        detected[1][1][0][3],
        detected[3][1][0][0],
        detected[2][1][0][1]
    ]
    # print(bounding_box)

    img_boxed = img.copy()
    cv2.polylines(img_boxed, np.int32([bounding_box]), True, (0, 255, 0), 2)

    cv2.imshow("boxed", img_boxed)

    # homography

    vertices = [
        [0, 0],
        [SIZE_W, 0],
        [SIZE_W, SIZE_H],
        [0, SIZE_H]
    ]
    print(vertices)
    matrix = cv2.getPerspectiveTransform(np.float32(bounding_box), np.float32(vertices))
    dewarped = cv2.warpPerspective(img, matrix, (SIZE_W, SIZE_H))

    cv2.imshow("dewarped", dewarped)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break