import cv2
import pyautogui as pag
import HandTrackingModule as htm
import time

wcam = 1280
hcam = 720

cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)

dect = htm.hand_detector(detection_con=0.8, max_hands=1 )

keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]


def draw_all(image, buttonlist):
    for bottone in buttonlist:
        x, y = bottone.pos
        w, h = bottone.size
        cv2.rectangle(image, bottone.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(image, bottone.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return image


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


button_list = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        button_list.append(Button([100 * x + 50, 100 * i + 50], key))

while True:
    scs, img = cam.read()

    img = dect.find_hands(img)
    lm_list, bbox = dect.find_position(img, draw=False)

    img = draw_all(img, button_list)

    if lm_list:
        cv2.flip(img, 1)
        for button in button_list:
            x, y = button.pos
            w, h = button.size

            if x < lm_list[8][1] < x + w and y < lm_list[8][2] < y + h:
                print('prsso il bottone')
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = dect.find_distance(8, 12, img)
                print(l)
                if l<100:
                    pag.keyDown(button.text.lower())
                    cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
                    time.sleep(0.15)

    cv2.imshow('cam', img)
    cv2.waitKey(1)
