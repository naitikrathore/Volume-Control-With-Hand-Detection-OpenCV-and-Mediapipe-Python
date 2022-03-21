import cv2
import time
import numpy as np
import HandRecognitionModule as ml
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam, hCam = 640, 480                        #adjusting camera size where w is width and h is height



cap = cv2.VideoCapture(0)
cap.set(3, wCam)                             #adjusting camera
cap.set(4, hCam)
pTime = 0

detector = ml.handDetector(detectionCon=0.5)      #detetctionCon the higher it is  more accurate will be the hand detection


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]



while True:
    success, img = cap.read()                #checking sucess of video capturing
    img = detector.findHands(img)            #finding hands
    lmList = detector.findPosition(img, draw=False)     #detecting the position
    if len(lmList) != 0:
       # print(lmList[4], lmList[8])            #getting the tip of thumb and index finger


        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2      #center point where we will draw a point between those two fingers

        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)        #making circle on thumb
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)        #making circle on index
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 3), 3)             #drawing lines between two fingers
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)        #drawing circle between two fing


        length = math.hypot(x2 - x1, y2 - y1)       #getting values when both finger are close to each other and when they are far
        #print(length)


       #Hand range 20 - 230
       #Volume range -96 -0

        vol = np.interp(length, [30, 200], [minVol, maxVol])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<40:                                               #value which tells both finger are close or not
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)      #when both finger will close to each other it will light up green



    cTime = time.time()                      #setting fps meter
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 0, 0), 3)              #putting fps in image

    cv2.imshow("Img", img)
    cv2.waitKey(1)                           #checking after delay of 1 second




