#Importing modules
import cv2
import pyautogui as pag
import HandTrackingModule as htm
import time

#Setting camera's weight and height
wcam = 1280
hcam = 720

#Configure the camera
cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)

#Create a detector
dect = htm.hand_detector(detection_con=0.8, max_hands=1 )

#Making a list of every key on the keyboard
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

#Method to draw all the buttons
def draw_all(image, buttonlist):
    for bottone in buttonlist:
        x, y = bottone.pos
        w, h = bottone.size
        cv2.rectangle(image, bottone.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(image, bottone.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return image

#Create a class Button
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

#Create a button list
button_list = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        button_list.append(Button([100 * x + 50, 100 * i + 50], key))

while True:
    #Getting camera's frame
    scs, img = cam.read()
        
    #Detectiong the hands and finding the position of the landmarks
    img = dect.find_hands(img)
    lm_list, bbox = dect.find_position(img, draw=False)

    #Drawing the buttons on the frame
    img = draw_all(img, button_list)

    #If the detector found some landmarks
    if lm_list:
        cv2.flip(img, 1)
        #For each button in the button list
        for button in button_list:
            #Get the position and the size of the current button
            x, y = button.pos
            w, h = button.size
        
        
            #If the landmark on the tip of the finger is in the zone of the button
            if x < lm_list[8][1] < x + w and y < lm_list[8][2] < y + h:
                #Change the button color
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                
                #Get the distance between the index finder and middle finger
                l, _, _ = dect.find_distance(8, 12, img)
                
                #If the distance is less than 100
                if l<100:
                    #Click the correct button
                    pag.keyDown(button.text.lower())
                    cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
                    time.sleep(0.15)

                        
    #Show the image
    cv2.imshow('cam', img)
    cv2.waitKey(1)
