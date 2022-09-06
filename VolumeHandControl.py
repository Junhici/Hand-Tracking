# Import modules
import math
import time
from ctypes import cast, POINTER

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingModule as htm

# Get speaker devices
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get volume range
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# Define volume, volume bar, volume percentage and area
vol = 0
vol_bar = 400
vol_per = 0
area = 0

# Set camera's weight and height
wcam, hcam = 640, 480

# Configure camera
cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)

# Define previous time
p_time = 0

# Create hands detector
detect = htm.hand_detector(detection_con=0., max_hands=1)

while True:
    # Get camera's frame
    success, img = cam.read()

    # Find hands, landmarks and bbox
    img = detect.find_hands(img)
    lm_list, bbox = detect.find_position(img, draw=False, nhand=1)

    # If there are landmarks in landmark list
    if len(lm_list) != 0:
        # Get area using border box's infos
        area = (bbox[2] + bbox[0]) * (bbox[3] - bbox[1]) // 100
        print(area)
        # If area is bigger than 900 pixels and smaller than 3000
        if 900 < area < 3000:
            # Find distance inbetween index and middle fingers
            lenght, img, info = detect.find_distance(4, 8, img)

            # Calculate volume bar and volume percentage using the distance
            vol_bar = np.interp(lenght, [40, 250], [400, 150])
            vol_per = np.interp(lenght, [40, 250], [0, 100])

            # Define smoothness
            smoothness = 1
            
            # Smooth volume percentage
            vol_per = smoothness * round(vol_per / smoothness)

            # Detect which fingers are up
            fingers = detect.fingers_up()
            
            # If middle finger is down
            if not fingers[4]:
                # Set volume to volume percentage
                volume.SetMasterVolumeLevelScalar(vol_per / 100, None)
                
                # Change circle color
                cv2.circle(img, (info[4], info[5]), 15, (0, 255, 255), cv2.FILLED)

    # Create an overlay
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    c_vol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'Volume: {str(round(c_vol))}', (400, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 2)
    cv2.putText(img, f'{str(round(vol_per))}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 2)

    # Show frame rate
    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime
    cv2.putText(img, str(round(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Show image
    cv2.imshow('Cam', img)
    cv2.waitKey(1)
