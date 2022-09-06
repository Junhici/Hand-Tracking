# Import modules
import os
import time

import cv2

import HandTrackingModule as htm

# Set camera's weight and height
wcam, hcam = 640, 480

# Configure camera
cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)

# Create an hand detector
dect = htm.hand_detector(detection_con=0.75)

# Define previous and current time
p_time = 0
ctime = 0

while True:
    # Get camera's frame
    success, img = cam.read()

    # Find hands and landmarks
    img = dect.find_hands(img)
    lm_list, bbox = dect.find_position(img, draw=False)

    # If there are landmakrs in the landmark list
    if len(lm_list) != 0:
        # Detect which fingers are up
        fingers = dect.fingers_up()

        # Print fingers list
        print(fingers)

    # Show frame rate
    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime
    cv2.putText(img, str(round(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Show frame
    cv2.imshow('Cam', img)
    cv2.waitKey(1)
