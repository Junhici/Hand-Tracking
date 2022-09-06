import os

import cv2
import numpy as np

import HandTrackingModule as htm

folderPath = 'Header'
my_list = os.listdir(folderPath)
overlay = []

for in_path in my_list:
    image = cv2.imread(f'{folderPath}/{in_path}')
    overlay.append(image)

header = overlay[0]
draw_color = (0, 0, 0)

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

dect = htm.hand_detector(detection_con=0.75)

xp, yp = 0, 0
img_canvas = np.zeros((480, 640, 3), np.uint8)

while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)

    img = dect.find_hands(img)
    lm_list, bbox = dect.find_position(img, draw=False)

    if len(lm_list) != 0:
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]

        fingers = dect.fingers_up()

        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
            if y1 < 125:
                if 0 < x1 < 160:
                    draw_color = (255, 0, 255)
                elif 161 < x1 < 320:
                    draw_color = (255, 0, 0)
                elif 321 < x1 < 480:
                    draw_color = (0, 0, 0)
                elif 481 < x1 < 640:
                    print('0')
                print(draw_color)
            print('Selection Mode')

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if draw_color == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), draw_color, 100)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, 100)
            else:
                cv2.line(img, (xp, yp), (x1, y1), draw_color, 15)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, 15)
            print('Draw Mode')

            xp, yp = x1, y1

    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, img_inv)
    img = cv2.bitwise_or(img, img_canvas)

    img[0:78, 0:640] = header
    # img = cv2.addWeighted(img, 0.5, img_canvas, 0.5, 0)
    cv2.imshow('cam', img)
    # cv2.imshow('Canvas', img_canvas)
    # cv2.imshow('Revert', img_inv)
    cv2.waitKey(1)
