import time

import cv2

import HandTrackingModule as htm

p_time = 0
ctime = 0
cam = cv2.VideoCapture(0)

detect = htm.hand_detector()

while True:
    success, img = cam.read()
    img = detect.find_hands(img)
    lm_list = detect.find_position(img, draw=False)
    if len(lm_list) != 0:
        print(lm_list[4])
    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime

    cv2.putText(img, str(round(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

    cv2.imshow('Cam', img)
    cv2.waitKey(1)
