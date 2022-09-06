import time

import cv2
import mediapipe as mp

cam = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
p_time = 0
ctime = 0

while True:
    success, img = cam.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id == 0:
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            mpdraw.draw_landmarks(img, hand_lms, mphands.HAND_CONNECTIONS)

    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime

    cv2.putText(img, str(round(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

    cv2.imshow('Cam', img)
    cv2.waitKey(1)
