import cv2
import mediapipe as mp
import time
import HandRecognitionModule as mle

pTime = 0             # fps
cTime = 0              #fps
cap = cv2.VideoCapture(0)           #to capture video
detector = mle.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
       print(lmList[4])

    cTime = time.time()  # this will give the current time
    fps = 1 / (cTime - pTime)  # to get the fps cureent time minus previous time
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                (255, 0, 255), 3)  # fps meter

    cv2.imshow("Image", img)       # basic code to run a webcam
    cv2.waitKey(1)