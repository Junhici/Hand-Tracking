# Import modules
import math
import time

import cv2
import mediapipe as mp

# Create hand detector class
class hand_detector():
    def __init__(self,
                 mode=False,              # Detection Mode
                 max_hands=2,             # Maximum hands detectable
                 model_complexity=1,      # Complexity of hands model
                 detection_con=0.5,       # Minimum detection confidence
                 tracking_con=0.5):       # Minimum tracking confidence
        
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.tracking_con = tracking_con
        
        # Define fingers' tips
        self.tip_ids = [4, 8, 12, 16, 20]

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_con,
                                        self.tracking_con)
        self.mpdraw = mp.solutions.drawing_utils

    # Method to detect hands
    def find_hands(self, img, draw=True):
        # Convert image from BGR (Blue, Green, Red) to RGB (Red, Green, Blue)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Define results
        self.results = self.hands.process(imgRGB)

        # If there are landmarks on the image
        if self.results.multi_hand_landmarks:
            # For each hand's landmarks
            for hand_lms in self.results.multi_hand_landmarks:
                # If draw is true
                if draw:
                    # Draw landmarks on the image
                    self.mpdraw.draw_landmarks(img, hand_lms, self.mphands.HAND_CONNECTIONS)

        # Return image
        return img

    # Method to find landmarks' position
    def find_position(self, img, nhand=0, draw=True, drawbbox=True):
        # Define border box, x position list and y position list
        bbox = []
        x_list = []
        y_list = []

        # Define list of landmarks
        self.lm_list = []

        # If there are landmarks on the image
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) == nhand + 1:
                realhandn = nhand
            else:
                realhandn = 0
            my_hand = self.results.multi_hand_landmarks[realhandn]
            # For each id and landmarks in current hand's landmarks
            for id, lm in enumerate(my_hand.landmark):
                # Define a list of ids, c position and y position of each landmark
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                self.lm_list.append([id, cx, cy])
                # If draw is true
                if draw:
                    # Draw a circle on each landmark
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            # Find position of minimum x, maximum x, minimum y and miximum y
            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            
            # Put the results into a list
            bbox = xmin, ymin, xmax, ymax
            
            # If drawbox is true, draw a triangle using bbox informations
            if drawbbox:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0, 2))

        # Return landmark list and border box
        return self.lm_list, bbox

    # Method to find fingers up
    def fingers_up(self):
        # Define list of fingers up
        fingers = []
        
        # If there are some landmarks on the image
        if len(self.lm_list) != 0:
            if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # For each finger
            for id in range(1, 5):
                #Check if finger's tip is above the finger's base
                if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            return fingers

    # Method to find distance between two fingers
    def find_distance(self, p1, p2, img, draw=True):
        # Get finger's x and y positions
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        
        # Calculate center position
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        # If draw is true
        if draw:
            # Create a circle on the finger's and inbetween them
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Calculate the distance inbetween the fingers
        lenght = math.hypot(x2 - x1, y2 - y1)
        
        # Return distance, the image, fingers' x, y and center position
        return lenght, img, [x1, y1, x2, y2, cx, cy]

def column(matrix, i):
    return (row[i] for row in matrix)

# Define previous time and current time
p_time = 0
ctime = 0


def main():
    p_time = 0
    ctime = 0
    
    # Configure camera
    cam = cv2.VideoCapture(0)

    # Create hand detector
    detect = hand_detector()

    while True:
        # Get camera's frame
        success, img = cam.read()
        
        # Find hands, landmarks position and border box
        img = detect.find_hands(img)
        lm_list, bbox = detect.find_position(img, draw=True)
        
        # If there are landmarks in landmark list
        if len(lm_list) != 0:
            # Detect which fingers are up
            fingers = detect.fingers_up()
            
            # Print fingers
            print(fingers)

        # Show frame rate
        ctime = time.time()
        fps = 1 / (ctime - p_time)
        p_time = ctime
        cv2.putText(img, str(round(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        # Show image
        cv2.imshow('Cam', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
