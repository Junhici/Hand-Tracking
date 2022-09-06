# Import the modules
import time

import cv2
import numpy as np
import pyautogui as pag

import HandTrackingModule as htm
import mouse

# Set camera's weight and height
wcam, hcam = 640, 480

# Configure the camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_BUFFERSIZE, 2)
cam.set(3, wcam)
cam.set(4, hcam)

# Define previous_time
p_time = 0

# Create hand detector
dect = htm.hand_detector(max_hands=1, detection_con=0.75)

# Find the screen size
wsc, hsc = pag.size()
pag.FAILSAFE = False

# Define frame reduction
frame_reduction = 100

# Define cursor movement smoothness
smooth = 5

# Defince previous location X and Y and current location X and Y
p_locX, p_locY = 0, 0
c_locX, c_locY = 0, 0

while True:
    # Get camera's frame
    scs, img = cam.read()

    # Detect hands, find landmarks and hand's box
    img = dect.find_hands(img)
    lm_list, bbox = dect.find_position(img, draw=False)

    # If there are some landmarks in the list
    if len(lm_list) != 0:
        # Get X and Y of the index finger and X and Y of the middle finger
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]

        # Detect which fingers are up
        fingers = dect.fingers_up()

        # If index finger is up and middle finger is down
        if fingers[1] and fingers[2] == 0:
            # Create a screen in the frame
            cv2.rectangle(img, (frame_reduction, frame_reduction), (wcam - frame_reduction, hcam - frame_reduction),
                          (255, 0, 255), 2)
            
            # Get X and Y reducted
            x3 = np.interp(x1, (frame_reduction, wcam - frame_reduction), (0, wsc))
            y3 = np.interp(y1, (frame_reduction, hcam - frame_reduction), (0, hsc))

            # Get current X and Y position smoothed
            c_locX = p_locX + (x3 - p_locX) / smooth
            c_locY = p_locY + (y3 - p_locY) / smooth

            # Move the mouse to current X and Y location
            mouse.move(wsc - c_locX, c_locY)
            
            # Create a finger inbetween middle and index finger
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            
            # Define previous location with current location's values
            p_locX, p_locY = c_locX, c_locY

        # Get if index finger and middle finger are up
        if fingers[1] and fingers[2]:
            #Find the distance between index and middle finger
            length, img, info = dect.find_distance(8, 12, img)
            
            #If the length is less than 40
            if length < 40:
                #Change the color of the circle inbetween middle and index finger
                cv2.circle(img, (info[4], info[5]), 15, (255, 0, 0), cv2.FILLED)
                mouse.click()

    # Frame Rate
    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime
    cv2.putText(img, str(round(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    #Show the frame
    cv2.imshow('cam', img)
    cv2.waitKey(1)
