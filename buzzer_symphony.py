import cv2
import numpy as np
import hand_detect as hd
import math
from boltiot import Bolt        
import conf 

mybolt = Bolt(conf.bolt_api_key, conf.device_id)

mode = False
volumeBar = 0

detector = hd.handDetector()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    detector.findHands(frame, draw = False)
    lmList = detector.findPosition(frame, draw = False)
    
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = ((x1+x2)//2), ((y1+y2)//2)
        
        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (219, 112, 147), 2)
        
        length = math.hypot(x2-x1, y2-y1)
        volumeBar = np.interp(length, [20,150], [400, 150])
        #print(length)
        
        if length < 20:
            cv2.circle(frame, (cx, cy), 10, (255, 255, 0), cv2.FILLED)
            
        cv2.rectangle(frame, (50, 150), (85, 400), (127, 255, 0), 3)
        cv2.rectangle(frame, (50, int(volumeBar)), (85, 400), (154, 250, 0), -1)
        
        if mode == True:
            mybolt.analogWrite('0', int(length))
            print(int(length))
            #time.sleep(1)
            mybolt.digitalWrite('0','LOW')
            mode = False
            
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break
cap.release() 
cv2.destroyAllWindows()

