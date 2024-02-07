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
vol_bar = 150

# Set camera's weight and height
wcam, hcam = 640, 480

# Configure camera
cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)

# Define previous time
p_time = 0

# Create hands detector
detect = htm.hand_detector(detection_con=0.5, max_hands=1, tracking_con=0.2)

while True:
    ret, img = cam.read()
    img = detect.find_hands(img)

    lm_list, bbox = detect.find_position(img, 1, False)

    if len(lm_list) > 0:

        # Prendiamo l'area della mano
        area = (bbox[2] - bbox[0]) * (bbox[3] + bbox[1])

        # Con questa condizion si limita la distanza a cui la mano si deve trovare
        if 20000<area<190000:
            distance, img, coords = detect.find_distance(4, 8, img, True)

            # Proporzione per la percentuale del volume (interpolazione lineare, formula non mia per ovvie ragioni)
            vol_per = np.interp(distance, [50, 200], [0, 100])
            vol_bar = (300*vol_per)/100


            fingers = detect.fingers_up()
            # Se il medio è abbassato
            print(vol_bar)
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(vol_per/100, None)
                cv2.circle(img, (coords[4], coords[5]), 15, (0, 255, 255), cv2.FILLED)
        # print(distance)
    cv2.rectangle(img, (20, 100), (90, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (20, 400-int(vol_bar)), (90, 400), (0, 255, 0), cv2.FILLED)

    ctime = time.time()
    fps = 1 / (ctime - p_time)
    p_time = ctime
    cv2.putText(img, str(round(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Camera", img)

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
