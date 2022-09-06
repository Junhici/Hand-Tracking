import time

import cv2
import numpy as np
import pyautogui as pag

import HandTrackingModule as htm
import mouse

wcam, hcam = 640, 480

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_BUFFERSIZE, 2)
cam.set(3, wcam)
cam.set(4, hcam)
p_time = 0

dect = htm.hand_detector(max_hands=1, detection_con=0.75)

wsc, hsc = pag.size()
pag.FAILSAFE = False

frame_reduction = 100
smooth = 5
p_locX, p_locY = 0, 0
c_locX, c_locY = 0, 0

while True:
    scs, img = cam.read()

    img = dect.find_hands(img)
    lm_list, bbox = dect.find_position(img, draw=False)

    if len(lm_list) != 0:
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]

        fingers = dect.fingers_up()

        if fingers[1] and fingers[2] == 0:
            cv2.rectangle(img, (frame_reduction, frame_reduction), (wcam - frame_reduction, hcam - frame_reduction),
                          (255, 0, 255), 2)
            x3 = np.interp(x1, (frame_reduction, wcam - frame_reduction), (0, wsc))
            y3 = np.interp(y1, (frame_reduction, hcam - frame_reduction), (0, hsc))

            c_locX = p_locX + (x3 - p_locX) / smooth
            c_locY = p_locY + (y3 - p_locY) / smooth

            mouse.move(wsc - c_locX, c_locY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            p_locX, p_locY = c_locX, c_locY

        if fingers[1] and fingers[2]:
            length, img, info = dect.find_distance(8, 12, img)
            if length < 40:
                cv2.circle(img, (info[4], info[5]), 15, (255, 0, 0), cv2.FILLED)
                mouse.click()

    # Frame Rate
    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime
    cv2.putText(img, str(round(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('cam', img)
    cv2.waitKey(1)
