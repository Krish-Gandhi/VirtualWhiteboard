import cv2
import mediapipe as mp
import time
import math

# Function to calculate the difference between two MediaPipe hand landmarks
def dist(first, second) -> float:
    return math.sqrt((first.x - second.x) * (first.x - second.x) + (first.y - second.y) * (first.y - second.y))

# Creates a VideoCapture object by opening a camera for video capturing
cap = cv2.VideoCapture(0)

# sets up hand tracking with MediaPipe 
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# timers[0] and timers[1] used for FPS calculation
# timers[2] used for closing timer
# timers[3] used for eraser timer
timers = [0, 0, 0, 0]

# Booleans closing and erasing used to display timer info
closing = False
erasing = False

# Constants for amount of time (in seconds) gesture needs to be held before action occurs
eraseTimerLength = 3
closeTimerLength = 5

# drawn holds all points where user has drawn in (x,y) form
drawn = []

# tuples of colors
blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)
white = (255,255,255)
black = (0,0,0)

while True:
    # Reads and processes the current image from camera
    status, img = cap.read()
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Draws points on current image
    for point in drawn:
        cv2.circle(img, point, 7, blue, cv2.FILLED)

    # Defines dimensions of image
    h, w, c = img.shape

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Draws points on hand landmarks
            for id, lm in enumerate(handLms.landmark):
                # If finger tip, paint black, else paint white
                cx, cy = int(lm.x *w), int(lm.y*h)
                color = white
                if id in [4, 8, 12, 16, 20]:
                    color = black
                cv2.circle(img, (cx,cy), 7, color, cv2.FILLED)

            # x and y are coordinates of landmark of fingertip of the thumb
            x = int(handLms.landmark[4].x * w)
            y = int(handLms.landmark[4].y * h)
            
            # if thumb and pointer finger are close, 
            # make thumb tip landmark blue and add point to drawn 
            if dist(handLms.landmark[4], handLms.landmark[8]) < 0.05:
                drawn.append((x,y))
                cv2.circle(img, (x, y), 7, blue, cv2.FILLED)

            # if thumb and ring finger are close 
            if dist(handLms.landmark[4], handLms.landmark[16]) < 0.07:
                # make thumb tip landmark blue
                cv2.circle(img, (x, y), 7, red, cv2.FILLED)
                if (timers[0] - timers[2] > closeTimerLength):
                    # Close camera and close windows
                    cap.release()
                    cv2.destroyAllWindows()
                    print("Closed by thumb and ring gesture")
                    break
                else:
                    closing = True
            else:
                # Resets closer countdown
                timers[2] = timers[0]
                closing = False

            # if thumb and pinky finger are close 
            if dist(handLms.landmark[4], handLms.landmark[20]) < 0.07:
                # make thumb tip landmark green
                cv2.circle(img, (x, y), 7, green, cv2.FILLED)
                if (timers[0] - timers[3] > eraseTimerLength):
                    drawn.clear()
                else:
                    erasing = True
            else:
                # Resets eraser countdown
                timers[3] = timers[0]
                erasing = False

            # Draws all landmarks of hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    else:
        # Reset countdowns
        timers[3] = timers[0]
        erasing = False
        timers[2] = timers[0]
        closing = False
    
    # FPS calculation
    timers[0] = time.time()
    fps = 1/(timers[0]-timers[1])
    timers[1] = timers[0]

    # Flips image so user is not drawing in reverse
    img = cv2.flip(img, 1)

    # Display status text
    if erasing and eraseTimerLength - int(timers[0] - timers[3]) > -1 and closing:
        cv2.putText(img, "Erasing in " + str(eraseTimerLength - int(timers[0] - timers[3])) + "...", (10,420), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3)
        cv2.putText(img, "Closing in " + str(closeTimerLength - int(timers[0] - timers[2])) + "...", (10,470), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    elif erasing and eraseTimerLength - int(timers[0] - timers[3]) > -1:
        cv2.putText(img, "Erasing in " + str(eraseTimerLength - int(timers[0] - timers[3])) + "...", (10,470), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3)
    elif closing:
        cv2.putText(img, "Closing in " + str(closeTimerLength - int(timers[0] - timers[2])) + "...", (10,470), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.putText(img,"FPS: " + str(int(fps)), (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)