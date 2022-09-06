import math
import time

import cv2
import mediapipe as mp


class hand_detector():
    def __init__(self,
                 mode=False,
                 max_hands=2,
                 model_complexity=1,
                 detection_con=0.5,
                 tracking_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        self.tip_ids = [4, 8, 12, 16, 20]

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_con,
                                        self.tracking_con)
        self.mpdraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, hand_lms, self.mphands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, nhand=0, draw=True, drawbbox=True):
        bbox = []
        x_list = []
        y_list = []

        self.lm_list = []

        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) == nhand + 1:
                realhandn = nhand
            else:
                realhandn = 0
            my_hand = self.results.multi_hand_landmarks[realhandn]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            bbox = xmin, ymin, xmax, ymax
            if drawbbox:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0, 2))

        return self.lm_list, bbox

    def fingers_up(self):
        fingers = []
        if len(self.lm_list) != 0:
            if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            return fingers

    def find_distance(self, p1, p2, img, draw=True):
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        lenght = math.hypot(x2 - x1, y2 - y1)
        return lenght, img, [x1, y1, x2, y2, cx, cy]


def column(matrix, i):
    return (row[i] for row in matrix)


p_time = 0
ctime = 0


def main():
    p_time = 0
    ctime = 0
    cam = cv2.VideoCapture(0)

    detect = hand_detector()

    while True:
        success, img = cam.read()
        img = detect.find_hands(img)
        lm_list = detect.find_position(img, draw=True)
        if len(lm_list) != 0:
            fingers = detect.fingers_up()
            print(fingers)

        ctime = time.time()
        fps = 1 / (ctime - p_time)
        p_time = ctime

        cv2.putText(img, str(round(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow('Cam', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
