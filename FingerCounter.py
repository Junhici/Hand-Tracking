import os
import time

import cv2

import HandTrackingModule as htm

wcam, hcam = 640, 480

cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)

dect = htm.hand_detector(detection_con=0.75)

p_time = 0
ctime = 0

while True:
    success, img = cam.read()

    img = dect.find_hands(img)
    lm_list = dect.find_position(img, draw=False)

    if len(lm_list) != 0:
        fingers = dect.fingers_up()

        print(fingers)

    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime

    cv2.putText(img, str(round(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('Cam', img)
    cv2.waitKey(1)
