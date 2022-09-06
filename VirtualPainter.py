# Import modules
import os

import cv2
import numpy as np

import HandTrackingModule as htm

# Find overlay's folder
folderPath = 'Header'
my_list = os.listdir(folderPath)
overlay = []

# Get overlay
for in_path in my_list:
    image = cv2.imread(f'{folderPath}/{in_path}')
    overlay.append(image)

# Define header
header = overlay[0]

# Define current draw color
draw_color = (0, 0, 0)

# Configure camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# Create hand detector
dect = htm.hand_detector(detection_con=0.75)

# Define x and y position
xp, yp = 0, 0

# Define image canvas
img_canvas = np.zeros((480, 640, 3), np.uint8)

while True:
    # Get camera's frame
    success, img = cam.read()
    
    # Flip image
    img = cv2.flip(img, 1)

    # Find hands, landmarks and border box
    img = dect.find_hands(img)
    lm_list, bbox = dect.find_position(img, draw=False)

    # If there are landmarks in landmark list
    if len(lm_list) != 0:
        # Get x and y of index and middle finger
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]
        
        # Detect which fingers are up
        fingers = dect.fingers_up()
        
        # ----------------------------------------------------------
        # SELECTION MODE
        # ----------------------------------------------------------

        # If index and middle finger are up
        if fingers[1] and fingers[2]:
            # Create a rectangle that starts from index finger's tip and ends on middle finger's tip
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
            
            # If index finger is higher than 125
            if y1 < 125:
                # If index finger is inbetween 0 and 160 pixels
                if 0 < x1 < 160:
                    # Set current draw color to pink
                    draw_color = (255, 0, 255)
                # Else if index finger is inbetween 161 and 320 pixels
                elif 161 < x1 < 320:
                    # Set current draw color to blue
                    draw_color = (255, 0, 0)
                # Else if index finger is inbetween 321 and 480 pixels
                elif 321 < x1 < 480:
                    # Set current draw color to black (eraser)
                    draw_color = (0, 0, 0)
                # Else if index finger is inbetween 481 and 640 pixels
                elif 481 < x1 < 640:
                    # Print 0
                    print('0')
                # Print current color
                print(draw_color)
            print('Selection Mode')
            
        # ----------------------------------------------------------
        # DRAW MODE
        # ----------------------------------------------------------

        # If index finger is up and middle finger is down
        if fingers[1] and fingers[2] == False:
            # Create a circle on index finger
            cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)
            # If x position and y position equals to zero
            if xp == 0 and yp == 0:
                # x position and y position equals to current x and current y
                xp, yp = x1, y1

            # If current draw color equals to black (eraser)
            if draw_color == (0, 0, 0):
                # Create a line on image following x and y position and current position with 100 pixels of thickness
                cv2.line(img, (xp, yp), (x1, y1), draw_color, 100)
                # Create a line on  canvas image following x and y position and current position with 100 pixels of thickness
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, 100)
            else:
                # Create a line on image following x and y position and current position with 15 pixels of thickness
                cv2.line(img, (xp, yp), (x1, y1), draw_color, 15)
                # Create a line on canvas image following x and y position and current position with 15 pixels of thickness
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, 15)
            print('Draw Mode')

            xp, yp = x1, y1

    # Convert image canvas from BGR to GRAY
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
