import cv2
from cvzone.HandTrackingModule import HandDetector as htm

cam = cv2.VideoCapture(0)
dect = htm.hand_detector(detection_con=0.75, max_hands=2)

while True:
    success, img = cam.read()
    hands, img = dect.find_hands(img)

    cv2.imshow(img)
    cv2.waitKey(0)